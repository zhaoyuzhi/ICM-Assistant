import os
from shutil import copyfile, move
import json

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

# read a json file, return the contents
def read_json_file(result_file):
    name_list = []
    sexy_score_list = []
    with open(result_file) as f:
        file_list = json.load(f)
    for i, file_item in enumerate(file_list):
        image_name = file_item["image_name"]
        sexy_score = file_item["sexy_score"]
        name_list.append(image_name)
        sexy_score_list.append(sexy_score)
    return name_list, sexy_score_list

# find the ground truth label
def conclude_one_item(sexy_score, thres = 0.5, gt = True):
    if sexy_score > thres and gt == True:
        result = 'TP'
    if sexy_score <= thres and gt == True:
        result = 'FN'
    if sexy_score > thres and gt == False:
        result = 'FP'
    if sexy_score <= thres and gt == False:
        result = 'TN'
    return result

# conclude the true or false prediction on one category
def conclude_single_category(name_list, sexy_score_list1, sexy_score_list2, sexy_score_list3, sexy_score_list4, sexy_score_list5, sexy_score_list6, keywords = 'leg_neg', thres = 0.5, gt = True):
    False1, True1, False2, True2, False3, True3, False4, True4, False5, True5, False6, True6 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(len(name_list)):
        if keywords in name_list[i]:
            if conclude_one_item(sexy_score_list1[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list1[i], thres, gt) == 'TN':
                True1 += 1
            else:
                False1 += 1
            if conclude_one_item(sexy_score_list2[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list2[i], thres, gt) == 'TN':
                True2 += 1
            else:
                False2 += 1
            if conclude_one_item(sexy_score_list3[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list3[i], thres, gt) == 'TN':
                True3 += 1
            else:
                False3 += 1
            if conclude_one_item(sexy_score_list4[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list4[i], thres, gt) == 'TN':
                True4 += 1
            else:
                False4 += 1
            if conclude_one_item(sexy_score_list5[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list5[i], thres, gt) == 'TN':
                True5 += 1
            else:
                False5 += 1
                print('False:', name_list[i])
            if conclude_one_item(sexy_score_list6[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list6[i], thres, gt) == 'TN':
                True6 += 1
            else:
                False6 += 1
                print('False:', name_list[i])
    return False1, True1, False2, True2, False3, True3, False4, True4, False5, True5, False6, True6

def conclude_all_category(name_list, sexy_score_list1, sexy_score_list2, sexy_score_list3, sexy_score_list4, sexy_score_list5, sexy_score_list6, keywords_list, thres, gt_list):
    overall_False1, overall_True1, overall_False2, overall_True2, overall_False3, overall_True3, overall_False4, overall_True4, overall_False5, overall_True5, overall_False6, overall_True6 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(len(keywords_list)):
        False1, True1, False2, True2, False3, True3, False4, True4, False5, True5, False6, True6 = conclude_single_category(name_list, sexy_score_list1, sexy_score_list2, sexy_score_list3, sexy_score_list4, sexy_score_list5, sexy_score_list6, keywords = keywords_list[i], thres = thres, gt = gt_list[i])
        overall_False1 += False1
        overall_True1 += True1
        overall_False2 += False2
        overall_True2 += True2
        overall_False3 += False3
        overall_True3 += True3
        overall_False4 += False4
        overall_True4 += True4
        overall_False5 += False5
        overall_True5 += True5
        overall_False6 += False6
        overall_True6 += True6
    acc1 = overall_True1 / (overall_True1 + overall_False1)
    acc2 = overall_True2 / (overall_True2 + overall_False2)
    acc3 = overall_True3 / (overall_True3 + overall_False3)
    acc4 = overall_True4 / (overall_True4 + overall_False4)
    acc5 = overall_True5 / (overall_True5 + overall_False5)
    acc6 = overall_True6 / (overall_True6 + overall_False6)
    return acc1, acc2, acc3, acc4, acc5, acc6

if __name__ == "__main__":

    # define the input jsons
    result_file = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-1.json'
    
    result_file_split = result_file.split('/')[-1].split('.json')[0]

    # obtain all data
    name_list, sexy_score_list = read_json_file(result_file)

    # ---------------------------------------------------------------

    # define the read and save paths
    read_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data\\data\\val_all'
    save_path = result_file_split
    check_path(save_path)

    # ---------------------------------------------------------------

    # Draw tables
    for i in range(len(name_list)):
        name = name_list[i]
        sexy_score = sexy_score_list[i]
        if (sexy_score < 0.5 and 'normal' not in name) or (sexy_score >= 0.5 and 'normal' in name):
            print(name, sexy_score)
            path1 = os.path.join(read_path, name)
            path2 = os.path.join(save_path, name)
            copyfile(path1, path2)
            