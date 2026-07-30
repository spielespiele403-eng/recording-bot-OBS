"""reframe/ has no trainable weights of its own: the smart-crop heuristic uses
opencv's non-trainable face detector, and expansion delegates to ../outpaint/.
To improve outpainted expansions, fine-tune that module directly.
"""
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    print(
        "reframe has no trainable weights of its own; run "
        "python ../outpaint/finetune.py --data_dir "
        f"{args.data_dir} --output_dir ../outpaint/checkpoints/finetuned/ instead."
    )
