# audio-gen/ — Musik-/Sound-Generierung

Ersetzt: Higgsfield's `generate_audio`. Erzeugt Musik/Sound-Clips aus einem Text-Prompt.

## Basismodell

**MusicGen** (`facebook/musicgen-medium`, Hugging Face: [facebook/musicgen-medium](https://huggingface.co/facebook/musicgen-medium), ladbar via `transformers` oder [`audiocraft`](https://github.com/facebookresearch/audiocraft)) — text-gesteuerte Musikgenerierung von Meta AI.

## Hardware

- Disk: ~6 GB
- VRAM: ~8-10 GB für Inferenz (medium), läuft auch auf CPU (sehr langsam)
- Fine-Tuning (LoRA, r=16): ~10-14 GB VRAM, auf einer RTX 3090 bei ein paar Dutzend Prompt/Audio-Paaren ca. 20-40 Minuten für 10 Epochen

## Lizenz-Hinweise

MusicGen-Gewichte stehen unter **CC-BY-NC-4.0 — nicht-kommerzielle Nutzung**. Für privates Setup unkritisch; bei kommerzieller Nutzung des Gesamtsystems muss dieses Modul gegen ein Modell mit passender Lizenz getauscht werden. Erzeugte Musik kann bestehendem Trainingsmaterial ähneln — vor Veröffentlichung prüfen.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_music_pairs --output_dir ./checkpoints/finetuned/
python serve.py --prompt "upbeat lo-fi hip hop with soft piano" --duration_seconds 15 --output out.wav
```

Programmatisch:

```python
from serve import run
result = run(prompt="tense orchestral build-up", duration_seconds=20, output="out.wav")
print(result["output_path"])
```
