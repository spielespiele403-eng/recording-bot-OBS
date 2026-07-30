"""Predicts a 0-100 virality score for a script/transcript with reasoning."""
import argparse
import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_tokenizer = None

HOOK_WORDS = ["you won't believe", "secret", "never", "always", "here's why", "watch until"]


def _load():
    global _model, _tokenizer
    if _model is not None:
        return
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    _model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL_DIR, num_labels=1, problem_type="regression"
    )
    if ADAPTER_DIR.exists():
        _model = PeftModel.from_pretrained(_model, ADAPTER_DIR)
    _model.eval()


def _reasoning(text: str, score: float) -> str:
    lower = text.lower()
    reasons = []
    if score >= 70:
        reasons.append("model predicts strong engagement")
    elif score >= 40:
        reasons.append("model predicts moderate engagement")
    else:
        reasons.append("model predicts weak engagement")
    if any(hook in lower for hook in HOOK_WORDS):
        reasons.append("contains a strong hook phrase")
    if "?" in text:
        reasons.append("uses a question to draw curiosity")
    word_count = len(text.split())
    if word_count < 30:
        reasons.append("short/punchy length suits short-form platforms")
    elif word_count > 150:
        reasons.append("longer length may hurt short-form retention")
    return "; ".join(reasons)


def run(text: str, video_length_s: float | None = None, platform: str = "", output: str = "./output.json", **kwargs) -> dict:
    _load()
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        logits = _model(**inputs).logits
    raw_score = logits.squeeze().item()
    virality_score = max(0.0, min(100.0, raw_score))
    reasoning = _reasoning(text, virality_score)

    output_path = Path(output)
    metadata = {
        "virality_score": virality_score,
        "reasoning": reasoning,
        "video_length_s": video_length_s,
        "platform": platform,
    }
    output_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--video_length_s", type=float, default=None)
    parser.add_argument("--platform", default="")
    parser.add_argument("--output", default="./output.json")
    args = parser.parse_args()
    result = run(
        text=args.text,
        video_length_s=args.video_length_s,
        platform=args.platform,
        output=args.output,
    )
    print(json.dumps(result, indent=2))
