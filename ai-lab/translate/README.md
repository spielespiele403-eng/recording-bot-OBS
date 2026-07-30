# translate/ — Video-Übersetzung

Ersetzt: HeyGen's "Video Translate". Übersetzt ein Skript/Transkript in eine Zielsprache; wenn das Transkript als Segmente mit Zeitstempeln (`start`/`end`/`text`) übergeben wird, bleibt die satzweise Timing-Info in der Ausgabe erhalten (wichtig für spätere Lippensynchronisation/Untertitel).

## Basismodell

`facebook/nllb-200-distilled-600M` (Hugging Face: [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)) — Meta's No Language Left Behind, 200 Sprachen, CC-BY-NC-4.0-Lizenz.

Zielsprachen werden als FLORES-200-Codes angegeben, z.B. `deu_Latn` (Deutsch), `eng_Latn` (Englisch), `fra_Latn` (Französisch).

## Hardware

- Disk: ~2.5 GB
- VRAM: ~2-3 GB für Inferenz, läuft auch auf CPU (langsamer)
- Fine-Tuning (LoRA, r=16): ~4-6 GB VRAM, auf einer RTX 3060/3090 bei ein paar tausend Satzpaaren ca. 15-25 Minuten für 5 Epochen

## Lizenz-Hinweise

NLLB-200 steht unter **CC-BY-NC-4.0 — nicht-kommerzielle Nutzung**. Für ein rein privates/nicht-kommerzielles Setup unkritisch; bei kommerzieller Nutzung des Gesamtsystems muss dieses Modul gegen ein Modell mit passender Lizenz getauscht werden (z.B. `facebook/m2m100_418M`, ebenfalls CC-BY-NC, oder ein MIT/Apache-lizenziertes Alternativmodell).

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_pairs --src_lang eng_Latn --tgt_lang deu_Latn
python serve.py --text "Hello, welcome to my channel." --target_lang deu_Latn --output out.txt
```

Programmatisch (mit Zeitstempeln):

```python
from serve import run
result = run(segments=[{"start": 0.0, "end": 2.1, "text": "Hello, welcome to my channel."}],
             target_lang="deu_Latn")
print(result["metadata"]["translated_text"])
```
