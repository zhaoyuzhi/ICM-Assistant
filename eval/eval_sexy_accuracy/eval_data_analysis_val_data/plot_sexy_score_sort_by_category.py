import os
import json
import numpy as np
import matplotlib.pyplot as plt

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
        if i == len(sorted_category_list) - 1:
            sorted_category_str = sorted_category_str + sorted_category_list[i]
        else:
            sorted_category_str = sorted_category_str + sorted_category_list[i] + ';'
        if i == len(sorted_category_list) // 2:
            sorted_category_str = sorted_category_str + '\n'
        elif i < len(sorted_category_list) - 1:
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
    
    # This function obtains the sequence of categories sorted by sexy level
    # It is based on the average sexy score output by the MLLM
    sorted_category_list, sorted_category_str = sort_category_list(sexy_score_avg_list4, category_list, reverse = True)

    # Manually define the sequence of categories sorted by sexy level
    sorted_category_list = ['whole_large_bare', 'upper_large_bare', 'lower_large_bare', 'male_sexy', 'whole_backless', 'upper_backless', 'upper_bust', 'sexy_kiss', 'lower_hips', 'middle_hips', 'stockings', 'middle_crotch', 'upper_shoulders_and_belly', 'lower_shoulders_and_belly', 'middle_shoulders_and_belly', 'whole_leg', 'lower_leg', 'middle_leg', 'middle_normal', 'lower_normal', 'upper_normal', 'whole_normal']
    print(len(sorted_category_list))
    sorted_category_str = ''
    for i in range(len(sorted_category_list)):
        sorted_category_str = sorted_category_str + str(i + 1) + '. '
        if i == len(sorted_category_list) - 1:
            sorted_category_str = sorted_category_str + sorted_category_list[i]
        else:
            sorted_category_str = sorted_category_str + sorted_category_list[i] + ';'
        if i == len(sorted_category_list) // 2:
            sorted_category_str = sorted_category_str + '\n'
        elif i < len(sorted_category_list) - 1:
            sorted_category_str = sorted_category_str + ' '

    # ---------------------------------------------------------------
    
    # Draw pictures
    sorted_sexy_score_avg_dic1 = resort_list(sorted_category_list, sexy_score_avg_dic1)
    sorted_sexy_score_avg_dic2 = resort_list(sorted_category_list, sexy_score_avg_dic2)
    sorted_sexy_score_avg_dic3 = resort_list(sorted_category_list, sexy_score_avg_dic3)
    sorted_sexy_score_avg_dic4 = resort_list(sorted_category_list, sexy_score_avg_dic4)
    sorted_sexy_score_avg_dic5 = resort_list(sorted_category_list, sexy_score_avg_dic5)
    sorted_sexy_score_avg_dic6 = resort_list(sorted_category_list, sexy_score_avg_dic6)

    plt.title("Average Sexy Score on %d data" % len(name_list1))
    plt.xlabel("Categories, sorted by %s" % sorted_category_str, size = 7)
    plt.ylabel("Average Sexy Score")
    plt.plot(sorted_sexy_score_avg_dic1, color = 'hotpink', marker = "^", label = result_file1_split)
    plt.plot(sorted_sexy_score_avg_dic2, color = 'black', marker = "^", label = result_file2_split)
    plt.plot(sorted_sexy_score_avg_dic3, color = 'green', marker = "1", label = result_file3_split)
    plt.plot(sorted_sexy_score_avg_dic4, color = 'blue', marker = "8", label = result_file4_split)
    plt.plot(sorted_sexy_score_avg_dic5, color = 'red', marker = "s", label = result_file5_split)
    plt.plot(sorted_sexy_score_avg_dic6, color = 'yellow', marker = ",", label = result_file6_split)
    for j in range(len(sorted_sexy_score_avg_dic1)):
        plt.text(j + 0.05, sorted_sexy_score_avg_dic4[j] - 0.05, j, fontsize = 10, color = "blue", style = "italic", weight = "light", verticalalignment = 'center', horizontalalignment = 'right', rotation = 0)
        plt.text(j + 0.05, sorted_sexy_score_avg_dic5[j] + 0.05, j, fontsize = 10, color = "red", style = "italic", weight = "light", verticalalignment = 'center', horizontalalignment = 'right', rotation = 0)
    plt.legend()
    plt.show()

    '''
    plt.title('Dictionary Scatter Plot')
    plt.xlabel('Keys')
    plt.ylabel('Values')
    keys = sexy_score_avg_dic1.keys()
    values = sexy_score_avg_dic1.values()
    plt.scatter(keys, values)
    plt.show()
    '''
