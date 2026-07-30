"""Changes an image's aspect ratio: crops around the region of interest (face
if detected, else full frame) when that fits the target ratio, otherwise
expands the canvas via ../outpaint/ so nothing is cut off.
"""
import argparse
import importlib.util
import json
from pathlib import Path

import cv2

_OUTPAINT_SERVE_PATH = Path(__file__).parent.parent / "outpaint" / "serve.py"
_spec = importlib.util.spec_from_file_location("outpaint_serve", _OUTPAINT_SERVE_PATH)
_outpaint_serve = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_outpaint_serve)
outpaint_run = _outpaint_serve.run

_FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _detect_roi(image, w: int, h: int) -> tuple[int, int, int, int]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = _FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return (0, 0, w, h)
    x0 = min(x for x, y, fw, fh in faces)
    y0 = min(y for x, y, fw, fh in faces)
    x1 = max(x + fw for x, y, fw, fh in faces)
    y1 = max(y + fh for x, y, fw, fh in faces)
    return (x0, y0, x1 - x0, y1 - y0)


def run(image_path: str, target_aspect_ratio: str, output: str = "out.png", **kwargs) -> dict:
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    tw, th = (int(x) for x in target_aspect_ratio.split(":"))
    target_ratio = tw / th
    current_ratio = w / h

    roi_x, roi_y, roi_w, roi_h = _detect_roi(image, w, h)

    if target_ratio <= current_ratio:
        new_w, new_h = round(h * target_ratio), h
    else:
        new_w, new_h = w, round(w / target_ratio)

    if new_w >= roi_w and new_h >= roi_h:
        cx, cy = roi_x + roi_w // 2, roi_y + roi_h // 2
        x0 = min(max(cx - new_w // 2, 0), w - new_w)
        y0 = min(max(cy - new_h // 2, 0), h - new_h)
        cropped = image[y0 : y0 + new_h, x0 : x0 + new_w]
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output, cropped)
        return {
            "output_path": output,
            "metadata": {"method": "crop", "roi": [roi_x, roi_y, roi_w, roi_h], "size": [new_w, new_h]},
        }

    # cropping to the target ratio would clip the region of interest -> expand instead
    if target_ratio > current_ratio:
        total_expand = round(h * target_ratio) - w
        directions = ("left", "right")
    else:
        total_expand = round(w / target_ratio) - h
        directions = ("top", "bottom")

    half = total_expand // 2
    tmp_path = str(Path(output).with_suffix(".tmp" + Path(output).suffix))
    first = outpaint_run(image_path=image_path, direction=directions[0], expand_px=half, output=tmp_path)
    second = outpaint_run(
        image_path=first["output_path"],
        direction=directions[1],
        expand_px=total_expand - half,
        output=output,
    )
    return {
        "output_path": second["output_path"],
        "metadata": {"method": "outpaint", "directions": list(directions), "expand_px": total_expand},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--target_aspect_ratio", required=True, help='e.g. "16:9", "9:16", "1:1"')
    parser.add_argument("--output", default="out.png")
    args = parser.parse_args()
    result = run(
        image_path=args.image_path,
        target_aspect_ratio=args.target_aspect_ratio,
        output=args.output,
    )
    print(json.dumps(result, indent=2))
