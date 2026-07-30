"""Hauptanwendungsfall: Prompt -> fertiges Video mit eigenem Avatar in eigener Stimme.

prompt -> llm -> voice -> lipsync-avatar -> upscale -> final_video
"""
import argparse
import importlib.util
import sys
from pathlib import Path

AI_LAB_DIR = Path(__file__).resolve().parent


def _run_module(module_name: str, **kwargs) -> dict:
    module_dir = AI_LAB_DIR / module_name
    sys.path.insert(0, str(module_dir))
    try:
        spec = importlib.util.spec_from_file_location(
            f"{module_name.replace('-', '_')}_serve", module_dir / "serve.py"
        )
        serve = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(serve)
        return serve.run(**kwargs)
    finally:
        sys.path.remove(str(module_dir))


def generate_video(
    prompt: str,
    speaker_wav: str,
    face_image_path: str,
    language: str = "en",
    output: str = "final_video.mp4",
) -> str:
    script_result = _run_module("llm", prompt=prompt)
    script = script_result["metadata"]["script"]

    voice_result = _run_module("voice", text=script, speaker_wav=speaker_wav, language=language)
    audio_path = voice_result["output_path"]

    lipsync_result = _run_module(
        "lipsync-avatar", face_image_or_video_path=face_image_path, audio_path=audio_path
    )
    video_path = lipsync_result["output_path"]

    upscale_result = _run_module("upscale", input_path=video_path, scale=2, output=output)
    return upscale_result["output_path"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--speaker-wav", required=True)
    parser.add_argument("--face-image", required=True)
    parser.add_argument("--output", default="final_video.mp4")
    args = parser.parse_args()
    final_path = generate_video(
        prompt=args.prompt,
        speaker_wav=args.speaker_wav,
        face_image_path=args.face_image,
        output=args.output,
    )
    print(final_path)
