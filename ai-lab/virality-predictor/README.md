# virality-predictor/ — Virality Predictor

Ersetzt: Higgsfield's `virality_predictor`. Nimmt ein Skript/Transkript (+ optional Basis-Metadaten wie Videolänge/Plattform) entgegen und gibt einen Virality-Score (0-100) mit kurzer Begründung zurück.

Anders als die übrigen Module wird hier kein generatives Modell verwendet, sondern ein kleiner Encoder mit einem selbst trainierten Regressions-Kopf (LoRA) — trainiert auf Engagement-Daten, die der Nutzer selbst sammelt (z.B. eigene View-/Like-/Watchtime-Historie als CSV). Ohne eigenes Fine-Tuning liefert das Modul nur unbrauchbare/zufällige Scores, da der Regressions-Kopf initial nicht trainiert ist.

## Basismodell

`distilbert-base-uncased` (Hugging Face: [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased)) — Apache-2.0-Lizenz, keine Einschränkungen.

## Hardware

- Disk: ~270 MB
- VRAM: <1 GB für Inferenz, läuft problemlos auf CPU
- Fine-Tuning (LoRA, r=8): <2 GB VRAM, auf jeder Consumer-GPU (auch CPU möglich) bei ein paar hundert bis tausend Beispielen ca. 5-10 Minuten für 10 Epochen

## Lizenz-Hinweise

DistilBERT (Apache 2.0) — uneingeschränkte kommerzielle Nutzung. Qualität hängt vollständig von der Menge/Güte der eigenen Trainingsdaten (Engagement-CSV) ab, nicht vom Basismodell.

## Trainingsdaten-Format (`finetune.py --data_dir`)

CSV-Dateien mit Spalten `text,engagement_score` (Score vom Nutzer vorab auf ca. 0-100 skaliert).

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_engagement.csv --output_dir ./checkpoints/finetuned/
python serve.py --text "You won't believe what happened next..." --platform tiktok --output out.json
```

Programmatisch:

```python
from serve import run
result = run(text="You won't believe what happened next...", platform="tiktok")
print(result["metadata"]["virality_score"], result["metadata"]["reasoning"])
```
