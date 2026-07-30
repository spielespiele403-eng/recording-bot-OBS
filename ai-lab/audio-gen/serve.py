"""Text-prompted music/sound generation via MusicGen."""
import argparse
import json
from pathlib import Path

import torch
import torchaudio
from peft import PeftModel
from transformers import AutoProcessor, MusicgenForConditionalGeneration

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_processor = None


def _load():
    global _model, _processor
    if _model is not None:
        return
    _processor = AutoProcessor.from_pretrained(BASE_MODEL_DIR)
    _model = MusicgenForConditionalGeneration.from_pretrained(BASE_MODEL_DIR)
    if ADAPTER_DIR.exists():
        _model = PeftModel.from_pretrained(_model, ADAPTER_DIR)
    if torch.cuda.is_available():
        _model.cuda()


def run(prompt: str, duration_seconds: int = 10, output: str = "out.wav", **kwargs) -> dict:
    _load()
    inputs = _processor(text=[prompt], padding=True, return_tensors="pt").to(_model.device)
    frame_rate = _model.config.audio_encoder.frame_rate
    max_new_tokens = int(duration_seconds * frame_rate)

    audio_values = _model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, guidance_scale=3.0)

    sample_rate = _model.config.audio_encoder.sampling_rate
    output_path = Path(output)
    torchaudio.save(str(output_path), audio_values[0].cpu(), sample_rate)

    metadata = {"prompt": prompt, "duration_seconds": duration_seconds, "sample_rate": sample_rate}
    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--duration_seconds", type=int, default=10)
    parser.add_argument("--output", default="out.wav")
    args = parser.parse_args()
    result = run(prompt=args.prompt, duration_seconds=args.duration_seconds, output=args.output)
    print(json.dumps(result, indent=2))
