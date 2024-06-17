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

def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

def main(args):
    
    # init model and tokenizer
    model = AutoModel.from_pretrained(args.model_path, trust_remote_code=True).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    model.tokenizer = tokenizer
    
    # read list_file
    # image path for odd-numbered actions, multi-turn dialogue for even-numbered actions
    list_file = text_readlines(args.list_file)
    num_of_samples = len(list_file) // 2

    for image_id in range(num_of_samples):

        # define the image file and conversations
        image_relative_file = list_file[image_id * 2]
        image_file = os.path.join(args.folder_file, image_relative_file)
        save_full_path = os.path.join(args.save_file, image_relative_file).split('.')[0] + '.txt'
        save_folder_path = '/'.join(save_full_path.split('/')[:-1])
        check_path(save_folder_path)

        conv = list_file[image_id * 2 + 1]
        conv_list = conv.split('\t')

        save_list = []

        # append information to save_list
        save_list.append(image_relative_file)
        
        # print
        print(image_relative_file)
        
        # 1st dialogue turn
        response, history = model.chat(text=conv_list[0], image=image_file, history=None)
        print(response)
        
        # append information to save_list
        save_list.append(conv_list[0])
        save_list.append(response)

        # 2nd - k-th dialogue turn
        for i in range(1, len(conv_list)):
            response, history = model.chat(text=conv_list[i], image=None, history=history)
            # print('USER:', conv_list[i])
            # print('ASSISTANT:', response)
            print(response)

            # append information to save_list
            save_list.append(conv_list[i])
            save_list.append(response)

        # save save_list to file
        # text_save(save_list, save_full_path)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="internlm-xcomposer-7b")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--folder-file", type=str, required=True)
    parser.add_argument("--list-file", type=str, default='list_file.txt', help='multiple questions are divided by \t')
    parser.add_argument("--save-file", type=str, default='save_folder')
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--conv-mode", type=str, default=None)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    main(args)
