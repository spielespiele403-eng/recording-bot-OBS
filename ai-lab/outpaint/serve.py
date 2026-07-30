"""Expands an image's canvas and inpaints the new border area (outpainting)."""
import argparse
import json
from pathlib import Path

import torch
from diffusers import AutoPipelineForInpainting
from PIL import Image, ImageDraw

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
LORA_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_pipe = None


def _load():
    global _pipe
    if _pipe is not None:
        return
    _pipe = AutoPipelineForInpainting.from_pretrained(BASE_MODEL_DIR, torch_dtype=torch.float16).to(
        "cuda"
    )
    if LORA_DIR.exists():
        _pipe.load_lora_weights(LORA_DIR)


def _expand_canvas(image: Image.Image, direction: str, expand_px: int) -> tuple[Image.Image, Image.Image]:
    w, h = image.size
    pad = {
        "left": (expand_px, 0, 0, 0),
        "right": (0, 0, expand_px, 0),
        "top": (0, expand_px, 0, 0),
        "bottom": (0, 0, 0, expand_px),
        "all": (expand_px, expand_px, expand_px, expand_px),
    }[direction]
    left, top, right, bottom = pad
    canvas = Image.new("RGB", (w + left + right, h + top + bottom), (0, 0, 0))
    canvas.paste(image, (left, top))

    mask = Image.new("L", canvas.size, 255)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([left, top, left + w, top + h], fill=0)
    return canvas, mask


def run(
    image_path: str,
    direction: str,
    expand_px: int,
    output: str = "out.png",
    prompt: str = "",
    **kwargs,
) -> dict:
    _load()
    image = Image.open(image_path).convert("RGB")
    canvas, mask = _expand_canvas(image, direction, expand_px)

    result = _pipe(
        prompt=prompt or "continue the background seamlessly, photorealistic",
        image=canvas,
        mask_image=mask,
        width=canvas.width,
        height=canvas.height,
    ).images[0]

    output_path = Path(output)
    result.save(output_path)
    return {
        "output_path": str(output_path),
        "metadata": {"direction": direction, "expand_px": expand_px, "size": list(result.size)},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--direction", default="all", choices=["left", "right", "top", "bottom", "all"])
    parser.add_argument("--expand_px", type=int, default=256)
    parser.add_argument("--output", default="out.png")
    args = parser.parse_args()
    result = run(
        image_path=args.image_path,
        direction=args.direction,
        expand_px=args.expand_px,
        output=args.output,
    )
    print(json.dumps(result, indent=2))
