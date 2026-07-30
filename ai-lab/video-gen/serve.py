"""Image-to-video generation via Stable Video Diffusion."""
import argparse
import json
from pathlib import Path

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video, load_image

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_pipe = None


def _load():
    global _pipe
    if _pipe is not None:
        return
    _pipe = StableVideoDiffusionPipeline.from_pretrained(
        BASE_MODEL_DIR, torch_dtype=torch.float16, variant="fp16"
    )
    if ADAPTER_DIR.exists():
        _pipe.unet.load_lora_adapter(ADAPTER_DIR)
    _pipe.enable_model_cpu_offload()


def run(image_path: str, output: str = "out.mp4", num_frames: int = 25, **kwargs) -> dict:
    _load()
    image = load_image(image_path).resize((1024, 576))
    frames = _pipe(image, decode_chunk_size=8, num_frames=num_frames).frames[0]

    output_path = Path(output)
    export_to_video(frames, str(output_path), fps=7)

    return {
        "output_path": str(output_path),
        "metadata": {"num_frames": num_frames, "fps": 7, "source_image": image_path},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--output", default="out.mp4")
    parser.add_argument("--num_frames", type=int, default=25)
    args = parser.parse_args()
    result = run(image_path=args.image_path, output=args.output, num_frames=args.num_frames)
    print(json.dumps(result, indent=2))
