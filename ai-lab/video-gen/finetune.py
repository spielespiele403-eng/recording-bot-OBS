"""LoRA fine-tunes the SVD UNet on the user's own short clips.

data_dir must contain one subfolder per clip, each with sequentially named
frames (000.png, 001.png, ...). The first frame of each clip is used as the
conditioning image, matching how SVD is conditioned at inference time.
"""
import argparse
from pathlib import Path

import torch
import torch.nn.functional as F
from diffusers import StableVideoDiffusionPipeline
from peft import LoraConfig
from PIL import Image
from torch.utils.data import DataLoader, Dataset

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
NUM_FRAMES = 25


class ClipDataset(Dataset):
    def __init__(self, data_dir: str):
        self.clip_dirs = sorted(p for p in Path(data_dir).iterdir() if p.is_dir())

    def __len__(self):
        return len(self.clip_dirs)

    def __getitem__(self, idx):
        frame_paths = sorted(self.clip_dirs[idx].glob("*.png"))[:NUM_FRAMES]
        frames = [Image.open(p).convert("RGB").resize((1024, 576)) for p in frame_paths]
        return frames


def main(data_dir: str, output_dir: str):
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        BASE_MODEL_DIR, torch_dtype=torch.float32
    )
    pipe.vae.requires_grad_(False)
    pipe.image_encoder.requires_grad_(False)
    pipe.unet.requires_grad_(False)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["to_k", "to_q", "to_v", "to_out.0"],
    )
    pipe.unet.add_adapter(lora_config)
    pipe.unet.train()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe.to(device)

    dataset = ClipDataset(data_dir)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True, collate_fn=lambda x: x[0])

    optimizer = torch.optim.AdamW(
        (p for p in pipe.unet.parameters() if p.requires_grad), lr=1e-4
    )

    for epoch in range(10):
        for frames in dataloader:
            conditioning_image = frames[0]
            image_embeddings = pipe._encode_image(conditioning_image, device, 1, False)
            latents = torch.stack(
                [
                    pipe.vae.encode(
                        pipe.image_processor.preprocess(f).to(device)
                    ).latent_dist.sample()
                    * pipe.vae.config.scaling_factor
                    for f in frames
                ],
                dim=1,
            )
            conditional_latents = pipe.vae.encode(
                pipe.image_processor.preprocess(conditioning_image).to(device)
            ).latent_dist.mode()
            conditional_latents = conditional_latents.unsqueeze(1).repeat(1, latents.shape[1], 1, 1, 1)

            noise = torch.randn_like(latents)
            timesteps = torch.randint(0, 1000, (1,), device=device).long()
            noisy_latents = pipe.scheduler.add_noise(latents, noise, timesteps)
            unet_input = torch.cat([noisy_latents, conditional_latents], dim=2)

            added_time_ids = pipe._get_add_time_ids(
                fps=7, motion_bucket_id=127, noise_aug_strength=0.02,
                dtype=image_embeddings.dtype, batch_size=1,
                num_videos_per_prompt=1, do_classifier_free_guidance=False,
            ).to(device)

            model_pred = pipe.unet(
                unet_input, timesteps, encoder_hidden_states=image_embeddings,
                added_time_ids=added_time_ids,
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
