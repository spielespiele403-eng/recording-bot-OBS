# ai-lab — Eigenes, kostenloses HeyGen + Higgsfield

Selbst gehostetes System, das die Kernfähigkeiten von HeyGen (KI-Avatare, Voice Cloning, Video-Übersetzung) und Higgsfield (Bild-/Video-/Audio-Generierung, Upscaling, Background Removal, Motion Control, Virality Prediction) nachbildet — ohne Abo, auf eigener Hardware.

Kein von-Grund-auf-Training: jedes Modul lädt ein starkes offenes, bereits vortrainiertes Basismodell (z.B. Stable Diffusion XL, Wav2Lip, XTTS, MusicGen) und feintunt es bei Bedarf auf eigene Daten (LoRA/Adapter). Das ist der einzige realistische Weg, in kurzer Zeit nahe an kommerzielle Qualität zu kommen, ohne die Trainingsinfrastruktur eines KI-Unternehmens.

Losgelöst vom Twitch/OBS-Bot in diesem Repo (`bot.py`) — eigenständiges Projekt.

## Hauptanwendungsfall

**Prompt → fertiges Video mit Avatar + Stimme**, in zwei wählbaren Modi (`pipeline.py` bzw. MCP-Tool `generate_avatar_video`):

```
Prompt
  → llm/            (Skript schreiben)
  → [image-gen/      (nur falls kein eigenes Foto: Avatar automatisch generieren)]
  → voice/           (Audio: eigene geklonte Stimme ODER Preset-Stimme)
  → lipsync-avatar/  (sprechender Avatar aus Foto/Video)
  → upscale/         (Endpolitur)
  → fertiges Video
```

- **Eigener Avatar/eigene Stimme**: `face_image_path` (eigenes Foto) + `speaker_wav` (eigene Stimmprobe) angeben
- **Automatisch generierter Avatar/Preset-Stimme**: beides weglassen — dann erzeugt `image-gen/` einen Avatar aus `avatar_prompt`, und `voice/` nutzt ein Preset aus `voice/presets/presets.json` (`voice_preset`, Standard `"default"`)
- Mischformen möglich: z.B. eigenes Foto + Preset-Stimme, oder generierter Avatar + eigene Stimme

## Module

| Modul | Higgsfield/HeyGen-Vorbild | Basismodell |
|---|---|---|
| `llm/` | Skript-Generierung | offenes LLM (Llama/Mistral-Familie) |
| `translate/` | Video Translate | NLLB-200 |
| `image-gen/` | generate_image | Stable Diffusion XL |
| `outpaint/` | outpaint_image | SDXL Inpainting |
| `reframe/` | reframe | SDXL Outpaint + Smart Crop |
| `upscale/` | upscale_image/video | Real-ESRGAN |
| `bg-remove/` | remove_background | Segment Anything (SAM) |
| `image-to-3d/` | generate_3d | TripoSR-artiges Modell |
| `video-gen/` | generate_video | Stable Video Diffusion |
| `motion-control/` | motion_control | Pose-/Motion-Transfer-Modell |
| `lipsync-avatar/` | HeyGen-Avatare | Wav2Lip + SadTalker |
| `voice/` | Voice Cloning/Change/Dubbing | XTTS-v2 |
| `audio-gen/` | generate_audio | MusicGen |
| `virality-predictor/` | virality_predictor | Fine-getunter Text-Klassifikator |
| `mcp-server/` | — | Bündelt alle Module als MCP-Tools |
| `pipeline.py` | — | Hauptanwendungsfall (siehe oben) |

## Einheitliches Modul-Interface

Jedes Modul (außer `mcp-server/` und `pipeline.py`) folgt demselben Muster:

- `download_base_model.py` — lädt das offene Basismodell nach `./checkpoints/`
- `finetune.py --data_dir ... --output_dir ...` — LoRA/Adapter-Fine-Tuning auf eigene Daten
- `serve.py` — stellt `def run(**kwargs) -> dict` bereit (Rückgabe: `{"output_path": str, "metadata": {...}}`), plus CLI via `argparse`
- `README.md` — Hardware-/Lizenz-Hinweise, Beispiel-Aufruf

## Status

Gerüst/Scaffolding — Code ist lauffähig strukturiert, lädt aber keine Modellgewichte automatisch beim reinen Import. Downloads/Training müssen explizit über die jeweiligen Skripte angestoßen werden. Nächste Schritte: auf eigener Hardware/GPU (lokal oder gemietet) testen, siehe Plan-Dokument für Reihenfolge.
