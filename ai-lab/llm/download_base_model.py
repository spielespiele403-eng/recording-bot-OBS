"""Downloads the base instruction-tuned LLM into ./checkpoints/."""
from pathlib import Path
from huggingface_hub import snapshot_download

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=CHECKPOINT_DIR,
        ignore_patterns=["*.bin", "*.pth"],  # keep only safetensors weights
    )
    print(f"Downloaded {MODEL_ID} to {CHECKPOINT_DIR}")
