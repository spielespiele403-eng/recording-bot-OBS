# image-to-3d/ — Bild zu 3D-Mesh

Ersetzt: Higgsfield's `generate_3d`. Rekonstruiert aus einem einzelnen Bild ein texturiertes 3D-Mesh, ausgegeben als GLB — passend zu Higgsfields GLB-Ausgabeformat.

## Basismodell

`stabilityai/TripoSR` (Hugging Face: [stabilityai/TripoSR](https://huggingface.co/stabilityai/TripoSR)) — schnelles feedforward Single-Image-to-3D-Modell von Stability AI/Tripo AI (Triplane-Transformer + NeRF-Decoder), MIT-Lizenz. Benötigt zusätzlich das `tsr`-Python-Paket aus dem [TripoSR-GitHub-Repo](https://github.com/VAST-AI-Research/TripoSR) (kein PyPI-Paket; per `pip install -r requirements.txt` aus dem geklonten Repo oder `pip install git+https://github.com/VAST-AI-Research/TripoSR`), sowie `rembg` für die Hintergrundentfernung des Eingabebilds (Teil von TripoSRs eigener Preprocessing-Pipeline).

## Hardware

- Disk: ~700 MB (Checkpoint)
- VRAM: ~6 GB für Inferenz (Rekonstruktion in unter einer Sekunde auf einer modernen GPU), läuft auch auf CPU (mehrere Sekunden bis über eine Minute)
- Fine-Tuning (nur NeRF-Decoder-Head, Bild-Tokenizer + Triplane-Backbone eingefroren): unüblich und aufwändig — TripoSR wird in der Praxis fast immer zero-shot verwendet, da echtes Fine-Tuning synthetische Multi-View-Renders pro Objektkategorie braucht (z.B. per Blender-Turntable erzeugt), keine einfachen 2D-Bild/Label-Paare wie bei anderen Modulen. Bei ein paar Dutzend Objekten mit je ~20-30 Views: grob 1-3 Stunden auf einer RTX 3090.

## Lizenz-Hinweise

TripoSR (Code und Gewichte) steht unter MIT-Lizenz — uneingeschränkte kommerzielle Nutzung.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_objects --output_dir ./checkpoints/finetuned/
python serve.py --image_path photo.jpg --output out.glb
```

Programmatisch:

```python
from serve import run
result = run(image_path="photo.jpg", output="out.glb")
print(result["metadata"])
```
