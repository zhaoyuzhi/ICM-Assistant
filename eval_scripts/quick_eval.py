from lmdeploy import pipeline, GenerationConfig
from lmdeploy.vl import load_image
import os

import math
import json
import requests
import base64

# 初始化模型管道
pipe = pipeline('zhaoyuzhi/ICM-InternVL2_5-1B')

# 固定 prompt
prompt = 'Is the image sexy?'
YES_TOKEN_ID = 9454  # "Yes" 的 token ID
NO_TOKEN_ID = 151643  # "No" 的 token ID

def read_image_paths(file_path):
    """读取图片路径"""
    with open(file_path, 'r') as f:
        paths = [line.strip() for line in f.readlines()]
    return paths

def calculate_softmax(logits_yes, logits_no):
    """计算两个logits的softmax"""
    exp_yes = math.exp(logits_yes)
    exp_no = math.exp(logits_no)
    total = exp_yes + exp_no
    prob_yes = exp_yes / total
    return prob_yes  # 只返回 yes 的概率


def request_sft_qwen_vl(messages, max_tokens=2048, temperature=1e-2):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "Qwen2-VL-2B",
        "messages": messages,
        "n": 1,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    # Please replace with your own deployed model
    response = requests.post("http://10.90.86.194:5022/v1/chat/completions", json.dumps(payload), headers=headers)
    response_data = json.loads(response.text)
    content = response_data["choices"][0]["message"]["content"]
    return content

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64image_ = base64.b64encode(image_file.read()).decode('utf-8')
    image_file.close()
    return base64image_


def get_prompt(image_path):
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
                     Is the image sexy?
                     """
                 },
            ],
        }
    ]
    return conversation_stage_1


def get_prompt_query(image_path, query):
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
                     {query}
                     """
                 },
            ],
        }
    ]
    return conversation_stage_1

def eval_images_val(image_paths):
    results = []
    correct = 0
    for img_path in image_paths:
        try:
            print(f"Processing {img_path}...")
            # 加载图片
            messages = get_prompt(image_paths)
            # 推理
            response = request_sft_qwen_vl(messages)
            ans = response
            print(ans)
            if 'yes' in ans.lower() and 'normal' not in image_paths:
                correct += 1
            if 'no' in ans.lower() and 'normal' in image_paths:
                correct += 1
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")
    print(correct / 1623.)


def eval_images_qa(paths):
    results = []
    correct = 0
    l = len(paths) // 3
    for idx in range(l):
        try:
            img_path = paths[3*idx]
            query = paths[3*idx + 1]
            ans = paths[3*idx + 2]
            print(f"Processing {img_path}...")
            # 加载图片
            messages = get_prompt_query(image_paths, query)
            # 推理
            response = request_sft_qwen_vl(messages)
            if (ans.lower()[0] == response.lower()[0]):
                correct += 1
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")
    print(1. * correct / l)


if __name__ == '__main__':
    input_txt = 'image_paths.txt'
    input_txt_qa = 'image_paths_qa.txt'
    image_paths = read_image_paths(input_txt)
    image_paths_qa = read_image_paths(input_txt_qa)


    # for evaluation of classification question: Is the image sexy?
    eval_images_val(image_paths)

    # for evaluation of Yes/No and Multi-choice question
    eval_images_qa(image_paths)


    # input_txt examples:
    #
    #  image_x_sexy.jpg
    #  ...
    #  image_y_normal.jpg


    # input_txt_qa examples:

    #  image_x_sexy.jpg
    #  question_x
    #  answer_x
    #  ...
    #  image_y_normal.jpg
    #  question_y
    #  answer_y

