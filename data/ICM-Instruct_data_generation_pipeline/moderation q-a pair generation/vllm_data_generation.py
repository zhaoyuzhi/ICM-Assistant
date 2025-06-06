# -*- coding: utf-8 -*-
import os
import argparse
import re
import requests
import json
from markdown_it import MarkdownIt
from gradio_client import Client
from gradio import utils

# read a txt expect EOF
def text_readlines(filename, mode='r'):
    try:
        file = open(filename, mode, encoding='utf-8')
    except IOError:
        error = []
        return error
    content = file.readlines()
    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]
    file.close()
    return content

# save a list to a txt
def text_save(content, filename, mode='a'):
    file = open(filename, mode, encoding='utf-8')
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# call LLM with vllm address as a parameter
def llm_client(prompt, stream=True, vllm_address="http://10.90.86.155:8000/generate"):
    headers = {"User-Agent": "vLLM Client"}
    pload = {
        "prompt": prompt,
        "stream": stream,
        "max_tokens": 2048,
        "top_p": 0.9,
        "temperature": 0.6
    }
    response = requests.post(vllm_address, headers=headers, json=pload, stream=stream)
    for chunk in response.iter_lines(chunk_size=8192, decode_unicode=False, delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode("utf-8"))
            clean_text = data["text"][0]
            clean_text = re.sub(r'$INST$.*?$/INST$', '', clean_text, flags=re.DOTALL)  # 去除系统提示部分
            clean_text = clean_text.strip()  # 去除首尾空白
    return clean_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_path', type=str, default='CoT_prompts_1/all_LLaVA_results_revised/liftup.txt', help='File path')
    parser.add_argument('--q_type', default='mix', choices=['mc', 'qa', 'mix'], help='The choices of prompting')
    parser.add_argument('--vllm_address', type=str, default="http://10.90.86.155:8000/generate", help='vLLM API endpoint.')
    opt = parser.parse_args()
    print(opt)
    
    # define base
    text_list = text_readlines(opt.txt_path)
    text_list_half_length = len(text_list) // 2
    save_path = opt.txt_path.split('/')[-1].split('.')[0] + '_' + opt.q_type
    check_path(save_path)

    # define input
    system_message = 'You are an image content moderator who can analyze a single image.'
    if opt.q_type == 'mc':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 5 multiple-choice questions (4 choices, A, B, C, D, per question). The response is in the format of a table. The columns are \'Question\', \'Choices\' (only for multiple-choice questions), and \'Answer\'. All answers can be derived from the description and should be concise and accurate.\nDescription: '
    if opt.q_type == 'qa':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 6 yes/no questions, 2 what questions, and 2 how questions. The response is in the format of a table. The columns are \'Type of Question\', \'Question\' and \'Answer\'. All answers can be derived from the description and should be concise and accurate.\nDescription: '
    if opt.q_type == 'mix':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 3 yes/no questions, 3 multiple-choice questions (4 choices, A, B, C, D, per question), 2 what questions, and 2 how questions. The response is in the format of a table. The columns are \'Type of Question\', \'Question\', \'Choices\' (only for multiple-choice questions), and \'Answer\'. All questions are related to content moderation. All answers can be derived from the description and should be concise and accurate.\nDescription: '

    # inference
    for i in range(text_list_half_length):
        image_name = text_list[i * 2]
        user_content = text_list[i * 2 + 1]
        print(i, text_list_half_length, image_name)

        input_content = '[INST]<<SYS>>' + system_message + '\n<</SYS>>\n' + instruction + user_content + '[/INST]'
        
        # forward LLM with the new vllm_address parameter
        text = llm_client(input_content, True, opt.vllm_address)

        save_list = []
        save_list.append(image_name + '\n')
        save_list.append(text)
        text_save(save_list, os.path.join(save_path, '%d.txt' % i), mode='a')