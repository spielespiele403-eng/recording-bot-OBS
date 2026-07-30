"""Fine-tunes the Real-ESRGAN upsampling head on the user's own high-res images.

data_dir must contain high-resolution images; low-res/high-res training pairs
are generated automatically by downsampling each image by --scale.
"""
import argparse
import glob
import os
from pathlib import Path

import torch
import torch.nn.functional as F
from basicsr.archs.rrdbnet_arch import RRDBNet
from PIL import Image
from torchvision import transforms

BASE_MODEL_PATH = Path(__file__).parent / "checkpoints" / "RealESRGAN_x4plus.pth"
CROP_SIZE = 256


def load_pairs(data_dir: str, scale: int) -> list[tuple[torch.Tensor, torch.Tensor]]:
    to_tensor = transforms.ToTensor()
    pairs = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*"))):
        if Path(path).suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        hr = Image.open(path).convert("RGB").resize((CROP_SIZE, CROP_SIZE))
        lr = hr.resize((CROP_SIZE // scale, CROP_SIZE // scale), Image.BICUBIC)
        pairs.append((to_tensor(lr), to_tensor(hr)))
    return pairs


def main(data_dir: str, output_dir: str, scale: int = 4, epochs: int = 20):
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=scale)
    model.load_state_dict(torch.load(BASE_MODEL_PATH)["params_ema"])

    for param in model.parameters():
        param.requires_grad = False
    for param in model.conv_last.parameters():
        param.requires_grad = True

    optimizer = torch.optim.Adam(model.conv_last.parameters(), lr=1e-4)
    pairs = load_pairs(data_dir, scale)

    for epoch in range(epochs):
        for lr_img, hr_img in pairs:
            pred = model(lr_img.unsqueeze(0))
            loss = F.l1_loss(pred, hr_img.unsqueeze(0))
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print(f"epoch {epoch + 1}/{epochs} loss {loss.item():.4f}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    torch.save({"params_ema": model.state_dict()}, Path(output_dir) / "RealESRGAN_x4plus.pth")
    print(f"Saved fine-tuned weights to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    parser.add_argument("--scale", type=int, default=4)
    args = parser.parse_args()
    main(args.data_dir, args.output_dir, args.scale)
