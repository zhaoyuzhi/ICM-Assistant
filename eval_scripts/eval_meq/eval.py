# -*- coding: utf-8 -*-
import glob
import os
import numpy as np

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

# read all the txt files under a folder, return four lists
def get_all_acc(prompting_txt_path):

    # define base
    txt_list = get_files(prompting_txt_path)
    print(txt_list)

    # define 3 lists for saving
    Accuracy_list = []
    Preciseness_list = []
    Comprehensiveness_list = []
    Fluency_list = []

    for i, txt_name in enumerate(txt_list):
        
        # extract the content from the txt_name
        txt_content = text_readlines(txt_name)
        
        # loop the txt_content
        begin_id = 100000 # should be larger than max_length of LLM
        for j in range(len(txt_content)):
            if '--' in txt_content[j]:
                begin_id = j
            if j > begin_id and '|' in txt_content[j] and txt_content[j].count('|') == 3:
                if 'Accuracy' in txt_content[j]:
                    cur_Accuracy = int(txt_content[j].split('|')[-2].strip())
                if 'Preciseness' in txt_content[j]:
                    cur_Preciseness = int(txt_content[j].split('|')[-2].strip())
                if 'Comprehensiveness' in txt_content[j]:
                    cur_Comprehensiveness = int(txt_content[j].split('|')[-2].strip())
                if 'Fluency' in txt_content[j]:
                    cur_Fluency = int(txt_content[j].split('|')[-2].strip())
        
        # append
        try:
            Accuracy_list.append(cur_Accuracy)
            Preciseness_list.append(cur_Preciseness)
            Comprehensiveness_list.append(cur_Comprehensiveness)
            Fluency_list.append(cur_Fluency)
        except:
            Accuracy_list.append(0)
            Preciseness_list.append(0)
            Comprehensiveness_list.append(0)
            Fluency_list.append(0)

    # print
    Accuracy_score = np.sum(np.array(Accuracy_list)) / len(txt_list)
    Preciseness_score = np.sum(np.array(Preciseness_list)) / len(txt_list)
    Comprehensiveness_score = np.sum(np.array(Comprehensiveness_list)) / len(txt_list)
    Fluency_score = np.sum(np.array(Fluency_list)) / len(txt_list)

    # packing
    assert len(txt_list) == len(Accuracy_list)
    assert len(txt_list) == len(Preciseness_list)
    assert len(txt_list) == len(Comprehensiveness_list)
    assert len(txt_list) == len(Accuracy_list)
    return_dic = {
        'txt_list': txt_list,
        'Accuracy_list': Accuracy_list,
        'Preciseness_list': Preciseness_list,
        'Comprehensiveness_list': Comprehensiveness_list,
        'Fluency_list': Fluency_list,
        'Accuracy_score': Accuracy_score,
        'Preciseness_score': Preciseness_score,
        'Comprehensiveness_score': Comprehensiveness_score,
        'Fluency_score': Fluency_score,
    }
        
    return return_dic

if __name__ == "__main__":

    # define folder path
    gt_mc_a_prompts_path = './'

    data_list = [

        'llava-v1.5-7b-after-baseline',

    ]

    # evaluate
    for i, item in enumerate(data_list):
        # read
        prompting_txt_path = os.path.join(gt_mc_a_prompts_path, item)
        # eval
        return_dic = get_all_acc(prompting_txt_path)
        # print the results
        print(item)
        print(return_dic['Accuracy_score'], return_dic['Preciseness_score'], return_dic['Comprehensiveness_score'], return_dic['Fluency_score'])
