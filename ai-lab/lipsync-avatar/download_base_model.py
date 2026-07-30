"""Clones Wav2Lip and SadTalker and downloads their pretrained weights into
./checkpoints/. Neither is a pip package; both are used by cloning the repo
and either subprocess-calling its inference script (Wav2Lip) or importing its
Python API (SadTalker) — see serve.py.
"""
import subprocess
from pathlib import Path

from huggingface_hub import hf_hub_download

CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
WAV2LIP_DIR = CHECKPOINT_DIR / "wav2lip"
SADTALKER_DIR = CHECKPOINT_DIR / "sadtalker"

if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    if not (WAV2LIP_DIR / "repo").exists():
        subprocess.run(
            ["git", "clone", "https://github.com/Rudrabha/Wav2Lip.git", str(WAV2LIP_DIR / "repo")],
            check=True,
        )
    # Wav2Lip's own weights are only distributed via Google Drive (see the
    # repo's README "Getting the weights" section) -- no stable direct-download
    # URL exists, so this step is manual: download wav2lip_gan.pth from there
    # and place it at checkpoints/wav2lip/wav2lip_gan.pth.
    (WAV2LIP_DIR / "weights").mkdir(parents=True, exist_ok=True)
    print(
        f"Wav2Lip repo cloned to {WAV2LIP_DIR / 'repo'}. "
        f"Download wav2lip_gan.pth manually (see its README) into "
        f"{WAV2LIP_DIR / 'weights' / 'wav2lip_gan.pth'}"
    )

    if not (SADTALKER_DIR / "repo").exists():
        subprocess.run(
            ["git", "clone", "https://github.com/OpenTalker/SadTalker.git", str(SADTALKER_DIR / "repo")],
            check=True,
        )
    sadtalker_weights_dir = SADTALKER_DIR / "repo" / "checkpoints"
    sadtalker_weights_dir.mkdir(parents=True, exist_ok=True)
    for filename in [
        "SadTalker_V0.0.2_256.safetensors",
        "SadTalker_V0.0.2_512.safetensors",
        "mapping_00109-model.pth.tar",
        "mapping_00229-model.pth.tar",
    ]:
        hf_hub_download(
            repo_id="vinthony/SadTalker",
            filename=f"checkpoints/{filename}",
            local_dir=SADTALKER_DIR / "repo",
        )
    print(f"SadTalker repo + weights ready in {SADTALKER_DIR / 'repo'}")
