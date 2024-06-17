# -*- coding: utf-8 -*-
import os
import argparse
import torch
from transformers import AutoModel, AutoTokenizer

torch.set_grad_enabled(False)

def main(args, conv_list):
    # init model and tokenizer
    model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    # print
    print(args.image_file)
    
    text = '<ImageHere>' + conv_list[0]
    # 1st dialogue turn
    with torch.cuda.amp.autocast():
        response, history = model.chat(tokenizer, query=text, image=args.image_file, history=[], do_sample=False)
    print('USER:', conv_list[0])
    print('ASSISTANT:', response)
        
    # 2nd - k-th dialogue turn
    for i in range(1, len(conv_list)):
        with torch.cuda.amp.autocast():
            response, history = model.chat(tokenizer, query=conv_list[i], image=None, history=history, do_sample=False)
        print('USER:', conv_list[i])
        print('ASSISTANT:', response)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default='internlm-xcomposer-7b', help='path to model file')
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