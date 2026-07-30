"""Adapts the cloned-voice speaker profile on the user's own longer sample set.

data_dir must contain one or more .wav files of the same speaker (a handful of
30s+ clips gives noticeably higher fidelity than the single ~10s clip XTTS-v2
needs for plain zero-shot cloning). The averaged conditioning latents are
cached so serve.py doesn't need a reference clip on every call.
"""
import argparse
import glob
import os
from pathlib import Path

import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def main(data_dir: str, output_dir: str):
    config = XttsConfig()
    config.load_json(str(BASE_MODEL_DIR / "config.json"))
    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir=str(BASE_MODEL_DIR), eval=True)

    wav_paths = sorted(glob.glob(os.path.join(data_dir, "*.wav")))
    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=wav_paths)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    torch.save((gpt_cond_latent, speaker_embedding), output_path / "speaker_latents.pth")
    print(f"Saved speaker latents from {len(wav_paths)} clips to {output_path / 'speaker_latents.pth'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
