# -*- coding: utf-8 -*-
import os
import argparse
import torch
from transformers import AutoModel, AutoTokenizer

torch.set_grad_enabled(False)

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

def main(args, conv_list):
    # define image list
    image_list = get_files(args.folder_file)

    # init model and tokenizer
    model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    model.tokenizer = tokenizer

    for image_id, image_file in enumerate(image_list):

        # define the image file
        image_relative_file = image_file.replace(args.folder_file, '')
        save_full_path = image_file.replace(args.folder_file, args.save_file).split('.')[0] + '.txt'
        save_folder_path = '/'.join(save_full_path.split('/')[:-1])
        check_path(save_folder_path)
        
        save_list = []

        # append information to save_list
        save_list.append(image_relative_file)
        
        # print
        print(image_relative_file)

        # 1st dialogue turn
        response, history = model.chat(text=conv_list[0], image=image_file, history=None)
        print('USER:', conv_list[0])
        print('ASSISTANT:', response)

        # append information to save_list
        save_list.append(conv_list[0])
        save_list.append(response)

        # 2nd - k-th dialogue turn
        for i in range(1, len(conv_list)):
            response, history = model.chat(text=conv_list[i], image=None, history=history)
            print('USER:', conv_list[i])
            print('ASSISTANT:', response)

            # append information to save_list
            save_list.append(conv_list[i])
            save_list.append(response)
        
        # save save_list to file
        text_save(save_list, save_full_path)
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default='internlm-xcomposer-7b', help='path to model file')
    parser.add_argument("--folder-file", type=str, default='img', help='path to all image files')
    parser.add_argument("--save-file", type=str, default='save_folder')
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()

    # define the caption
    conv_list = [
        'Describe the image in detail.'
    ]

    # define the multi-turn conversation list
    conv_list = [
        'Describe the image in 3 or 4 sentences.',
        'Answer following questions with only yes or no and question numbers, without repeating questions: 1. Is this image sexually suggestive?; 2. Is this image related to violence or abuse?; 3. Does this image contain abnormal or unusual content in daily life?; 4. Does this image contain porn content?; 5. Does this image contain scary or frightening content?; 6. Does this image contain violent content?; 7. Does this image contain disgusting content?; 8. Does this image contain political content?; 9. Does this image look ugly?'
    ]

    main(args, conv_list)