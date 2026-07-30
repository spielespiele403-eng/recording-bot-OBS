# Stimm-Presets

Für den Modus "System erstellt eigene Stimme" (kein eigenes `speaker_wav` angegeben) wird eine Referenz-Audiodatei aus dieser Registry (`presets.json`) verwendet, statt eine eigene Stimme zu klonen.

`presets.json` bildet einen Preset-Namen auf eine `.wav`-Datei (10-20s, klare Sprachaufnahme, 24kHz) und eine Beschreibung ab. Die `.wav`-Dateien selbst liegen nicht im Repo (Audiodaten, keine Codebasis) — leg eigene Referenzclips hier ab oder nutze eine frei lizenzierte Sprachaufnahme (z.B. LibriTTS/VCTK-Ausschnitte, Lizenz prüfen) und trage sie in `presets.json` ein:

```json
{
  "default": {"wav": "presets/default.wav", "description": "Neutraler Standard-Sprecher"},
  "warm-female": {"wav": "presets/warm_female.wav", "description": "Warme weibliche Stimme"}
}
```

`voice/serve.py` löst `voice_preset` über diese Datei auf, wenn kein `speaker_wav` übergeben wird.
