"""LoRA fine-tunes NLLB on the user's own parallel sentence pairs.

data_dir must contain one or more .jsonl files with lines like
{"src_text": "...", "tgt_text": "..."}. All pairs use the same
src_lang/tgt_lang, given via --src_lang/--tgt_lang (NLLB FLORES-200 codes,
e.g. "eng_Latn", "deu_Latn").
"""
import argparse
import glob
import json
import os
from pathlib import Path

from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def load_pairs(data_dir: str) -> tuple[list[str], list[str]]:
    src_texts, tgt_texts = [], []
    for path in glob.glob(os.path.join(data_dir, "*.jsonl")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                src_texts.append(row["src_text"])
                tgt_texts.append(row["tgt_text"])
    return src_texts, tgt_texts


def main(data_dir: str, output_dir: str, src_lang: str, tgt_lang: str):
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_DIR, src_lang=src_lang, tgt_lang=tgt_lang
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_DIR)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="SEQ_2_SEQ_LM",
    )
    model = get_peft_model(model, lora_config)

    src_texts, tgt_texts = load_pairs(data_dir)
    dataset = Dataset.from_dict({"src_text": src_texts, "tgt_text": tgt_texts})
    dataset = dataset.map(
        lambda batch: tokenizer(
            batch["src_text"], text_target=batch["tgt_text"], truncation=True, max_length=256
        ),
        batched=True,
        remove_columns=["src_text", "tgt_text"],
    )

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        num_train_epochs=5,
        per_device_train_batch_size=8,
        learning_rate=1e-4,
        logging_steps=10,
        save_strategy="no",
        report_to=[],
    )
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )
    trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved LoRA adapter to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    parser.add_argument("--src_lang", default="eng_Latn")
    parser.add_argument("--tgt_lang", default="deu_Latn")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir, args.src_lang, args.tgt_lang)
