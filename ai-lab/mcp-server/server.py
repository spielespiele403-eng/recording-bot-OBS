"""MCP server exposing every ai-lab module as one tool each.

Each tool dynamically imports the sibling module's serve.py and calls its
run(**kwargs), so this file never imports heavy model deps directly and
stays usable even if a given module isn't finished yet.
"""
import importlib.util
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

AI_LAB_DIR = Path(__file__).resolve().parent.parent

mcp = FastMCP("ai-lab")


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


@mcp.tool()
def write_script(prompt: str, max_length: int = 300) -> dict:
    """Generate a spoken-video script from a short prompt. (llm/)"""
    return _run_module("llm", prompt=prompt, max_length=max_length)


@mcp.tool()
def translate_script(text: str, target_lang: str) -> dict:
    """Translate a script/text into another language. (translate/)"""
    return _run_module("translate", text=text, target_lang=target_lang)


@mcp.tool()
def generate_image(
    prompt: str, output: str = "out.png", width: int = 1024, height: int = 1024
) -> dict:
    """Generate an image from a text prompt. (image-gen/)"""
    return _run_module(
        "image-gen", prompt=prompt, output=output, width=width, height=height
    )


@mcp.tool()
def outpaint_image(
    image_path: str, direction: str, expand_px: int, output: str = "out.png"
) -> dict:
    """Expand an image beyond its original borders. (outpaint/)"""
    return _run_module(
        "outpaint",
        image_path=image_path,
        direction=direction,
        expand_px=expand_px,
        output=output,
    )


@mcp.tool()
def reframe(image_path: str, target_aspect_ratio: str, output: str = "out.png") -> dict:
    """Change an image's aspect ratio via smart crop/outpaint. (reframe/)"""
    return _run_module(
        "reframe",
        image_path=image_path,
        target_aspect_ratio=target_aspect_ratio,
        output=output,
    )


@mcp.tool()
def upscale_media(
    input_path: str,
    scale: int = 4,
    output: str = "out.png",
    media_type: str = "image",
) -> dict:
    """Upscale an image or video. media_type is 'image' or 'video' (routing hint only). (upscale/)"""
    return _run_module("upscale", input_path=input_path, scale=scale, output=output)


@mcp.tool()
def remove_background(image_path: str, output: str = "out.png") -> dict:
    """Cut out the background of an image, leaving transparency. (bg-remove/)"""
    return _run_module("bg-remove", image_path=image_path, output=output)


@mcp.tool()
def generate_3d(image_path: str, output: str = "out.glb") -> dict:
    """Turn a single image into a 3D mesh (.glb). (image-to-3d/)"""
    return _run_module("image-to-3d", image_path=image_path, output=output)


@mcp.tool()
def generate_video(image_path: str, output: str = "out.mp4", num_frames: int = 25) -> dict:
    """Animate a still image into a short video. (video-gen/)"""
    return _run_module(
        "video-gen", image_path=image_path, output=output, num_frames=num_frames
    )


@mcp.tool()
def motion_control(
    reference_image_path: str, driving_video_path: str, output: str = "out.mp4"
) -> dict:
    """Transfer motion from a driving video onto a reference image. (motion-control/)"""
    return _run_module(
        "motion-control",
        reference_image_path=reference_image_path,
        driving_video_path=driving_video_path,
        output=output,
    )


@mcp.tool()
def lipsync_avatar(
    face_image_or_video_path: str,
    audio_path: str,
    mode: str = "wav2lip",
    output: str = "out.mp4",
) -> dict:
    """Make a face image/video speak in sync with an audio track. (lipsync-avatar/)"""
    return _run_module(
        "lipsync-avatar",
        face_image_or_video_path=face_image_or_video_path,
        audio_path=audio_path,
        mode=mode,
        output=output,
    )


@mcp.tool()
def generate_speech(
    text: str,
    speaker_wav: str = None,
    voice_preset: str = "default",
    language: str = "en",
    output: str = "out.wav",
) -> dict:
    """Synthesize speech. Pass speaker_wav to clone a voice, or omit it and use voice_preset for a preset voice. (voice/)"""
    return _run_module(
        "voice",
        text=text,
        speaker_wav=speaker_wav,
        voice_preset=voice_preset,
        language=language,
        output=output,
    )


@mcp.tool()
def generate_audio(prompt: str, duration_seconds: int = 10, output: str = "out.wav") -> dict:
    """Generate music/sound-effect audio from a text prompt. (audio-gen/)"""
    return _run_module(
        "audio-gen", prompt=prompt, duration_seconds=duration_seconds, output=output
    )


@mcp.tool()
def predict_virality(text: str) -> dict:
    """Score a script/caption for predicted virality with reasoning. (virality-predictor/)"""
    return _run_module("virality-predictor", text=text)


@mcp.tool()
def generate_avatar_video(
    prompt: str,
    speaker_wav: str = None,
    voice_preset: str = "default",
    face_image_path: str = None,
    avatar_prompt: str = None,
    language: str = "en",
    output: str = "final_video.mp4",
) -> dict:
    """Main use case: prompt -> finished avatar video. Pass face_image_path/speaker_wav
    for your own avatar+voice, or omit both to auto-generate an avatar (image-gen) and
    use a preset voice (voice_preset). Runs the full llm -> voice -> lipsync-avatar ->
    upscale pipeline. (pipeline.py)"""
    pipeline_dir = AI_LAB_DIR
    sys.path.insert(0, str(pipeline_dir))
    try:
        spec = importlib.util.spec_from_file_location("ai_lab_pipeline", pipeline_dir / "pipeline.py")
        pipeline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pipeline)
        kwargs = {
            "prompt": prompt,
            "speaker_wav": speaker_wav,
            "voice_preset": voice_preset,
            "face_image_path": face_image_path,
            "language": language,
            "output": output,
        }
        if avatar_prompt is not None:
            kwargs["avatar_prompt"] = avatar_prompt
        output_path = pipeline.generate_video(**kwargs)
        return {"output_path": output_path, "metadata": {}}
    finally:
        sys.path.remove(str(pipeline_dir))


if __name__ == "__main__":
    mcp.run(transport="stdio")
