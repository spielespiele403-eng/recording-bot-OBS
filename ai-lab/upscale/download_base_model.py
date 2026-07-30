"""Downloads the Real-ESRGAN x4plus weights into ./checkpoints/."""
from pathlib import Path
from basicsr.utils.download_util import load_file_from_url

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    path = load_file_from_url(MODEL_URL, model_dir=str(CHECKPOINT_DIR), file_name="RealESRGAN_x4plus.pth")
    print(f"Downloaded RealESRGAN_x4plus to {path}")
