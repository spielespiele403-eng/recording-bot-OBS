# image-gen/ — Text-zu-Bild

Ersetzt: Higgsfield's `generate_image`. Erzeugt aus einem Text-Prompt ein Bild in frei wählbarer Auflösung.

## Basismodell

`stabilityai/stable-diffusion-xl-base-1.0` (Hugging Face: [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)) — Stable Diffusion XL, OpenRAIL++-M-Lizenz.

## Hardware

- Disk: ~7 GB (fp16 Safetensors)
- VRAM: ~8-10 GB für Inferenz in fp16 bei 1024x1024
- Fine-Tuning (LoRA, r=16, DreamBooth-Style auf 10-30 eigenen Bildern): ~10-14 GB VRAM, auf einer RTX 3090/4090 ca. 15-30 Minuten für 20 Epochen

## Lizenz-Hinweise

CreativeML Open RAIL++-M: kommerzielle Nutzung erlaubt, mit Nutzungsbeschränkungen (kein Einsatz zur Erzeugung illegaler/schädlicher Inhalte, siehe Lizenztext). Erzeugte Bilder gehören dem Nutzer.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_style --output_dir ./checkpoints/finetuned/
python serve.py --prompt "a cinematic portrait of a lighthouse at sunset" --output out.png
```

Programmatisch:

```python
from serve import run
result = run(prompt="a cinematic portrait of a lighthouse at sunset", width=1024, height=1024)
print(result["output_path"])
```
