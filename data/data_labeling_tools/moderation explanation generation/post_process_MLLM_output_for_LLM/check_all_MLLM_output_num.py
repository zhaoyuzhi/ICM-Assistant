# -*- coding: utf-8 -*-
import os
import argparse

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

# read a folder, return all the file names
def get_filespaths(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(filespath)
    return ret

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

if __name__ == '__main__':
    
    # run this after getting all results
    base_folder_path_list = ['./CoT_prompts_2/all_LLaVA_results', './CoT_prompts_3/all_LLaVA_results', './CoT_prompts_4/all_LLaVA_results', './CoT_prompts_5/all_LLaVA_results', './CoT_prompts/all_LLaVA_results']

    # obtain all labels and results
    all_labels = []
    base_l = get_files(base_folder_path_list[0])
    for j in range(len(base_l)):
        all_labels.append(base_l[j].split('\\')[-1].split('.txt')[0])
    all_results = [[] for _ in range(len(base_l))]
    print(all_labels)

    # conclude the number of images, according to labels
    for i in range(len(base_folder_path_list)):
        base_l = get_files(base_folder_path_list[i])
        for j in range(len(base_l)):
            base_len = len(text_readlines(base_l[j]))
            all_results[j].append(base_len)
    print(all_results)
    
