"""Removes the background from an image using SAM, prompted with a single
foreground point (image center by default). A fixed point prompt is used
instead of a full automatic-mask-generator pass, which is much slower and
often segments the wrong region for single-subject cutouts.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import SamModel, SamProcessor

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
FINETUNED_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_processor = None


def _load():
    global _model, _processor
    if _model is not None:
        return
    model_dir = FINETUNED_DIR if FINETUNED_DIR.exists() else BASE_MODEL_DIR
    _processor = SamProcessor.from_pretrained(model_dir)
    _model = SamModel.from_pretrained(model_dir)
    _model.eval()


def run(image_path: str, output: str = "out.png", point: list | None = None, **kwargs) -> dict:
    _load()
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    input_point = point or [width // 2, height // 2]

    inputs = _processor(image, input_points=[[input_point]], return_tensors="pt")
    with torch.no_grad():
        outputs = _model(**inputs, multimask_output=True)

    masks = _processor.image_processor.post_process_masks(
        outputs.pred_masks, inputs["original_sizes"], inputs["reshaped_input_sizes"]
    )[0][0]
    scores = outputs.iou_scores.squeeze()
    best_idx = int(scores.argmax().item())
    mask = (masks[best_idx].numpy() * 255).astype(np.uint8)

    rgba = image.convert("RGBA")
    rgba.putalpha(Image.fromarray(mask))

    output_path = Path(output)
    rgba.save(output_path)
    metadata = {"score": float(scores[best_idx]), "point": input_point}
    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--output", default="out.png")
    args = parser.parse_args()
    result = run(image_path=args.image_path, output=args.output)
    print(json.dumps(result, indent=2))
