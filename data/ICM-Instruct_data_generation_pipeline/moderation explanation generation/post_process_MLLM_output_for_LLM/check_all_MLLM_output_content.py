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

    parser = argparse.ArgumentParser()
    parser.add_argument("--base_folder_path", type=str, default='./CoT_prompts_1/all_LLaVA_results')
    parser.add_argument("--save_folder_path", type=str, default='./CoT_prompts_1/all_LLaVA_results_revised')
    args = parser.parse_args()

    # define black words
    black_word_list = ['prior information', 'prior description', 'prior knowledge', 'prior assumption', 'prior statement', 'prior prompt', 'priority information', 'based on the information', 'based on the prior']

    # run this after getting all results
    check_path(args.save_folder_path)

    # obtain all labels and results
    base_folder_path_list = get_files(args.base_folder_path)
    for i in range(len(base_folder_path_list)):
        base_path = base_folder_path_list[i]
        save_path = base_path.replace(args.base_folder_path, args.save_folder_path)
        base_list = text_readlines(base_path)
        save_list = []
        for j in range(len(base_list) // 2):
            name = base_list[j * 2]
            content = base_list[j * 2 + 1]
            # save the name and content to a new list
            save_list.append(name)
            content_split = content.split('.')
            content_split_post = []
            save_tag = True
            for k in range(len(content_split)):
                content_split_current_line = content_split[k]
                # if a black word is in the current line, delete this line
                for m in range(len(black_word_list)):
                    if black_word_list[m].lower() in content_split_current_line.lower():
                        save_tag = False
                if save_tag:
                    content_split_post.append(content_split_current_line)
                    #print(content_split_current_line)
            save_list.append('.'. join(content_split_post))
            # print the step
            print(save_path, i, j)
        # save the list
        text_save(save_list, save_path)
      
