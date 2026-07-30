"""Zero-shot voice cloning / multilingual TTS via XTTS-v2.

Also covers Higgsfield's voice_change: to convert an existing recording into
the cloned voice instead of synthesizing new text, call
`_model.voice_conversion(source_wav=..., target_wav=speaker_wav)` on the
loaded Xtts instance in place of the text-conditioned inference below.
"""
import argparse
import json
from pathlib import Path

import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
FINETUNED_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None


def _load():
    global _model
    if _model is not None:
        return
    config = XttsConfig()
    config.load_json(str(BASE_MODEL_DIR / "config.json"))
    _model = Xtts.init_from_config(config)
    _model.load_checkpoint(config, checkpoint_dir=str(BASE_MODEL_DIR), eval=True)
    if torch.cuda.is_available():
        _model.cuda()


def run(text: str, speaker_wav: str, language: str = "en", output: str = "out.wav", **kwargs) -> dict:
    _load()
    latents_path = FINETUNED_DIR / "speaker_latents.pth"
    if latents_path.exists():
        gpt_cond_latent, speaker_embedding = torch.load(latents_path)
    else:
        gpt_cond_latent, speaker_embedding = _model.get_conditioning_latents(audio_path=[speaker_wav])

    result = _model.inference(text, language, gpt_cond_latent, speaker_embedding)

    output_path = Path(output)
    torchaudio.save(str(output_path), torch.tensor(result["wav"]).unsqueeze(0), 24000)

    metadata = {
        "language": language,
        "speaker_wav": speaker_wav,
        "used_finetuned_speaker": latents_path.exists(),
    }
    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker_wav", required=True)
    parser.add_argument("--language", default="en")
    parser.add_argument("--output", default="out.wav")
    args = parser.parse_args()
    result = run(text=args.text, speaker_wav=args.speaker_wav, language=args.language, output=args.output)
    print(json.dumps(result, indent=2))
