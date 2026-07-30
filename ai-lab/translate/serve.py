"""Translates a script/transcript into a target language.

If `segments` (a list of {"start", "end", "text"} dicts) is passed instead of
a single blob of `text`, each segment is translated individually and its
timing is preserved in the output JSON.
"""
import argparse
import json
from pathlib import Path

from peft import PeftModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
ADAPTER_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_tokenizer = None


def _load():
    global _model, _tokenizer
    if _model is not None:
        return
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR)
    _model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_DIR)
    if ADAPTER_DIR.exists():
        _model = PeftModel.from_pretrained(_model, ADAPTER_DIR)


def _translate_one(text: str, target_lang: str) -> str:
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    forced_bos_token_id = _tokenizer.convert_tokens_to_ids(target_lang)
    output_ids = _model.generate(
        **inputs, forced_bos_token_id=forced_bos_token_id, max_new_tokens=512
    )
    return _tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()


def run(
    text: str = "",
    target_lang: str = "deu_Latn",
    segments: list | None = None,
    output: str = "./output.json",
    **kwargs,
) -> dict:
    _load()
    output_path = Path(output)

    if segments:
        translated_segments = [
            {**seg, "text": _translate_one(seg["text"], target_lang)} for seg in segments
        ]
        translated_text = " ".join(seg["text"] for seg in translated_segments)
        output_path.write_text(
            json.dumps({"segments": translated_segments}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        metadata = {"translated_text": translated_text, "segments": translated_segments}
    else:
        translated_text = _translate_one(text, target_lang)
        output_path.write_text(translated_text, encoding="utf-8")
        metadata = {"translated_text": translated_text}

    metadata["target_lang"] = target_lang
    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    parser.add_argument("--target_lang", default="deu_Latn")
    parser.add_argument("--output", default="./output.txt")
    args = parser.parse_args()
    result = run(text=args.text, target_lang=args.target_lang, output=args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))
