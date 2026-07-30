# llm/ — Skript-Generierung

Ersetzt: Higgsfield's Skript-/Prompt-zu-Text-Schritt (der erste Schritt in Workflows wie Explainer-Video, UGC-Video, Podcast). Nimmt einen kurzen Prompt ("ein paar Worte") entgegen und erzeugt daraus ein vollständiges, natürlich klingendes Sprechtext-Skript (mehrere Absätze) für ein Video.

## Basismodell

`mistralai/Mistral-7B-Instruct-v0.2` (Hugging Face: [mistralai/Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)) — offenes, instruction-getuntes 7B-LLM, Apache-2.0-Lizenz, kein Gating, kommerzielle Nutzung erlaubt.

Alternative: `meta-llama/Meta-Llama-3-8B-Instruct` (bessere Qualität, aber gated — benötigt Zustimmung zur Meta Llama 3 Community License auf Hugging Face und ist bei rein kommerzieller Nutzung ab 700M MAU laut Lizenz gesondert zu vereinbaren).

## Hardware

- Disk: ~15 GB (fp16 Safetensors)
- VRAM: ~16 GB für Inferenz in fp16 (mit 4-bit-Quantisierung via `bitsandbytes` auch ~6 GB möglich, im Code nicht aktiviert)
- Fine-Tuning (LoRA, r=16): ~10-12 GB VRAM, auf einer RTX 3090/4090 bei wenigen hundert Beispielen ca. 20-40 Minuten für 3 Epochen

## Lizenz-Hinweise

Mistral-7B-Instruct-v0.2 steht unter Apache 2.0 — uneingeschränkte kommerzielle Nutzung. Bei Wechsel auf Llama-3-Familie: Lizenzbedingungen (gated download, Nutzungsbeschränkungen) auf Hugging Face beachten.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_scripts --output_dir ./checkpoints/finetuned/
python serve.py --prompt "ein Video über nachhaltige Ernährung" --output out.txt
```

Programmatisch:

```python
from serve import run
result = run(prompt="ein Video über nachhaltige Ernährung", max_length=300)
print(result["metadata"]["script"])
```
