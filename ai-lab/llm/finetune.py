"""LoRA fine-tunes the base LLM on the user's own script examples.

data_dir must contain one or more .txt or .jsonl files. .jsonl lines use
{"text": "..."}; .txt files are used as-is, one training example per file.
"""
import argparse
import glob
import json
import os
from pathlib import Path

from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def load_examples(data_dir: str) -> list[str]:
    examples = []
    for path in glob.glob(os.path.join(data_dir, "*.jsonl")):
        with open(path, encoding="utf-8") as f:
            examples.extend(json.loads(line)["text"] for line in f if line.strip())
    for path in glob.glob(os.path.join(data_dir, "*.txt")):
        examples.append(Path(path).read_text(encoding="utf-8"))
    return examples


def main(data_dir: str, output_dir: str):
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_DIR)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    examples = load_examples(data_dir)
    dataset = Dataset.from_dict({"text": examples})
    dataset = dataset.map(
        lambda batch: tokenizer(batch["text"], truncation=True, max_length=1024),
        batched=True,
        remove_columns=["text"],
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="no",
        report_to=[],
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
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
