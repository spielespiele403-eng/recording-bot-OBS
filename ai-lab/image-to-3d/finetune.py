"""Fine-tunes only TripoSR's NeRF decoder MLP on user-specific object
categories. TripoSR's image tokenizer and triplane transformer backbone are
trained on ~1M synthetic 3D objects and are not realistically re-trained by
end users, so both stay frozen here; only model.decoder is updated.
model.render() runs its ray marching under torch.no_grad() internally (it is
an inference-only convenience method), so training instead calls
model.renderer(...) directly on rays built the same way, to keep gradients.

data_dir must contain one subfolder per object, each with:
  input.png    - the reference image fed to TripoSR
  views/*.png  - n_views ground-truth turntable renders (elevation 0 degrees,
                 evenly spaced azimuth), matching get_spherical_cameras' convention
"""
import argparse
import glob
from pathlib import Path

import torch
import torchvision.transforms.functional as TF
from PIL import Image
from tsr.system import TSR
from tsr.utils import get_spherical_cameras

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"


def main(data_dir: str, output_dir: str, epochs: int, lr: float):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = TSR.from_pretrained(str(BASE_MODEL_DIR), config_name="config.yaml", weight_name="model.ckpt")
    model.to(device)
    model.renderer.set_chunk_size(8192)

    for param in model.image_tokenizer.parameters():
        param.requires_grad = False
    for param in model.backbone.parameters():
        param.requires_grad = False
    optimizer = torch.optim.Adam(model.decoder.parameters(), lr=lr)

    object_dirs = sorted(p for p in Path(data_dir).iterdir() if p.is_dir())

    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for obj_dir in object_dirs:
            image = Image.open(obj_dir / "input.png").convert("RGB")
            view_paths = sorted(glob.glob(str(obj_dir / "views" / "*.png")))
            gt_views = torch.stack(
                [TF.to_tensor(Image.open(p).convert("RGB")) for p in view_paths]
            ).to(device)

            scene_codes = model([image], device=device)
            rays_o, rays_d = get_spherical_cameras(
                len(view_paths), elevation_deg=0.0, camera_distance=1.9, fovy_deg=40.0, height=256, width=256
            )
            rendered = torch.stack(
                [
                    model.renderer(model.decoder, scene_codes[0], o.to(device), d.to(device))
                    for o, d in zip(rays_o, rays_d)
                ]
            )
            loss = torch.nn.functional.mse_loss(rendered, gt_views)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"epoch {epoch+1}/{epochs} loss {epoch_loss / len(object_dirs):.4f}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), Path(output_dir) / "model.ckpt")
    (Path(output_dir) / "config.yaml").write_text((BASE_MODEL_DIR / "config.yaml").read_text())
    print(f"Saved fine-tuned decoder to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=1e-4)
    args = parser.parse_args()
    main(args.data_dir, args.output_dir, args.epochs, args.lr)
