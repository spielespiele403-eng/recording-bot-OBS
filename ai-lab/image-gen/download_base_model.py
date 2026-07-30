"""Downloads the base text-to-image model into ./checkpoints/."""
from pathlib import Path
from diffusers import DiffusionPipeline

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

if __name__ == "__main__":
    pipe = DiffusionPipeline.from_pretrained(MODEL_ID)
    pipe.save_pretrained(CHECKPOINT_DIR)
    print(f"Downloaded {MODEL_ID} to {CHECKPOINT_DIR}")
