# voice/ — Voice Cloning, Voice Change, Dubbing

Ersetzt: HeyGen's Voice Cloning sowie Higgsfield's `voice_change` und `dubbing`. Erzeugt Sprachausgabe in einer geklonten Stimme aus nur ~10 Sekunden Referenzaudio, mehrsprachig. Für Dubbing: Text zuerst mit `translate/` in die Zielsprache übersetzen, dann hier mit derselben geklonten Stimme in dieser Sprache synthetisieren. Dieses Modul liefert die Audiospur für den Hauptanwendungsfall (Prompt → fertiges Video in der eigenen Stimme).

## Basismodell

Coqui **XTTS-v2** (Hugging Face: [coqui/XTTS-v2](https://huggingface.co/coqui/XTTS-v2), Python-Paket [`TTS`](https://github.com/coqui-ai/TTS)) — Zero-Shot Voice Cloning aus kurzer Referenzaudio, 17 Sprachen, unterstützt zusätzlich Voice-Conversion-Modus (bestehende Aufnahme in eine Zielstimme umwandeln, siehe `serve.py`-Docstring für `voice_change`).

## Hardware

- Disk: ~2 GB (Checkpoint)
- VRAM: ~4-6 GB für Inferenz, läuft auch auf CPU (deutlich langsamer, mehrere Sekunden pro Satz)
- "Fine-Tuning" hier ist kein Gradienten-Training, sondern das Cachen gemittelter Sprecher-Konditionierungslatents aus mehreren längeren Referenzclips (statt nur einem 10s-Clip) — dauert nur Sekunden bis wenige Minuten je nach Anzahl der Clips, kein GPU-Training nötig

## Lizenz-Hinweise

XTTS-v2 steht unter der **Coqui Public Model License (CPML)** — nicht-kommerzielle Nutzung frei, kommerzielle Nutzung erfordert eine Lizenz von Coqui. Für privates Voice Cloning unkritisch; vor kommerziellem Einsatz Lizenzbedingungen prüfen. Stimm-Cloning nur mit Einwilligung der jeweiligen Person verwenden.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_voice_clips --output_dir ./checkpoints/finetuned/
python serve.py --text "Hello, welcome to my channel." --speaker_wav ./ref.wav --language en --output out.wav
```

Programmatisch:

```python
from serve import run
result = run(text="Willkommen zurück!", speaker_wav="./ref.wav", language="de", output="out.wav")
print(result["output_path"])
```

Für Dubbing: Text vorher mit `translate/serve.py` übersetzen, das Ergebnis als `text` hier einsetzen und `language` auf den FLORES/XTTS-Sprachcode der Zielsprache setzen.
