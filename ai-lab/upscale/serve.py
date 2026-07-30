"""Upscales an image or video using Real-ESRGAN (frame-by-frame for video)."""
import argparse
import json
from pathlib import Path

import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

BASE_MODEL_PATH = Path(__file__).parent / "checkpoints" / "RealESRGAN_x4plus.pth"
FINETUNED_MODEL_PATH = Path(__file__).parent / "checkpoints" / "finetuned" / "RealESRGAN_x4plus.pth"
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

_upsampler = None


def _load(scale: int):
    global _upsampler
    if _upsampler is not None:
        return
    model_path = FINETUNED_MODEL_PATH if FINETUNED_MODEL_PATH.exists() else BASE_MODEL_PATH
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=scale)
    _upsampler = RealESRGANer(scale=scale, model_path=str(model_path), model=model)


def _upscale_image(input_path: str, scale: int, output: str) -> dict:
    _load(scale)
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    output_image, _ = _upsampler.enhance(image, outscale=scale)
    cv2.imwrite(output, output_image)
    return {"output_path": output, "metadata": {"type": "image", "scale": scale}}


def _upscale_video(input_path: str, scale: int, output: str) -> dict:
    _load(scale)
    reader = cv2.VideoCapture(input_path)
    fps = reader.get(cv2.CAP_PROP_FPS)
    writer = None
    frame_count = 0

    while True:
        ok, frame = reader.read()
        if not ok:
            break
        upscaled, _ = _upsampler.enhance(frame, outscale=scale)
        if writer is None:
            h, w = upscaled.shape[:2]
            writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
        writer.write(upscaled)
        frame_count += 1

    reader.release()
    writer.release()
    return {"output_path": output, "metadata": {"type": "video", "scale": scale, "frames": frame_count}}


def run(input_path: str, scale: int = 4, output: str = "out.png", **kwargs) -> dict:
    if Path(input_path).suffix.lower() in VIDEO_EXTS:
        return _upscale_video(input_path, scale, output)
    return _upscale_image(input_path, scale, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--scale", type=int, default=4)
    parser.add_argument("--output", default="out.png")
    args = parser.parse_args()
    result = run(input_path=args.input_path, scale=args.scale, output=args.output)
    print(json.dumps(result, indent=2))
