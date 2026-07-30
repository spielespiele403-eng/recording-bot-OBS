"""LoRA fine-tunes MusicGen on the user's own (prompt, audio) pairs.

data_dir must contain matching pairs: name.wav + name.txt, where name.txt
holds the text prompt describing name.wav.
"""
import argparse
import glob
import os
from pathlib import Path

import torch
import torchaudio
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoProcessor, MusicgenForConditionalGeneration, Trainer, TrainingArguments

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def load_pairs(data_dir: str):
    prompts, wav_paths = [], []
    for wav_path in sorted(glob.glob(os.path.join(data_dir, "*.wav"))):
        txt_path = os.path.splitext(wav_path)[0] + ".txt"
        with open(txt_path, encoding="utf-8") as f:
            prompts.append(f.read().strip())
        wav_paths.append(wav_path)
    return prompts, wav_paths


def main(data_dir: str, output_dir: str):
    processor = AutoProcessor.from_pretrained(BASE_MODEL_DIR)
    model = MusicgenForConditionalGeneration.from_pretrained(BASE_MODEL_DIR)
    sample_rate = model.config.audio_encoder.sampling_rate

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["k_proj", "v_proj", "q_proj", "out_proj"],
        lora_dropout=0.05,
        bias="none",
    )
    model = get_peft_model(model, lora_config)

    prompts, wav_paths = load_pairs(data_dir)

    def encode(example):
        wav, sr = torchaudio.load(example["wav_path"])
        wav = torchaudio.functional.resample(wav, sr, sample_rate).mean(dim=0, keepdim=True)
        with torch.no_grad():
            audio_codes = model.get_base_model().audio_encoder.encode(wav.unsqueeze(0))["audio_codes"]
        inputs = processor(text=[example["prompt"]], padding=True, return_tensors="pt")
        return {
            "input_ids": inputs["input_ids"][0],
            "attention_mask": inputs["attention_mask"][0],
            "labels": audio_codes[0, 0].transpose(0, 1),
        }

    dataset = Dataset.from_dict({"prompt": prompts, "wav_path": wav_paths})
    dataset = dataset.map(encode, remove_columns=["prompt", "wav_path"])

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=10,
        per_device_train_batch_size=1,
        learning_rate=1e-4,
        logging_steps=5,
        save_strategy="no",
        report_to=[],
    )
    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
    trainer.train()

    model.save_pretrained(output_dir)
    processor.save_pretrained(output_dir)
    print(f"Saved LoRA adapter to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
