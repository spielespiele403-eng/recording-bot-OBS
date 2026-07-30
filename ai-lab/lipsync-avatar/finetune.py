"""Identity-specific fine-tuning of Wav2Lip on the user's own talking-head
footage, so the mouth region is rendered more accurately for that one face.

Wav2Lip is a small conv-based generator (not a transformer), so "LoRA" here
means peft LoRA adapters injected into its Conv2d/ConvTranspose2d decoder
layers rather than the attention-layer LoRA used in the other modules.

data_dir must be preprocessed like Wav2Lip's own training data (see its
preprocess.py): one subfolder per clip containing numbered face crops
(0.jpg, 1.jpg, ...) at 25fps and an audio.wav with the matching speech.
"""
import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from PIL import Image
from torch.utils.data import DataLoader, Dataset

CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
WAV2LIP_REPO = CHECKPOINT_DIR / "wav2lip" / "repo"
WAV2LIP_WEIGHTS = CHECKPOINT_DIR / "wav2lip" / "weights" / "wav2lip_gan.pth"

sys.path.insert(0, str(WAV2LIP_REPO))
import audio  # noqa: E402
from models import Wav2Lip  # noqa: E402

SYNC_LEN = 5  # Wav2Lip's fixed sync window: 5 consecutive frames per sample


class ClipDataset(Dataset):
    def __init__(self, data_dir: str):
        self.clip_dirs = sorted(p for p in Path(data_dir).iterdir() if p.is_dir())

    def __len__(self):
        return len(self.clip_dirs)

    def __getitem__(self, idx):
        clip_dir = self.clip_dirs[idx]
        frame_paths = sorted(clip_dir.glob("*.jpg"), key=lambda p: int(p.stem))[:SYNC_LEN]
        frames = torch.stack(
            [torch.from_numpy(__import__("numpy").array(Image.open(p))).permute(2, 0, 1) / 255.0
             for p in frame_paths]
        )
        wav = audio.load_wav(str(clip_dir / "audio.wav"), 16000)
        mel = torch.from_numpy(audio.melspectrogram(wav)).unsqueeze(0)
        return frames.float(), mel.float()


def main(data_dir: str, output_dir: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = Wav2Lip()
    checkpoint = torch.load(WAV2LIP_WEIGHTS, map_location=device)
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["face_decoder_blocks", "output_block"],
    )
    model = get_peft_model(model, lora_config)
    model.train()

    dataset = ClipDataset(data_dir)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
    optimizer = torch.optim.AdamW(
        (p for p in model.parameters() if p.requires_grad), lr=1e-4
    )

    for epoch in range(20):
        for frames, mel in dataloader:
            frames, mel = frames.to(device), mel.to(device)
            lower_half = frames.clone()
            lower_half[:, :, frames.shape[2] // 2 :, :] = 0.0

            generated = model(mel, lower_half)
            loss = F.l1_loss(generated, frames)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print(f"epoch {epoch}: loss {loss.item():.4f}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_path)
    print(f"Saved LoRA adapter to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
