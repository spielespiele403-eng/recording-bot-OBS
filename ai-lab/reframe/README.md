# reframe/ — Seitenverhältnis ändern

Ersetzt: Higgsfield's `reframe`. Bringt ein Bild auf ein Ziel-Seitenverhältnis (z.B. `9:16` für Shorts, `16:9` für Querformat). Erkennt per Gesichtserkennung die wichtige Bildregion; passt das Zielformat per zentriertem Zuschnitt hinein, wird die erkannte Region angeschnitten, wird stattdessen die Leinwand über `../outpaint/` erweitert statt Inhalt zu verlieren.

## Basismodell

Kein eigenes. Smart-Crop nutzt den in `opencv-python` mitgelieferten, nicht trainierbaren Haar-Cascade-Gesichtsdetektor (`haarcascade_frontalface_default.xml`). Die Erweiterungs-Fälle rufen `../outpaint/serve.py`'s `run()` auf und nutzen dessen Modell (SDXL Inpainting).

## Hardware

- Disk/VRAM: keine eigenen — nur `opencv-python` (CPU) für die Erkennung; im Erweiterungsfall gelten die Hardware-Anforderungen von `../outpaint/`
- Fine-Tuning: kein eigenes Modul-Modell zum Feintunen (siehe `finetune.py`); Qualität der Erweiterung verbessert sich durch Fine-Tuning von `../outpaint/`

## Lizenz-Hinweise

`opencv-python` ist Apache-2.0. Für die Erweiterungs-Fälle gelten die Lizenzbedingungen von `../outpaint/` (SDXL Inpainting, OpenRAIL++-M).

## Verwendung

```bash
python download_base_model.py
python serve.py --image_path portrait.png --target_aspect_ratio 9:16 --output out.png
```

Programmatisch:

```python
from serve import run
result = run(image_path="portrait.png", target_aspect_ratio="9:16", output="out.png")
print(result["metadata"]["method"])  # "crop" oder "outpaint"
```
