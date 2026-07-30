# ai-lab MCP Server

Exposes all 14 ai-lab modules as MCP tools. Runs entirely locally on your own
hardware — no cloud API calls, no per-generation cost, unlike HeyGen/Higgsfield.

Each tool dynamically imports the matching sibling module's `serve.py` at
call time and invokes its `run(**kwargs)`, returning
`{"output_path": str, "metadata": {...}}`.

## Setup

```bash
pip install mcp
```

## Add to Claude Code (`.mcp.json`)

```json
{
  "mcpServers": {
    "ai-lab": {
      "command": "python",
      "args": ["/absolute/path/to/ai-lab/mcp-server/server.py"]
    }
  }
}
```

## Tools

| Tool | Module | Parameters |
|---|---|---|
| `write_script` | `llm/` | `prompt: str`, `max_length: int = 300` |
| `translate_script` | `translate/` | `text: str`, `target_lang: str` |
| `generate_image` | `image-gen/` | `prompt: str`, `output: str = "out.png"`, `width: int = 1024`, `height: int = 1024` |
| `outpaint_image` | `outpaint/` | `image_path: str`, `direction: str`, `expand_px: int`, `output: str = "out.png"` |
| `reframe` | `reframe/` | `image_path: str`, `target_aspect_ratio: str`, `output: str = "out.png"` |
| `upscale_media` | `upscale/` | `input_path: str`, `scale: int = 4`, `output: str = "out.png"`, `media_type: str = "image"` (routing hint, works for image or video) |
| `remove_background` | `bg-remove/` | `image_path: str`, `output: str = "out.png"` |
| `generate_3d` | `image-to-3d/` | `image_path: str`, `output: str = "out.glb"` |
| `generate_video` | `video-gen/` | `image_path: str`, `output: str = "out.mp4"`, `num_frames: int = 25` |
| `motion_control` | `motion-control/` | `reference_image_path: str`, `driving_video_path: str`, `output: str = "out.mp4"` |
| `lipsync_avatar` | `lipsync-avatar/` | `face_image_or_video_path: str`, `audio_path: str`, `mode: str = "wav2lip"`, `output: str = "out.mp4"` |
| `generate_speech` | `voice/` | `text: str`, `speaker_wav: str`, `language: str = "en"`, `output: str = "out.wav"` |
| `generate_audio` | `audio-gen/` | `prompt: str`, `duration_seconds: int = 10`, `output: str = "out.wav"` |
| `predict_virality` | `virality-predictor/` | `text: str` |

## Notes

- All models load and run on-device (GPU recommended); nothing is sent to a
  third-party API.
- Tools return the module's raw result dict — `output_path` points at the
  generated file on local disk, `metadata` carries generation-specific info
  (e.g. `metadata["script"]`, `metadata["virality_score"]`).
