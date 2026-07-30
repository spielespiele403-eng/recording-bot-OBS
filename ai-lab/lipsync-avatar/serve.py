"""Audio-driven talking avatar: lip-syncs (Wav2Lip) or fully animates a still
photo (SadTalker) to a given audio track.

Wav2Lip has no clean importable Python API (its logic lives in a
script-guarded inference.py), so it's invoked via subprocess, matching how the
upstream repo is meant to be used. SadTalker exposes a proper `SadTalker`
class, so that's imported and called directly.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = CHECKPOINT_DIR / "finetuned"

WAV2LIP_REPO = CHECKPOINT_DIR / "wav2lip" / "repo"
WAV2LIP_WEIGHTS = CHECKPOINT_DIR / "wav2lip" / "weights" / "wav2lip_gan.pth"

SADTALKER_REPO = CHECKPOINT_DIR / "sadtalker" / "repo"
SADTALKER_WEIGHTS = SADTALKER_REPO / "checkpoints"

_sadtalker = None


def _run_wav2lip(face_path: str, audio_path: str, output: str) -> dict:
    checkpoint = ADAPTER_DIR / "wav2lip_gan.pth" if ADAPTER_DIR.exists() else WAV2LIP_WEIGHTS
    subprocess.run(
        [
            sys.executable, str(WAV2LIP_REPO / "inference.py"),
            "--checkpoint_path", str(checkpoint),
            "--face", face_path,
            "--audio", audio_path,
            "--outfile", output,
        ],
        check=True,
        cwd=WAV2LIP_REPO,
    )
    return {"output_path": output, "metadata": {"mode": "wav2lip", "checkpoint": str(checkpoint)}}


def _run_sadtalker(face_path: str, audio_path: str, output: str) -> dict:
    global _sadtalker
    if _sadtalker is None:
        sys.path.insert(0, str(SADTALKER_REPO))
        from src.gradio_demo import SadTalker

        _sadtalker = SadTalker(checkpoint_path=str(SADTALKER_WEIGHTS), lazy_load=True)

    result_dir = Path(output).parent / "sadtalker_tmp"
    result_dir.mkdir(parents=True, exist_ok=True)
    generated_path = _sadtalker.test(
        source_image=face_path, driven_audio=audio_path, result_dir=str(result_dir)
    )
    Path(generated_path).replace(output)
    return {"output_path": output, "metadata": {"mode": "sadtalker"}}


def run(face_image_or_video_path: str, audio_path: str, mode: str = "wav2lip", output: str = "out.mp4", **kwargs) -> dict:
    if mode == "wav2lip":
        return _run_wav2lip(face_image_or_video_path, audio_path, output)
    if mode == "sadtalker":
        return _run_sadtalker(face_image_or_video_path, audio_path, output)
    raise ValueError(f"unknown mode: {mode!r} (expected 'wav2lip' or 'sadtalker')")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--face_image_or_video_path", required=True)
    parser.add_argument("--audio_path", required=True)
    parser.add_argument("--mode", default="wav2lip", choices=["wav2lip", "sadtalker"])
    parser.add_argument("--output", default="out.mp4")
    args = parser.parse_args()
    result = run(
        face_image_or_video_path=args.face_image_or_video_path,
        audio_path=args.audio_path,
        mode=args.mode,
        output=args.output,
    )
    print(json.dumps(result, indent=2))
