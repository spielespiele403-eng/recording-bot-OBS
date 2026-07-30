# upscale/ — Bild- & Video-Upscaling

Ersetzt: Higgsfield's `upscale_image`/`upscale_video`. Erhöht die Auflösung eines Bildes oder eines Videos (Frame für Frame) um den angegebenen Faktor. Die Eingabeart (Bild vs. Video) wird automatisch anhand der Dateiendung erkannt.

## Basismodell

Real-ESRGAN, Gewicht `RealESRGAN_x4plus` (GitHub-Release: [xinntao/Real-ESRGAN v0.1.0](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.1.0), Python-Paket `realesrgan` + `basicsr`).

## Hardware

- Disk: ~65 MB
- VRAM: ~2-4 GB für Bild-Inferenz bei 4x; Video-Upscaling ist pro Frame genauso teuer wie ein Einzelbild, Gesamtzeit skaliert mit der Frameanzahl (läuft auf CPU, aber deutlich langsamer)
- Fine-Tuning (nur Upsampling-Kopf, auf eigenen Hi-Res-Bildern): ~4-6 GB VRAM, auf einer RTX 3060/3090 bei einigen Dutzend Bildern ca. 10-20 Minuten für 20 Epochen

## Lizenz-Hinweise

Real-ESRGAN steht unter BSD-3-Clause — uneingeschränkte kommerzielle Nutzung.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_photos --output_dir ./checkpoints/finetuned/
python serve.py --input_path photo.jpg --scale 4 --output out.png
python serve.py --input_path clip.mp4 --scale 2 --output out.mp4
```

Programmatisch:

```python
from serve import run
result = run(input_path="clip.mp4", scale=2, output="out.mp4")
print(result["metadata"])
```
