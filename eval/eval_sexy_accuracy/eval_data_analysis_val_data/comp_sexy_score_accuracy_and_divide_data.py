import os
import json
from shutil import copyfile, move
from prettytable import PrettyTable

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

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":

    # define the input jsons
    base_path = 'D:\\dataset\\advertisement_data\\data\\val'
    result_file = './eval_sexy_accuracy/result_val_data/llava_ablation_study/llava-v1.5-7b-after-baseline.json'
    
    # read the json
    name_list, sexy_score_list = read_json_file(result_file)
    length = len(name_list)
    
    # define the save path
    save_path = result_file.split('/')[-1].split('.json')[0]
    check_path(os.path.join(save_path, 'TP'))
    check_path(os.path.join(save_path, 'FP'))
    check_path(os.path.join(save_path, 'TN'))
    check_path(os.path.join(save_path, 'FN'))

    # analysis
    TP, FP, TN, FN = 0, 0, 0, 0
    for i in range(length):
        # define the source path
        path1 = os.path.join(base_path, name_list[i].split('/')[-1].split('_')[0], name_list[i].split('/')[-1])
        # for prediction is not-sexy
        if sexy_score_list[i] < 0.5:
            # for target is not-sexy
            if 'not-sexy' in name_list[i]:
                TN += 1
            # for target is sexy
            else:
                FN += 1
                path2 = os.path.join(save_path, 'FN', name_list[i].split('/')[-1])
                copyfile(path1, path2)
        # for prediction is sexy
        else:
            # for target is not-sexy
            if 'not-sexy' in name_list[i]:
                FP += 1
                path2 = os.path.join(save_path, 'FP', name_list[i].split('/')[-1])
                copyfile(path1, path2)
            # for target is sexy
            else:
                TP += 1
    
    # print the method name
    print(save_path)
    
    # calculate results and compute metrics
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    accuracy = (TP + TN) / (TP + FP + TN + FN)
    table = PrettyTable(['TP', 'FP', 'TN', 'FN', 'total', 'precision', 'recall', 'accuracy'])
    table.add_row([TP, FP, TN, FN, length, precision, recall, accuracy])
    print(table)
