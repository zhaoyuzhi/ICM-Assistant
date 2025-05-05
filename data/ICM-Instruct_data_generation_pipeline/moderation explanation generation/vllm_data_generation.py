import argparse
from openai import OpenAI
import json
import shutil
import tqdm
import cv2
import requests
import base64
import glob
import os


def request_sft_qwen_vl(messages, max_tokens=2048, temperature=1e-2, vlm_address="http://10.90.86.194:5022/v1/chat/completions"):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "Qwen2.5-VL-72B-AWQ",
        "messages": messages,
        "n": 1,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(vlm_address, data=json.dumps(payload), headers=headers)
    response_data = json.loads(response.text)
    content = response_data["choices"][0]["message"]["content"]
    return content

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64image_ = base64.b64encode(image_file.read()).decode('utf-8')
    return base64image_

def get_stage_prompt(image_path, previous_results=None):
    conversation_stage_1 = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encode_image_to_base64(image_path)}"}
                },
                {"type": "text",
                 "text":
                     f"""
                     Answer the following 3 questions sequentially based on the given description.
                     Do not use the first person view, answer with an objective description.
                     Explicit description: {previous_results}
                     
                     1. Please describe the image in detail with explicit information such as person's movements/clothes.
                     2. Please describe the implicit content of the image in detail, such as overall atmosphere.
                     3. Explain why this image is or not sexy based on the image explicit content and the implicit content.
                     """
                 },
            ],
        }
    ]
    return conversation_stage_1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images and generate textual descriptions.")
    parser.add_argument('--vlm_address', default="http://10.90.86.194:5022/v1/chat/completions", help='VLM API endpoint.')
    parser.add_argument('--input_dir', required=True, help='Directory containing input images.')
    parser.add_argument('--output_dir', required=True, help='Directory to save output texts.')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for im in glob.glob(os.path.join(args.input_dir, '*')):
        img_path = im
        key = im.split('\\')[-1].split('_2')[0]
        print(im)
        if key in conversion_dict:
            desc = short_desc[conversion_dict[key]]

            base_name = os.path.splitext(im)[0]
            output_path = os.path.join(args.output_dir, f"{os.path.basename(base_name)}.txt")

            result = request_sft_qwen_vl(get_stage_prompt(img_path, desc), vlm_address=args.vlm_address)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)

            print(f"Saved into：{output_path}")