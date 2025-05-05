# -*- coding: utf-8 -*-
import os
import json
from typing import List, Optional
from transformers import AutoTokenizer
import transformers
import torch
import time
import argparse

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding='utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read a txt expect EOF
def text_readlines(filename, mode = 'r'):
    # try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        # Use the following command if there is Chinese characters are read
        file = open(filename, mode, encoding='utf-8')
        # file = open(filename, mode)
    except IOError:
        error = []
        return error
    content = file.readlines()
    # This for loop deletes the EOF (like \n)
    for i in range(len(content)):
        content[i] = content[i][:len(content[i]) - 1]
    file.close()
    return content

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# call LLM
def llm_client(
    pipeline,
    tokenizer,
    prompt,
    top_k = 10,
    num_return_sequences = 1,
    max_length = 2048,
):
    sequences = pipeline(
        prompt,
        do_sample = True,
        top_k = top_k,
        num_return_sequences = num_return_sequences,
        eos_token_id = tokenizer.eos_token_id,
        max_length = max_length,
    )
    
    out = ''
    for seq in sequences:
        out += seq['generated_text']
    
    return out

if __name__ == '__main__':

    # using Meta's LLaMA 2 to label data
    # Note:
    # if running on 2 A800 GPU cards, the program takes around 67000 Mb memory on each card
    # if running on 4 A800 GPU cards, the program takes around 33500 Mb memory on each card
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type = str, default = '/home/zyz/pretrained_models/llama-2-70b-chat-hf', help = 'Model path')
    parser.add_argument('--txt_path', type = str, default = '/home/zyz/pretrained_models/llama-2-70b-chat-hf', help = 'File path')
    parser.add_argument('--q_type', default = 'mix', choices = ['mc', 'qa', 'mix'], help = 'The choices of prompting')
    opt = parser.parse_args()
    print(opt)

    # define base
    tokenizer = AutoTokenizer.from_pretrained(opt.model_path)
    pipeline = transformers.pipeline(
        "text-generation",
        model=opt.model_path,
        torch_dtype=torch.float16,
        device_map="auto",
    )

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
        #instruction = 'You are an image content moderator who can analyze a single image. You receive a long description of an image. Your task is to analyze and rewrite the provided long description using a specific format.\nThe format includes 3 long sentences. The first long sentence is a brief description of the image. The second long sentence is the reason why this image is sexy (e.g., Because ..., this image is a sexy image.) The third long sentence is a conclusion of the image\'s atmosphere and the sexy level of this image. Each long sentence is not longer than two sentences.\nLong description: '
    
    # inference
    for i in range(text_list_half_length):

        # extract the image_name and user_content
        image_name = text_list[i*2]
        user_content = text_list[i*2+1]
        print(i, text_list_half_length, image_name)

        # define the specific format of input prompt
        input_content = '[INST]<<SYS>>' + system_message + '\n<</SYS>>\n' + instruction + user_content + '[/INST]'

        # forward LLM
        text = llm_client(pipeline, tokenizer, prompt = input_content)
        text = text.replace(input_content, '')

        # save the generated contents to a file
        save_list = []
        save_list.append(image_name + '\n')
        save_list.append(text)
        text_save(save_list, os.path.join(save_path, '%d.txt' % i), mode = 'a')
        