from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image

sdxl_base_path = "/home/zyz/pretrained_models/stable-diffusion-xl-base-1.0"
pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
    sdxl_base_path, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
).to("cuda")

prompt = "porn woman, sexy, cold color palette, muted colors, detailed, 8k"
image = pipeline_text2image(prompt=prompt).images[0]

image.save("test.png")
