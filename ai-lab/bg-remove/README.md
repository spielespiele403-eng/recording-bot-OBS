# bg-remove/ — Hintergrund entfernen

Ersetzt: Higgsfield's `remove_background`. Entfernt den Hintergrund eines Bildes und liefert ein transparentes PNG (Cutout des Vordergrund-Objekts).

## Basismodell

`facebook/sam-vit-base` (Hugging Face: [facebook/sam-vit-base](https://huggingface.co/facebook/sam-vit-base)) — Meta's Segment Anything Model (SAM), ViT-B-Encoder-Variante, Apache-2.0-Lizenz. Wird per Punkt-Prompt (standardmäßig Bildmitte) zur Vordergrund-Maske geführt.

**Leichtgewichtige Alternative:** das `rembg`-Paket (U^2-Net-Modell, ~176 MB, MIT-Lizenz) läuft ganz ohne Prompt und ist deutlich schneller/genügsamer als SAM, dafür weniger steuerbar (kein Punkt-/Box-Prompt, kein Fine-Tuning auf eigene Objektklassen). Für einfache Portrait-/Produkt-Cutouts ohne GPU eine gute Alternative: `pip install rembg` und `rembg.remove(...)`.

## Hardware

- Disk: ~375 MB (ViT-B-Encoder + Decoder)
- VRAM: ~2-3 GB für Inferenz, läuft auch auf CPU (langsamer, aber machbar, da der Encoder klein ist)
- Fine-Tuning (nur Decoder-Head, Encoder + Prompt-Encoder eingefroren): ~4-6 GB VRAM, auf einer RTX 3060 bei ein paar hundert Bild/Maske-Paaren ca. 10-20 Minuten für 10 Epochen

## Lizenz-Hinweise

SAM steht unter Apache 2.0 — uneingeschränkte kommerzielle Nutzung, keine Gating-Zustimmung nötig.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_masks --output_dir ./checkpoints/finetuned/
python serve.py --image_path photo.jpg --output out.png
```

Programmatisch:

```python
from serve import run
result = run(image_path="photo.jpg", output="out.png")
print(result["metadata"])
```
