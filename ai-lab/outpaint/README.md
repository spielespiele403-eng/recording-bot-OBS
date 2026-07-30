# outpaint/ — Bild erweitern

Ersetzt: Higgsfield's `outpaint_image`. Erweitert die Leinwand eines Bildes in eine oder alle Richtungen (`left`/`right`/`top`/`bottom`/`all`) und füllt den neuen Rand per Inpainting mit passendem Bildinhalt.

## Basismodell

`diffusers/stable-diffusion-xl-1.0-inpainting-0.1` (Hugging Face: [diffusers/stable-diffusion-xl-1.0-inpainting-0.1](https://huggingface.co/diffusers/stable-diffusion-xl-1.0-inpainting-0.1)) — SDXL-Inpainting-Variante, OpenRAIL++-M-Lizenz.

## Hardware

- Disk: ~7 GB (fp16 Safetensors)
- VRAM: ~8-10 GB für Inferenz in fp16
- Fine-Tuning (LoRA, r=16, Stil-Anpassung auf eigenen Bildern): ~10-14 GB VRAM, auf einer RTX 3090/4090 ca. 15-30 Minuten für 20 Epochen

## Lizenz-Hinweise

CreativeML Open RAIL++-M: kommerzielle Nutzung erlaubt, mit Nutzungsbeschränkungen laut Lizenztext.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_style --output_dir ./checkpoints/finetuned/
python serve.py --image_path portrait.png --direction all --expand_px 256 --output out.png
```

Programmatisch:

```python
from serve import run
result = run(image_path="portrait.png", direction="left", expand_px=300, output="out.png")
print(result["metadata"])
```
