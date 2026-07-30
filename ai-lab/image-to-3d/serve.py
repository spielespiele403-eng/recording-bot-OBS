"""Reconstructs a textured 3D mesh (GLB) from a single image using TripoSR."""
import argparse
import json
from pathlib import Path

import rembg
import torch
from PIL import Image
from tsr.system import TSR
from tsr.utils import remove_background, resize_foreground

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
FINETUNED_DIR = Path(__file__).parent / "checkpoints" / "finetuned"

_model = None
_rembg_session = None
_device = "cuda" if torch.cuda.is_available() else "cpu"


def _load():
    global _model, _rembg_session
    if _model is not None:
        return
    model_dir = FINETUNED_DIR if FINETUNED_DIR.exists() else BASE_MODEL_DIR
    _model = TSR.from_pretrained(str(model_dir), config_name="config.yaml", weight_name="model.ckpt")
    _model.renderer.set_chunk_size(8192)
    _model.to(_device)
    _model.eval()
    _rembg_session = rembg.new_session()


def run(image_path: str, output: str = "out.glb", mc_resolution: int = 256, **kwargs) -> dict:
    _load()
    image = Image.open(image_path).convert("RGB")
    image = remove_background(image, _rembg_session)
    image = resize_foreground(image, 0.85)

    with torch.no_grad():
        scene_codes = _model([image], device=_device)
        meshes = _model.extract_mesh(scene_codes, resolution=mc_resolution)

    output_path = Path(output)
    meshes[0].export(str(output_path))
    metadata = {
        "vertices": int(len(meshes[0].vertices)),
        "faces": int(len(meshes[0].faces)),
        "mc_resolution": mc_resolution,
    }
    return {"output_path": str(output_path), "metadata": metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--output", default="out.glb")
    parser.add_argument("--mc_resolution", type=int, default=256)
    args = parser.parse_args()
    result = run(image_path=args.image_path, output=args.output, mc_resolution=args.mc_resolution)
    print(json.dumps(result, indent=2))
