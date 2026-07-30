"""LoRA fine-tunes the MagicAnimate UNet's attention layers on the user's own
reference-image + driving-video pairs, so it renders that specific person's
appearance and clothing more faithfully during motion transfer.

data_dir must contain one subfolder per training example, each with:
  reference.png     - a still photo of the person
  driving/           - frames of a video showing the target motion (extracted
                       with e.g. ffmpeg -i clip.mp4 driving/%04d.png)

Note: magic-animate is a fast-moving research repo, not a stable pip package.
The class paths imported below (from checkpoints/magicanimate_repo) match the
repo's structure as of its initial release; if download_base_model.py pulled
a newer commit with renamed modules, adjust the imports accordingly.
"""
import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from controlnet_aux import OpenposeDetector
from peft import LoraConfig
from PIL import Image
from torch.utils.data import DataLoader, Dataset

CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
REPO_DIR = CHECKPOINT_DIR / "magicanimate_repo"
PRETRAINED_DIR = CHECKPOINT_DIR / "pretrained_models"

sys.path.insert(0, str(REPO_DIR))
from magicanimate.pipelines.pipeline_animation import MagicAnimatePipeline  # noqa: E402


class MotionPairDataset(Dataset):
    def __init__(self, data_dir: str, pose_detector: OpenposeDetector):
        self.example_dirs = sorted(p for p in Path(data_dir).iterdir() if p.is_dir())
        self.pose_detector = pose_detector

    def __len__(self):
        return len(self.example_dirs)

    def __getitem__(self, idx):
        example_dir = self.example_dirs[idx]
        reference = Image.open(example_dir / "reference.png").convert("RGB")
        driving_frames = sorted((example_dir / "driving").glob("*.png"))
        pose_frames = [self.pose_detector(Image.open(p).convert("RGB")) for p in driving_frames]
        return reference, pose_frames


def main(data_dir: str, output_dir: str):
    pipe = MagicAnimatePipeline.from_pretrained(PRETRAINED_DIR)
    pipe.unet.requires_grad_(False)
    pipe.appearance_encoder.requires_grad_(False)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
    )
    pipe.unet.add_adapter(lora_config)
    pipe.unet.train()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe.to(device)

    pose_detector = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
    dataset = MotionPairDataset(data_dir, pose_detector)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True, collate_fn=lambda x: x[0])

    optimizer = torch.optim.AdamW(
        (p for p in pipe.unet.parameters() if p.requires_grad), lr=1e-4
    )

    for epoch in range(10):
        for reference, pose_frames in dataloader:
            appearance_latents = pipe.encode_reference(reference, device)
            pose_latents = pipe.encode_pose_sequence(pose_frames, device)
            target_latents = pipe.encode_video_latents(pose_frames, device)

            noise = torch.randn_like(target_latents)
            timesteps = torch.randint(0, 1000, (1,), device=device).long()
            noisy_latents = pipe.scheduler.add_noise(target_latents, noise, timesteps)

            model_pred = pipe.unet(
                noisy_latents, timesteps,
                encoder_hidden_states=appearance_latents,
                pose_condition=pose_latents,
            ).sample

            loss = F.mse_loss(model_pred, noise)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print(f"epoch {epoch}: loss {loss.item():.4f}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    pipe.unet.save_lora_adapter(output_path)
    print(f"Saved LoRA adapter to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
