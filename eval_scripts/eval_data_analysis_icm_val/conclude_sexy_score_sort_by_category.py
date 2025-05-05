import os
import json
import numpy as np
import prettytable as pt

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

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

# read and process json files
def read_and_process_json_file(result_file, category_list):
    name_list = []
    sexy_score_list = []
    sexy_score_by_category_list = [[] for i in range(len(category_list))]
    sexy_score_avg_list = []
    sexy_score_std_list = []
    with open(result_file) as f:
        file_list = json.load(f)
    # process original data
    for i, file_item in enumerate(file_list):
        image_name = file_item["image_name"]
        sexy_score = file_item["sexy_score"]
        for j in range(len(category_list)):
            if category_list[j] == image_name.split('_202')[0]:
                sexy_score_by_category_list[j].append(sexy_score)
        name_list.append(image_name)
        sexy_score_list.append(sexy_score)
    # post-process asexy_score_by_category_list
    for k in range(len(category_list)):
        avg = np.mean(sexy_score_by_category_list[k])
        std = np.std(sexy_score_by_category_list[k])
        sexy_score_avg_list.append(avg)
        sexy_score_std_list.append(std)
    return name_list, sexy_score_list, sexy_score_by_category_list, sexy_score_avg_list, sexy_score_std_list

# find the ground truth label
def get_all_categories(result_file):
    category_list = []
    with open(result_file) as f:
        file_list = json.load(f)
    for i, file_item in enumerate(file_list):
        image_name = file_item["image_name"]
        category_name = image_name.split('_202')[0]
        if category_name not in category_list:
            category_list.append(category_name)
    return category_list

# list to dic
def list_to_dic(category_list, in_list):
    out_dic = {}
    for i in range(len(in_list)):
        out_dic[category_list[i]] = in_list[i]
    return out_dic

# sort the category_list
def sort_category_list(sexy_score_avg_list, category_list, reverse = True):
    _, sorted_category_list = zip(*sorted(zip(sexy_score_avg_list, category_list), reverse = reverse))
    sorted_category_list = list(sorted_category_list)
    sorted_category_str = ''
    for i in range(len(sorted_category_list)):
        sorted_category_str = sorted_category_str + str(i + 1) + '. '
        sorted_category_str = sorted_category_str + sorted_category_list[i] + ';'
        if i == len(sorted_category_list) // 2:
            sorted_category_str = sorted_category_str + '\n'
        else:
            sorted_category_str = sorted_category_str + ' '
    return sorted_category_list, sorted_category_str

# re-sort the list based on the sequence of sorted_category_list
def resort_list(sorted_category_list, in_dic):
    out_list = []
    for i in range(len(sorted_category_list)):
        out_list.append(in_dic[sorted_category_list[i]])
    return out_list

if __name__ == "__main__":

    # define the input jsons
    result_file1 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-1.json'
    result_file2 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-2.json'
    result_file3 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-3.json'
    result_file4 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-4.json'
    result_file5 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-5.json'
    result_file6 = './eval_sexy_classification_and_score/eval_sexy_classification_and_score_val_data/llava_ablation_study/llava-v1.5-7b-ab2-6.json'
    
    result_file1_split = result_file1.split('/')[-1].split('.json')[0]
    result_file2_split = result_file2.split('/')[-1].split('.json')[0]
    result_file3_split = result_file3.split('/')[-1].split('.json')[0]
    result_file4_split = result_file4.split('/')[-1].split('.json')[0]
    result_file5_split = result_file5.split('/')[-1].split('.json')[0]
    result_file6_split = result_file6.split('/')[-1].split('.json')[0]

    # ---------------------------------------------------------------
    
    # obtain all data
    category_list = get_all_categories(result_file1)

    name_list1, sexy_score_list1, sexy_score_by_category_list1, sexy_score_avg_list1, sexy_score_std_list1 = read_and_process_json_file(result_file1, category_list)
    sexy_score_avg_dic1 = list_to_dic(category_list, sexy_score_avg_list1)
    sexy_score_std_dic1 = list_to_dic(category_list, sexy_score_std_list1)
    
    name_list2, sexy_score_list2, sexy_score_by_category_list2, sexy_score_avg_list2, sexy_score_std_list2 = read_and_process_json_file(result_file2, category_list)
    sexy_score_avg_dic2 = list_to_dic(category_list, sexy_score_avg_list2)
    sexy_score_std_dic2 = list_to_dic(category_list, sexy_score_std_list2)

    name_list3, sexy_score_list3, sexy_score_by_category_list3, sexy_score_avg_list3, sexy_score_std_list3 = read_and_process_json_file(result_file3, category_list)
    sexy_score_avg_dic3 = list_to_dic(category_list, sexy_score_avg_list3)
    sexy_score_std_dic3 = list_to_dic(category_list, sexy_score_std_list3)

    name_list4, sexy_score_list4, sexy_score_by_category_list4, sexy_score_avg_list4, sexy_score_std_list4 = read_and_process_json_file(result_file4, category_list)
    sexy_score_avg_dic4 = list_to_dic(category_list, sexy_score_avg_list4)
    sexy_score_std_dic4 = list_to_dic(category_list, sexy_score_std_list4)

    name_list5, sexy_score_list5, sexy_score_by_category_list5, sexy_score_avg_list5, sexy_score_std_list5 = read_and_process_json_file(result_file5, category_list)
    sexy_score_avg_dic5 = list_to_dic(category_list, sexy_score_avg_list5)
    sexy_score_std_dic5 = list_to_dic(category_list, sexy_score_std_list5)

    name_list6, sexy_score_list6, sexy_score_by_category_list6, sexy_score_avg_list6, sexy_score_std_list6 = read_and_process_json_file(result_file6, category_list)
    sexy_score_avg_dic6 = list_to_dic(category_list, sexy_score_avg_list6)
    sexy_score_std_dic6 = list_to_dic(category_list, sexy_score_std_list6)

    # ---------------------------------------------------------------
    
    sorted_category_list1, sorted_category_str1 = sort_category_list(sexy_score_avg_list1, category_list, reverse = True)
    sorted_category_list2, sorted_category_str2 = sort_category_list(sexy_score_avg_list2, category_list, reverse = True)
    sorted_category_list3, sorted_category_str3 = sort_category_list(sexy_score_avg_list3, category_list, reverse = True)
    sorted_category_list4, sorted_category_str4 = sort_category_list(sexy_score_avg_list4, category_list, reverse = True)
    sorted_category_list5, sorted_category_str5 = sort_category_list(sexy_score_avg_list5, category_list, reverse = True)
    sorted_category_list6, sorted_category_str6 = sort_category_list(sexy_score_avg_list5, category_list, reverse = True)

    tb = pt.PrettyTable()
    tb.field_names = ["Index", result_file1_split, result_file2_split, result_file3_split, result_file4_split, result_file5_split, result_file6_split]
    for i in range(len(sorted_category_list1)):
        tb.add_row([str(i + 1), sorted_category_list1[i], sorted_category_list2[i], sorted_category_list3[i], sorted_category_list4[i], sorted_category_list5[i], sorted_category_list6[i]])
    print(tb)
    