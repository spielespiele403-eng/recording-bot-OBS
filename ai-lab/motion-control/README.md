# motion-control/ — Bewegungsübertragung

Ersetzt: Higgsfield's `motion_control` (Recast/Puppeteer). Nimmt ein Referenzfoto (Person/Charakter) und ein Treiber-Video entgegen und überträgt die Bewegung/Pose aus dem Video auf die Person im Foto.

## Basismodell

**MagicAnimate** (GitHub: [magic-research/magic-animate](https://github.com/magic-research/magic-animate), Gewichte auf Hugging Face: [zcxu-eric/MagicAnimate](https://huggingface.co/zcxu-eric/MagicAnimate)) — Appearance-Encoder + Pose-ControlNet + zeitlich konsistentes Diffusion-UNet auf Basis von Stable Diffusion 1.5. Gewählt statt einer einfacheren DensePose/OpenPose-Warping-Pipeline, weil MagicAnimate deutlich konsistentere Ergebnisse über längere Sequenzen liefert (temporale Attention statt reinem Frame-für-Frame-Warping).

MagicAnimate ist kein pip-Paket — `download_base_model.py` klont das Repo direkt nach `./checkpoints/magicanimate_repo/` und lädt die Gewichte (inkl. SD-1.5-Basis und `sd-vae-ft-mse`) separat via `huggingface_hub` herunter. Pose-Extraktion aus dem Treiber-Video läuft über `controlnet_aux`'s `OpenposeDetector` (DWPose-Nachfolgemodelle sind alternativ einsetzbar, im Code nicht aktiviert).

**Hinweis:** Es handelt sich um ein aktives Forschungsrepo ohne stabile API — falls sich die Modul-/Klassennamen in einem neueren Commit geändert haben, müssen die Importe in `finetune.py`/`serve.py` entsprechend angepasst werden.

## Hardware

- Disk: ~10 GB (MagicAnimate-Gewichte + SD-1.5-Basis + VAE)
- **VRAM: mindestens 16 GB für Inferenz**, empfohlen 24 GB für längere Clips. CPU-only ist nicht praktikabel (Minuten statt Sekunden pro Frame, mehrstündige Laufzeiten).
- Fine-Tuning (LoRA, r=16 auf UNet-Attention): ~20 GB VRAM, auf einer RTX 4090 bei einer Handvoll Referenzbild/Treiber-Video-Paaren ca. 1-2 Stunden für 10 Epochen.

## Lizenz-Hinweise

MagicAnimate wird unter einer **Forschungs-/Non-Commercial-orientierten Lizenz** veröffentlicht (siehe LICENSE im Repo) und baut auf Stable Diffusion 1.5 (CreativeML OpenRAIL-M, mit Nutzungsbeschränkungen) auf. **Videomodelle wie dieses sind tendenziell strenger lizenziert als Bild-/Textmodelle** — für rein privaten, nicht-kommerziellen Gebrauch unkritisch, vor jeglicher kommerzieller Nutzung unbedingt die aktuelle Lizenz beider Repos (magic-animate + SD 1.5) prüfen.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_pairs --output_dir ./checkpoints/finetuned/
python serve.py --reference_image_path ./me.png --driving_video_path ./dance.mp4 --output out.mp4
```

Programmatisch:

```python
from serve import run
result = run(reference_image_path="./me.png", driving_video_path="./dance.mp4")
print(result["output_path"])
```
