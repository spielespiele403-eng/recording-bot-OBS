"""Generates an image from a text prompt (text-to-image)."""
import argparse
import json
from pathlib import Path

import torch
from diffusers import DiffusionPipeline

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
LORA_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_pipe = None


def _load():
    global _pipe
    if _pipe is not None:
        return
    _pipe = DiffusionPipeline.from_pretrained(BASE_MODEL_DIR, torch_dtype=torch.float16).to("cuda")
    if LORA_DIR.exists():
        _pipe.load_lora_weights(LORA_DIR)


def run(prompt: str, output: str = "out.png", width: int = 1024, height: int = 1024, **kwargs) -> dict:
    _load()
    image = _pipe(prompt=prompt, width=width, height=height).images[0]
    output_path = Path(output)
    image.save(output_path)
    return {
        "output_path": str(output_path),
        "metadata": {"prompt": prompt, "width": width, "height": height},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", default="out.png")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    args = parser.parse_args()
    result = run(prompt=args.prompt, output=args.output, width=args.width, height=args.height)
    print(json.dumps(result, indent=2))
