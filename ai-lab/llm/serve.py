"""Generates a full spoken-video script from a short prompt."""
import argparse
import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_tokenizer = None


def _load():
    global _model, _tokenizer
    if _model is not None:
        return
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    _model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_DIR, torch_dtype=torch.float16, device_map="auto"
    )
    if ADAPTER_DIR.exists():
        _model = PeftModel.from_pretrained(_model, ADAPTER_DIR)


def run(prompt: str, max_length: int = 300, output: str = "./output.txt", **kwargs) -> dict:
    _load()
    messages = [
        {
            "role": "user",
            "content": (
                f"Write a natural, spoken video script (a few paragraphs, no stage "
                f"directions) about: {prompt}"
            ),
        }
    ]
    inputs = _tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(_model.device)
    output_ids = _model.generate(
        inputs, max_new_tokens=max_length, do_sample=True, temperature=0.8
    )
    script = _tokenizer.decode(
        output_ids[0][inputs.shape[-1] :], skip_special_tokens=True
    ).strip()

    output_path = Path(output)
    output_path.write_text(script, encoding="utf-8")

    return {
        "output_path": str(output_path),
        "metadata": {"script": script, "prompt": prompt},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--max_length", type=int, default=300)
    parser.add_argument("--output", default="./output.txt")
    args = parser.parse_args()
    result = run(prompt=args.prompt, max_length=args.max_length, output=args.output)
    print(json.dumps(result, indent=2))
