"""Clones MagicAnimate and downloads its pretrained weights into ./checkpoints/.

MagicAnimate is not pip-installable; it's used by cloning the GitHub repo and
importing its model/pipeline classes directly (see serve.py / finetune.py).
"""
import subprocess
from pathlib import Path

from huggingface_hub import snapshot_download

REPO_URL = "https://github.com/magic-research/magic-animate.git"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
REPO_DIR = CHECKPOINT_DIR / "magicanimate_repo"
PRETRAINED_DIR = CHECKPOINT_DIR / "pretrained_models"

if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    if not REPO_DIR.exists():
        subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True)

    # MagicAnimate's own appearance encoder + pose ControlNet + temporal weights
    snapshot_download(repo_id="zcxu-eric/MagicAnimate", local_dir=PRETRAINED_DIR / "magicanimate")
    # Underlying Stable Diffusion 1.5 + fine-tuned VAE it builds on
    snapshot_download(
        repo_id="runwayml/stable-diffusion-v1-5",
        local_dir=PRETRAINED_DIR / "stable-diffusion-v1-5",
        allow_patterns=["*.json", "*fp16*"],
    )
    snapshot_download(repo_id="stabilityai/sd-vae-ft-mse", local_dir=PRETRAINED_DIR / "sd-vae-ft-mse")
    print(f"Cloned repo to {REPO_DIR}, weights in {PRETRAINED_DIR}")
