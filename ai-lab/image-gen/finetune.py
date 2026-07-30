"""LoRA fine-tunes the SDXL UNet on the user's own images (DreamBooth-style).

data_dir must contain image files (.png/.jpg/.jpeg). An optional .txt file
with the same basename as an image provides its caption; otherwise a generic
placeholder-token caption is used.
"""
import argparse
import glob
import os
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline
from peft import LoraConfig
from peft.utils import get_peft_model_state_dict
from PIL import Image
from torchvision import transforms

BASE_MODEL_DIR = Path(__file__).parent / "checkpoints"
DEFAULT_CAPTION = "a photo in sks style"
RESOLUTION = 1024


def load_examples(data_dir: str) -> list[tuple[Image.Image, str]]:
    examples = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*"))):
        if Path(path).suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        caption_path = Path(path).with_suffix(".txt")
        caption = (
            caption_path.read_text(encoding="utf-8").strip()
            if caption_path.exists()
            else DEFAULT_CAPTION
        )
        examples.append((Image.open(path).convert("RGB"), caption))
    return examples


def main(data_dir: str, output_dir: str, epochs: int = 20):
    pipe = StableDiffusionXLPipeline.from_pretrained(BASE_MODEL_DIR, torch_dtype=torch.float32)
    pipe.vae.requires_grad_(False)
    pipe.text_encoder.requires_grad_(False)
    pipe.text_encoder_2.requires_grad_(False)
    pipe.unet.requires_grad_(False)
    pipe.unet.add_adapter(
        LoraConfig(r=16, lora_alpha=16, target_modules=["to_k", "to_q", "to_v", "to_out.0"])
    )

    to_tensor = transforms.Compose(
        [
            transforms.Resize(RESOLUTION),
            transforms.CenterCrop(RESOLUTION),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ]
    )
    examples = [(to_tensor(img), caption) for img, caption in load_examples(data_dir)]

    trainable_params = [p for p in pipe.unet.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=1e-4)
    add_time_ids = torch.tensor([[RESOLUTION, RESOLUTION, 0, 0, RESOLUTION, RESOLUTION]])

    for epoch in range(epochs):
        for pixel_values, caption in examples:
            latents = (
                pipe.vae.encode(pixel_values.unsqueeze(0)).latent_dist.sample()
                * pipe.vae.config.scaling_factor
            )
            noise = torch.randn_like(latents)
            timesteps = torch.randint(0, pipe.scheduler.config.num_train_timesteps, (1,))
            noisy_latents = pipe.scheduler.add_noise(latents, noise, timesteps)

            prompt_embeds, _, pooled_embeds, _ = pipe.encode_prompt(
                caption, device=pipe.device, num_images_per_prompt=1, do_classifier_free_guidance=False
            )
            model_pred = pipe.unet(
                noisy_latents,
                timesteps,
                encoder_hidden_states=prompt_embeds,
                added_cond_kwargs={"text_embeds": pooled_embeds, "time_ids": add_time_ids},
            ).sample

            loss = torch.nn.functional.mse_loss(model_pred, noise)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        print(f"epoch {epoch + 1}/{epochs} loss {loss.item():.4f}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    StableDiffusionXLPipeline.save_lora_weights(
        output_dir, unet_lora_layers=get_peft_model_state_dict(pipe.unet)
    )
    print(f"Saved LoRA adapter to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_dir", default="./checkpoints/finetuned/")
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
