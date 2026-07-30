"""reframe/ has no model of its own: smart-crop uses opencv's bundled face
detector, and expansion delegates to ../outpaint/, whose checkpoints must be
downloaded separately.
"""
from pathlib import Path

OUTPAINT_DOWNLOAD_SCRIPT = Path(__file__).parent.parent / "outpaint" / "download_base_model.py"
OUTPAINT_CHECKPOINT_DIR = Path(__file__).parent.parent / "outpaint" / "checkpoints"

if __name__ == "__main__":
    if OUTPAINT_CHECKPOINT_DIR.exists():
        print(f"outpaint checkpoints found at {OUTPAINT_CHECKPOINT_DIR}")
    else:
        print(f"No model to download here. Run: python {OUTPAINT_DOWNLOAD_SCRIPT}")
