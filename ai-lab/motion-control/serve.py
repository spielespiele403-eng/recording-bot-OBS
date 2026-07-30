"""Motion transfer via MagicAnimate: animates a reference photo with the
motion (pose sequence) extracted from a driving video.
"""
import argparse
import json
import sys
from pathlib import Path

import torch
from controlnet_aux import OpenposeDetector
from diffusers.utils import export_to_video
from PIL import Image

CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
REPO_DIR = CHECKPOINT_DIR / "magicanimate_repo"
PRETRAINED_DIR = CHECKPOINT_DIR / "pretrained_models"
ADAPTER_DIR = CHECKPOINT_DIR / "finetuned"

sys.path.insert(0, str(REPO_DIR))
from magicanimate.pipelines.pipeline_animation import MagicAnimatePipeline  # noqa: E402
from magicanimate.utils.videoreader import VideoReader  # noqa: E402

_pipe = None
_pose_detector = None


def _load():
    global _pipe, _pose_detector
    if _pipe is not None:
        return
    _pipe = MagicAnimatePipeline.from_pretrained(PRETRAINED_DIR, torch_dtype=torch.float16)
    if ADAPTER_DIR.exists():
        _pipe.unet.load_lora_adapter(ADAPTER_DIR)
    _pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    _pose_detector = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")


def run(reference_image_path: str, driving_video_path: str, output: str = "out.mp4", **kwargs) -> dict:
    _load()
    reference = Image.open(reference_image_path).convert("RGB")
    driving_frames = list(VideoReader(driving_video_path))
    pose_frames = [_pose_detector(Image.fromarray(f)) for f in driving_frames]

    frames = _pipe(reference_image=reference, pose_sequence=pose_frames).frames

    output_path = Path(output)
    export_to_video(frames, str(output_path), fps=25)

    return {
        "output_path": str(output_path),
        "metadata": {
            "reference_image": reference_image_path,
            "driving_video": driving_video_path,
            "num_frames": len(frames),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference_image_path", required=True)
    parser.add_argument("--driving_video_path", required=True)
    parser.add_argument("--output", default="out.mp4")
    args = parser.parse_args()
    result = run(
        reference_image_path=args.reference_image_path,
        driving_video_path=args.driving_video_path,
        output=args.output,
    )
    print(json.dumps(result, indent=2))
