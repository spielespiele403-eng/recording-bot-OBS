"""Fine-tunes SAM by training only the mask decoder head on user-provided
object categories. SAM's image encoder and prompt encoder stay frozen; this
is the standard cheap way to bias SAM's promptable segmentation towards a
specific class of foreground subjects, since retraining the ViT encoder
itself needs orders of magnitude more data/compute than most users have.

data_dir must contain images/<name>.jpg and masks/<name>.png (binary ground
truth masks, same stem as the image, foreground pixels > 0).
"""
import argparse
import glob
import os
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from transformers import SamModel, SamProcessor

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def _bbox_from_mask(mask: np.ndarray) -> list[int]:
    ys, xs = np.where(mask > 0)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


class MaskDataset(Dataset):
    def __init__(self, data_dir: str, processor: SamProcessor):
        self.image_paths = sorted(glob.glob(os.path.join(data_dir, "images", "*")))
        self.mask_paths = sorted(glob.glob(os.path.join(data_dir, "masks", "*")))
        self.processor = processor

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        mask = np.array(Image.open(self.mask_paths[idx]).convert("L"))
        box = _bbox_from_mask(mask)
        inputs = self.processor(image, input_boxes=[[box]], return_tensors="pt")
        return {
            "pixel_values": inputs["pixel_values"][0],
            "input_boxes": inputs["input_boxes"][0],
            "ground_truth_mask": torch.from_numpy((mask > 0).astype(np.float32)),
        }


def main(data_dir: str, output_dir: str, epochs: int, lr: float):
    processor = SamProcessor.from_pretrained(BASE_MODEL_DIR)
    model = SamModel.from_pretrained(BASE_MODEL_DIR)

    for param in model.vision_encoder.parameters():
        param.requires_grad = False
    for param in model.prompt_encoder.parameters():
        param.requires_grad = False

    dataset = MaskDataset(data_dir, processor)
    loader = DataLoader(dataset, batch_size=1, shuffle=True)
    optimizer = torch.optim.Adam(model.mask_decoder.parameters(), lr=lr)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    model.train()
    for epoch in range(epochs):
        for batch in loader:
            outputs = model(
                pixel_values=batch["pixel_values"],
                input_boxes=batch["input_boxes"],
                multimask_output=False,
            )
            gt_mask = batch["ground_truth_mask"]
            pred_mask = torch.nn.functional.interpolate(
                outputs.pred_masks.squeeze(1), size=gt_mask.shape[-2:], mode="bilinear", align_corners=False
            ).squeeze(1)
            loss = loss_fn(pred_mask, gt_mask)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f"epoch {epoch+1}/{epochs} loss {loss.item():.4f}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    processor.save_pretrained(output_dir)
    print(f"Saved fine-tuned SAM (decoder head) to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-5)
    args = parser.parse_args()
    main(args.data_dir, args.output_dir, args.epochs, args.lr)
