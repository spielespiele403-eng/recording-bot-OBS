# video-gen/ — Bild-zu-Video

Ersetzt: Higgsfield's `generate_video`. Nimmt ein Startbild entgegen und erzeugt daraus einen kurzen Videoclip (Kamera-/Objektbewegung, kein neuer Bildinhalt).

Reines Text-zu-Video ist mit diesem Basismodell nicht möglich — dafür muss zuerst `image-gen/` (SDXL) ein Startbild aus dem Prompt erzeugen, das dann hier als `image_path` eingespeist wird (`Prompt → image-gen/ → video-gen/`).

## Basismodell

`stabilityai/stable-video-diffusion-img2vid-xt` (Hugging Face: [stabilityai/stable-video-diffusion-img2vid-xt](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt), via `diffusers`) — Stability AI's Image-to-Video-Latent-Diffusion-Modell, erzeugt 25 Frames bei 1024x576.

## Hardware

- Disk: ~10 GB (fp16 Safetensors)
- **VRAM: mindestens 16 GB für Inferenz** (mit `enable_model_cpu_offload()` bereits berücksichtigt; ohne Offloading eher 20+ GB). Ein leistungsfähiges GPU ist praktisch Pflicht — CPU-only ist für dieses Modul nicht praktikabel (mehrere Minuten bis Stunden pro Clip, falls überhaupt lauffähig).
- Fine-Tuning (LoRA, r=16): 20-24 GB VRAM, auf einer RTX 4090 bei einigen Dutzend kurzen Clips ca. 1-2 Stunden für 10 Epochen. Video-Diffusion-Fine-Tuning ist deutlich speicherhungriger als Bild- oder Text-Fine-Tuning (Frame-Stapel statt Einzelbild).

## Lizenz-Hinweise

**Achtung, restriktiver als die meisten anderen Module hier:** Stable Video Diffusion steht unter der [Stability AI Community License](https://stability.ai/community-license) — kostenlos für Forschung und für Organisationen/Individuen mit weniger als $1M Jahresumsatz; darüber hinaus ist eine kostenpflichtige Enterprise-Lizenz von Stability AI erforderlich. Rein privates Streaming-/Hobby-Setup ist unkritisch, bei kommerzieller Nutzung oberhalb der Umsatzgrenze vorher prüfen. Generell gilt für Videomodelle: Lizenzen sind tendenziell strikter/forschungsnäher als bei Bild- oder Textmodellen — vor Produktiveinsatz die jeweils aktuelle Lizenz auf der Modellseite gegenlesen.

## Verwendung

```bash
python download_base_model.py
python finetune.py --data_dir ./data/my_clips --output_dir ./checkpoints/finetuned/
python serve.py --image_path ./start_frame.png --output out.mp4 --num_frames 25
```

Programmatisch:

```python
from serve import run
result = run(image_path="./start_frame.png", num_frames=25)
print(result["output_path"])
```
