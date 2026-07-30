"""Downloads Stable Video Diffusion (img2vid-xt) into ./checkpoints/."""
from pathlib import Path
from huggingface_hub import snapshot_download

MODEL_ID = "stabilityai/stable-video-diffusion-img2vid-xt"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=CHECKPOINT_DIR,
        ignore_patterns=["*.safetensors.index.fp16.json", "*.ckpt"],
    )
    print(f"Downloaded {MODEL_ID} to {CHECKPOINT_DIR}")
