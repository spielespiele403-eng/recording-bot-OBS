# lipsync-avatar/ — Sprechender Avatar

Ersetzt: HeyGen's Kernfunktion, die KI-Avatare. Erzeugt aus einem Foto/Video eines Gesichts und einer Audiospur ein Video, in dem die Person das Gesagte spricht. **Das Modul, das im Hauptanwendungsfall (`Prompt → llm/ → voice/ → lipsync-avatar/`) direkt verwendet wird.**

Zwei Modi, gesteuert über `mode`:

- `"wav2lip"` — synct nur den Mundbereich auf ein bestehendes Video/Standbild; Kopf bleibt unbewegt bzw. bewegt sich wie im Quellvideo. Schnell, robust, aber kein eigenständiges Kopf-/Blick-/Mimikspiel.
- `"sadtalker"` — animiert ein einzelnes Standfoto vollständig (Kopfbewegung, Blinzeln, Mimik) allein aus Audio. Aufwändiger, aber überzeugender für "aus einem Foto einen sprechenden Menschen machen".

## Basismodelle

- **Wav2Lip** (GitHub: [Rudrabha/Wav2Lip](https://github.com/Rudrabha/Wav2Lip)) — Encoder-Decoder-GAN für audio-getriebene Lippensynchronisation. Die Gewichte (`wav2lip_gan.pth`) werden **nicht** über Hugging Face oder eine feste URL verteilt, sondern laut Repo-README nur über Google Drive — deshalb ist dieser Download-Schritt in `download_base_model.py` manuell (Link im Wav2Lip-README, Datei nach `checkpoints/wav2lip/weights/wav2lip_gan.pth` legen).
- **SadTalker** (GitHub: [OpenTalker/SadTalker](https://github.com/OpenTalker/SadTalker), Gewichte gespiegelt auf Hugging Face: [vinthony/SadTalker](https://huggingface.co/vinthony/SadTalker)) — Audio-zu-3D-Bewegungskoeffizienten-Modell + Face-Renderer, animiert Kopf/Mimik aus einem einzelnen Foto.

Beide sind reine GitHub-Repos ohne pip-Paket; `download_base_model.py` klont sie nach `./checkpoints/{wav2lip,sadtalker}/repo/`.

## Hardware

- Disk: ~2 GB (Wav2Lip-Gewichte) + ~5 GB (SadTalker-Gewichte inkl. Renderer)
- **VRAM: mindestens 16 GB empfohlen**, wenn beide Modi verfügbar sein sollen (SadTalker allein läuft mit ca. 6-8 GB, Wav2Lip mit ca. 4 GB — aber ein 16GB+-GPU ist die realistische Baseline, damit z.B. auch parallel `voice/` oder `llm/` geladen sein können). CPU-only ist für beide Modelle nicht praktikabel: Wav2Lip-Inferenz dauert dann Minuten statt Sekunden pro Videosekunde, SadTalker ist auf CPU kaum nutzbar.
- Fine-Tuning: Wav2Lip ist ein kleines Conv-Netz (kein Transformer) — "LoRA" bedeutet hier peft-LoRA-Adapter auf den Decoder-Conv-Layern, identitätsspezifisch auf eigenem Videomaterial trainiert (~6-10 GB VRAM, auf einer RTX 3060/4090 bei ein paar Minuten eigenem Videomaterial ca. 30-45 Minuten für 20 Epochen). SadTalker-Fine-Tuning ist in diesem Scaffold nicht enthalten (das Modell generalisiert bereits gut über Gesichter aus einem einzigen Foto; personenspezifisches Fine-Tuning bringt hier vergleichsweise wenig).

## Lizenz-Hinweise

- Wav2Lip: Code steht unter einer **nicht-kommerziellen Forschungslizenz** (siehe Repo-LICENSE) — ausdrücklich nur für Forschungs-/persönliche Zwecke, keine kommerzielle Nutzung ohne Rücksprache mit den Autoren.
- SadTalker: Code unter Apache-2.0, einzelne Komponenten (z.B. der Face-Renderer, teils von face-vid2vid/PIRender abgeleitet) können abweichende, teils nicht-kommerzielle Lizenzbedingungen haben — vor kommerziellem Einsatz im Repo genau nachlesen.
- **Wie bei den anderen Video-/Avatar-Modulen gilt: deutlich strengere Lizenzlage als bei offenen LLMs/Bildmodellen.** Für privaten Gebrauch (eigene Stimme, eigenes Gesicht, kein Vertrieb) unkritisch; kommerzielle Nutzung vorher rechtlich prüfen.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_face_clips --output_dir ./checkpoints/finetuned/
python serve.py --face_image_or_video_path ./me.jpg --audio_path ./speech.wav --mode sadtalker --output out.mp4
python serve.py --face_image_or_video_path ./me.mp4 --audio_path ./speech.wav --mode wav2lip --output out.mp4
```

Programmatisch:

```python
from serve import run
result = run(face_image_or_video_path="./me.jpg", audio_path="./speech.wav", mode="sadtalker")
print(result["output_path"])
```
