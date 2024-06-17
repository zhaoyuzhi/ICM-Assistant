import torch
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image

sdxl_base_path = "/home/zyz/pretrained_models/stable-diffusion-xl-base-1.0"
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    sdxl_base_path, torch_dtype=torch.float16
)
pipe = pipe.to("cuda")
url = "source_img.jpg"

init_image = load_image(url).convert("RGB")
prompt = "a photo of an beautiful woman"
image = pipe(prompt, image=init_image).images[0]

image.save("img2img.png")
