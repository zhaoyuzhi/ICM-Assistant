from lmdeploy import pipeline, GenerationConfig
from lmdeploy.vl import load_image
import os
import math
import json

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

def process_images(image_paths, output_json):
    results = []
    for img_path in image_paths:
        try:
            print(f"Processing {img_path}...")

            # 加载图片
            image = load_image(img_path)

            # 推理
            response = pipe((prompt, image), gen_config=GenerationConfig(output_logits='generation'))

            # 提取 logit
            logits = response.logits
            logits_yes = float(logits[0, YES_TOKEN_ID])
            logits_no = float(logits[0, NO_TOKEN_ID])

            # softmax
            sexy_score = calculate_softmax(logits_yes, logits_no)
            conclusion = "Yes" if sexy_score > 0.5 else "No"

            # 构造结果
            result = {
                "image_name": os.path.basename(img_path),
                "logit_yes": logits_yes,
                "logit_no": logits_no,
                "sexy_score": sexy_score,
                "sexy_conclusion": conclusion
            }
            results.append(result)

        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")

    # 写入 JSON 文件
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    input_txt = 'image_paths.txt'     # 输入图片列表 txt
    output_json = 'results.json'      # 输出结果 json

    image_paths = read_image_paths(input_txt)
    process_images(image_paths, output_json)
    print("处理完成，结果已写入", output_json)