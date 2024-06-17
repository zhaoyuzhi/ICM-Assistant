#!/usr/bin/env python
# coding: utf-8
import argparse
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import torch
from PIL import Image
from diffusers import AutoPipelineForText2Image
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read a txt expect EOF
def text_readlines(filename, mode = 'r'):
    # try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        # Use the following command if there is Chinese characters are read
        file = open(filename, mode, encoding = 'utf-8')
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--magicprompt_path", type=str, default='/home/zyz/pretrained_models/MagicPrompt-Stable-Diffusion')
    parser.add_argument("--sdxl_path", type=str, default='/home/zyz/pretrained_models/stable-diffusion-xl-base-1.0')
    parser.add_argument("--input_prompt_path", type=str, default='./assets/postive_prompt_list.txt')
    parser.add_argument("--save_folder_path", type=str, default='SDXL_sexy_test_data')
    parser.add_argument("--num_of_images_per_class", type=int, default=20)
    args = parser.parse_args()

    # -------------------------------------------------------------------------------------
    # define models and pipelines
    magicprompt_tokenizer = GPT2Tokenizer.from_pretrained(args.magicprompt_path)
    magicprompt_model = GPT2LMHeadModel.from_pretrained(args.magicprompt_path, pad_token_id=magicprompt_tokenizer.eos_token_id)
    magicprompt_pipe = pipeline(
        'text-generation', model=magicprompt_model, tokenizer=magicprompt_tokenizer, max_new_tokens=100
    )

    sdxl_pipe_text2image = AutoPipelineForText2Image.from_pretrained(
        args.sdxl_path, torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    ).to("cuda")

    # -------------------------------------------------------------------------------------
    # forward
    input_short_description_list = text_readlines(args.input_prompt_path)
    
    for i, input_short_description in enumerate(input_short_description_list):
        # create save_folder
        save_sub_folder_path = os.path.join(args.save_folder_path, input_short_description)
        check_path(save_sub_folder_path)
        # MagicPrompt
        out = magicprompt_pipe(input_short_description)[0]['generated_text'].replace('\n', '')
        # SDXL
        fix_prompts = ', detailed, 8k'
        prompt = out + fix_prompts
        for j in range(args.num_of_images_per_class):
            save_image_path = os.path.join(save_sub_folder_path, str(j).zfill(5) + '.jpg')
            image = sdxl_pipe_text2image(prompt=prompt).images[0]
            image.save(save_image_path)
