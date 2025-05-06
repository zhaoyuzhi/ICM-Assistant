# -*- coding: utf-8 -*-
import os
import time
import argparse

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

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

if __name__ == "__main__":

    # using OpenAI's ChatGPT to label data
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompting_txt_path', type = str, default = './gpt-3.5-turbo-1106/train_name_list-llava-v1.5-7b-after-reasoning-30k-qa-102k-mc-74k-wh-70k-qamcwh-246k', help = 'File path')
    opt = parser.parse_args()
    print(opt)
    
    # define base
    txt_list = get_files(opt.prompting_txt_path)

    for i, txt_name in enumerate(txt_list):
        
        # extract the content from the txt_name
        txt_content = text_readlines(txt_name)
        
        # loop the txt_content
        for j in range(len(txt_content)):
            if '--' in txt_content[j] and txt_content[j].count('|') > 3:
                print(i, j, txt_name)
