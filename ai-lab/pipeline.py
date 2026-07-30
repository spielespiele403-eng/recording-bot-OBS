"""Hauptanwendungsfall: Prompt -> fertiges Video mit Avatar + Stimme.

Zwei Modi pro Komponente:
- Avatar: eigenes Foto (face_image_path) ODER automatisch generierter Avatar
  (wenn face_image_path fehlt, wird ueber image-gen ein Avatar-Bild erzeugt,
  gesteuert per avatar_prompt).
- Stimme: eigene geklonte Stimme (speaker_wav) ODER ein vordefiniertes Preset
  (voice_preset, aufgeloest ueber voice/presets/presets.json).

prompt -> llm -> [image-gen fuer Avatar, falls kein Foto] -> voice -> lipsync-avatar -> upscale -> final_video
"""
import argparse
import importlib.util
import sys
from pathlib import Path

AI_LAB_DIR = Path(__file__).resolve().parent
DEFAULT_AVATAR_PROMPT = (
    "professional headshot portrait of a friendly person, studio lighting, "
    "neutral background, looking at camera"
)


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
    speaker_wav: str = None,
    voice_preset: str = "default",
    face_image_path: str = None,
    avatar_prompt: str = DEFAULT_AVATAR_PROMPT,
    language: str = "en",
    output: str = "final_video.mp4",
) -> str:
    script_result = _run_module("llm", prompt=prompt)
    script = script_result["metadata"]["script"]

    if face_image_path is None:
        avatar_result = _run_module("image-gen", prompt=avatar_prompt, output="auto_avatar.png")
        face_image_path = avatar_result["output_path"]

    voice_result = _run_module(
        "voice",
        text=script,
        speaker_wav=speaker_wav,
        voice_preset=voice_preset,
        language=language,
    )
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
    parser.add_argument("--speaker-wav", default=None, help="Eigene Stimme klonen. Weglassen fuer --voice-preset.")
    parser.add_argument("--voice-preset", default="default", help="Preset-Stimme, falls kein --speaker-wav angegeben ist.")
    parser.add_argument("--face-image", default=None, help="Eigenes Avatar-Foto. Weglassen fuer automatisch generierten Avatar.")
    parser.add_argument("--avatar-prompt", default=DEFAULT_AVATAR_PROMPT, help="Prompt fuer den Avatar, falls kein --face-image angegeben ist.")
    parser.add_argument("--output", default="final_video.mp4")
    args = parser.parse_args()
    final_path = generate_video(
        prompt=args.prompt,
        speaker_wav=args.speaker_wav,
        voice_preset=args.voice_preset,
        face_image_path=args.face_image,
        avatar_prompt=args.avatar_prompt,
        output=args.output,
    )
    print(final_path)
