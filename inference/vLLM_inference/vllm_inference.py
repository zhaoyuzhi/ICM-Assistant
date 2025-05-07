import requests

# 假设这是你的固定prompt
fixed_prompt = "Expalin why is image is or not sexy."

def read_image_paths(file_path):
    """从给定的txt文件中读取图片路径"""
    with open(file_path, 'r') as file:
        image_paths = [line.strip() for line in file.readlines()]
    return image_paths

def query_model(image_path, prompt):
    """向模型发送请求并获取响应"""
    url = 'http://<your-model-server>/api/v1/generate'  # 替换为你的模型服务器地址
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "prompt": prompt + image_path,
        "max_tokens": 50,  # 根据需要调整
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['text']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


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

def get_prompt(image_path, fixed_prompt, previous_results=None):
    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encode_image_to_base64(image_path)}"}
                },
                {
                    "type": "text",
                    "text": fixed_prompt
                },
            ],
        }
    ]
    return conversation



def save_results(results, output_file):
    """将结果保存到指定的输出文件"""
    with open(output_file, 'w') as file:
        for image_path, (prompt, answer) in results.items():
            file.write(f"{image_path}\n")
            file.write(f"{prompt}\n")
            file.write(f"{answer}\n")

def main(input_file, output_file):
    image_paths = read_image_paths(input_file)
    results = {}
    for image_path in image_paths:
        try:
            print(f"Processing {image_path}...")
            prompt_with_path = get_prompt(image_path, fixed_prompt)
            answer = request_sft_qwen_vl(prompt_with_path)
            results[image_path] = (fixed_prompt, answer)
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
    
    save_results(results, output_file)

if __name__ == '__main__':
    input_file = 'image_paths.txt'  # 输入的图片列表文件
    output_file = 'results.txt'     # 输出的结果文件
    main(input_file, output_file)