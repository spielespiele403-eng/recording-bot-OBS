"""Trains a LoRA regression head on top of DistilBERT to predict virality.

data_dir must contain one or more .csv files with columns "text" and
"engagement_score" (a number, e.g. views/likes/watch-time already scaled by
the user to roughly 0-100).
"""
import argparse
import glob
import os
from pathlib import Path

import pandas as pd
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def load_dataframe(data_dir: str) -> pd.DataFrame:
    frames = [pd.read_csv(path) for path in glob.glob(os.path.join(data_dir, "*.csv"))]
    return pd.concat(frames, ignore_index=True)


def main(data_dir: str, output_dir: str):
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL_DIR, num_labels=1, problem_type="regression"
    )

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_lin", "v_lin"],
        lora_dropout=0.05,
        bias="none",
        task_type="SEQ_CLS",
    )
    model = get_peft_model(model, lora_config)

    df = load_dataframe(data_dir)
    dataset = Dataset.from_pandas(df[["text", "engagement_score"]])
    dataset = dataset.map(
        lambda batch: tokenizer(batch["text"], truncation=True, max_length=256),
        batched=True,
    )
    dataset = dataset.rename_column("engagement_score", "labels")
    dataset = dataset.remove_columns(["text"])
    dataset.set_format(type="torch")

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=10,
        per_device_train_batch_size=16,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="no",
        report_to=[],
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorWithPadding(tokenizer),
    )
    trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved LoRA adapter to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
