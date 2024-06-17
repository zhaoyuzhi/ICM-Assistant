# -*- coding: utf-8 -*-
import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch

torch.manual_seed(1234)

def main(args, conv_list):
    # Note: The default behavior now has injection attack prevention off.
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    if args.bf16:
        # use bf16
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="auto", trust_remote_code=True, bf16=True).eval()
    elif args.fp16:
        # use fp16
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="auto", trust_remote_code=True, fp16=True).eval()
    elif args.cpu:
        # use cpu only
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="cpu", trust_remote_code=True).eval()
    else:
        # use cuda device
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="cuda", trust_remote_code=True).eval()

    # Specify hyperparameters for generation
    model.generation_config = GenerationConfig.from_pretrained(args.model_path, trust_remote_code=True)

    # print
    print(args.image_file)
    
    # 1st dialogue turn
    query = tokenizer.from_list_format([
        {'image': args.image_file}, # Either a local path or an url
        {'text': conv_list[0]},
    ])
    response, history = model.chat(tokenizer, query=query, history=None)
    print('USER:', conv_list[0])
    print('ASSISTANT:', response)

    # 2nd dialogue turn
    response, history = model.chat(tokenizer, conv_list[1], history=history)
    print('USER:', conv_list[1])
    print('ASSISTANT:', response)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default='Qwen-VL-Chat', help='path to model file')
    parser.add_argument("--image-file", type=str, default='img.png', help='path to image file')
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()

    # define the multi-turn conversation list
    conv_list = [
        'Describe the image in 3 or 4 sentences.',
        'Answer following questions with only yes or no and question numbers, without repeating questions: 1. Is this image sexually suggestive?; 2. Is this image related to violence or abuse?; 3. Does this image contain abnormal or unusual content in daily life?; 4. Does this image contain porn content?; 5. Does this image contain scary or frightening content?; 6. Does this image contain violent content?; 7. Does this image contain disgusting content?; 8. Does this image contain political content?; 9. Does this image look ugly?'
    ]

    main(args, conv_list)