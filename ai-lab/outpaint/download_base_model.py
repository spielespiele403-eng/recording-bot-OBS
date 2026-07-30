"""Downloads the base SDXL inpainting model into ./checkpoints/."""
from pathlib import Path
from diffusers import AutoPipelineForInpainting

MODEL_ID = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

if __name__ == "__main__":
    pipe = AutoPipelineForInpainting.from_pretrained(MODEL_ID)
    pipe.save_pretrained(CHECKPOINT_DIR)
    print(f"Downloaded {MODEL_ID} to {CHECKPOINT_DIR}")
