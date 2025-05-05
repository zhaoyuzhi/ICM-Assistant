from openai import OpenAI
import json
import shutil
import tqdm
import cv2
import requests
import base64


def request_sft_qwen_vl(messages, max_tokens=2048, temperature=1e-2):
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
    response = requests.post("http://10.90.86.194:5022/v1/chat/completions", json.dumps(payload), headers=headers)
    response_data = json.loads(response.text)
    content = response_data["choices"][0]["message"]["content"]
    return content

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64image_ = base64.b64encode(image_file.read()).decode('utf-8')
    image_file.close()
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

short_desc = {
    "upper_chest": "It is known that the image is a close-up of a person's upper chest, showing her cleavage.",
    "upper_back": "It is known that the person in the image has her back bare, which often gives people a sexy feel.",
    "upper_belly": "It is known that the person in the image has her belly exposed.",
    "upper_lift_up_clothes": "It is known that the person in the image is lifting up clothes, which often gives people a sexy feel.",
    "upper_stick_out_tongue": "It is known that the woman in the image is sticking out her tongue, which often gives people a sexy feel.",
    "upper_pout_mouth": "It is known that the person in the image is posing as if kissing, which often gives people a sexy feel.",
    "upper_take_on_underwear": "It is known that the woman in the image is putting on the underwear, which often gives people a sexy feel.",
    "upper_bite_lip": "It is known that the person in the image is biting her lip, which often gives people a sexy feel.",
    "upper_male_largely_bare_body": "It is known that the male in the image has a large area of his body exposed.",
    "upper_largely_bare_body": "It is known that the person in the image has a large area of her body exposed.",
    "upper_bite_fingers": "It is known that if a person puts her finger inside her mouth, it often gives people a sexy feel.",
    "upper_wear_wet_clothes": "It is known that the person's upper clothes are soaked, which often gives people a sexy feel.",
    "middle_legs": "It is known that if a person's clothes almost expose her thighs, it often gives people a sexy feel.",
    "middle_belly": "It is known that the person in the image has her belly exposed.",
    "middle_hip": "It is known that the image is a close-up of the buttocks.",
    "middle_crotch": "It is known that the image is a close-up of the crotch, and the person is only wearing underwear.",
    "lower_leg": "It is known that the person in the image is naked from her thighs to his/her ankles.",
    "lower_belly": "It is known that the person in the image has her belly exposed.",
    "lower_hip": "It is known that the person in the photo deliberately shows her buttocks, an action that often gives people a sexy feel.",
    "lower_take_on_stockings": "It is known that the person in the image is taking on lower stockings, which often gives people a sexy feel.",
    "lower_largely_bare_body": "It is known that the person in the image has a large area of her body exposed.",
    "lower_take_off_stockings": "It is known that the woman in the image is taking off lower stockings, which often gives people a sexy feel.",
    "lower_lift_up_dresses": "It is known that the person in the image is lifting their clothes, which often gives people a sexy feel.",
    "whole_largely_bare_body": "It is known that the person in the image has a large area of her body exposed.",
    "whole_leg": "It is known that if a person's clothes almost expose her thighs, it often gives people a sexy feel.",
    "whole_belly": "It is known that the person in the image has her belly exposed.",
    "whole_back": "It is known that the person in the image has her back bare, which often gives people a sexy feel.",
    "whole_take_off_clothes": "It is known that the person in the image is taking of clothes, which often gives people a sexy feel.",
    "other_meme": "It is known that there are texts with teasing or sexually suggestive meanings in the image.",
    "other_patterns": "It is known that there are sexually suggestive patterns or similar objects in the image.",
    "other_kiss": "It is known that the people in the image are kissing.",
    "upper_normal_body": "It is known that the exposure level of this image is very low and it is an appropriate image.",
    "middle_normal_body": "It is known that the exposure level of this image is very low and it is an appropriate image.",
    "lower_normal_body": "It is known that the exposure level of this image is very low and it is an appropriate image.",
    "whole_normal_body": "It is known that the exposure level of this image is very low and it is an appropriate image."
}

conversion_dict = {
    'bite_finger': 'upper_bite_fingers',
    'bite_lip': 'upper_bite_lip',
    'liftup': 'upper_lift_up_clothes',

    'lower_hips': 'lower_hip',
    'lower_large_bare': 'lower_largely_bare_body',
    'lower_leg': 'lower_leg',
    'lower_normal': 'lower_normal_body',
    'lower_shoulders_and_belly': 'lower_belly',

    'male_sexy': 'upper_male_largely_bare_body',

    'middle_crotch': 'middle_crotch',
    'middle_leg': 'middle_leg',
    'middle_hips': 'middle_hip',
    'middle_normal': 'middle_normal_body',
    'middle_shoulders_and_belly': 'middle_belly',

    'pout': 'upper_pout_mouth',
    'sexy_imagetext': 'other_meme',
    'sexy_implicit': 'other_patterns',
    'sexy_kiss': 'other_kiss',

    'skirt': 'lower_lift_up_dresses',
    'stockings': 'lower_take_off_stockings',
    'takeoff': 'whole_take_off_clothes',
    'tongue': 'upper_stick_out_tongue',

    'upper_backless': 'upper_back',
    'upper_bust': 'upper_chest',
    'upper_large_bare': 'upper_largely_bare_body',
    'upper_normal': 'upper_normal_body',
    'upper_shoulders_and_belly': 'upper_belly',

    'wearing_bras': 'upper_take_on_underwear',
    'wearing_stockings': 'lower_take_on_stockings',
    'wet': 'upper_wear_wet_clothes',
    'whole_backless': 'whole_back',
    'whole_large_bare': 'whole_largely_bare_body',
    'whole_leg': 'whole_leg',
    'whole_normal': 'whole_normal_body',
    'whole_shoulders_and_belly': 'whole_belly'
}
# bbox = [x_min, y_min, x_max, y_max]

import glob
import os

output_dir = "D:\\uitar\\output"
os.makedirs(output_dir, exist_ok=True)  # 创建输出目录（如果不存在）

for im in glob.glob('D:\\sexy_check_all\\*'):
    img_path = im
    key = im.split('\\')[-1].split('_2')[0]
    print(im)
    if key in conversion_dict:
        desc = short_desc[conversion_dict[key]]

        # 生成输出文件名（保留原文件名，扩展名改为.txt）
        base_name = os.path.splitext(im)[0]  # 去除扩展名
        output_path = os.path.join(output_dir, f"{base_name}.txt")

        # 获取处理结果
        result = request_sft_qwen_vl(get_stage_prompt(img_path, desc))

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)

        # 保留原有的print语句（可选）
        print(f"已保存结果到：{output_path}")