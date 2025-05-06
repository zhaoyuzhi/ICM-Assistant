import os
import json
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

    # define folder path
    folder_path = './'

    # read generated lists
    data_list = [
        'llava-v1.5-7b-after-baseline.json',
    ]

    # evaluate
    for i, item in enumerate(data_list):

        # read
        result_file = os.path.join(folder_path, item)
        name_list, sexy_score_list = read_json_file(result_file)
        length = len(name_list)

        # analysis
        TP, FP, TN, FN = 0, 0, 0, 0
        for i in range(length):
            # for prediction is not-sexy
            if sexy_score_list[i] < 0.5:
                # for target is not-sexy
                if 'not-sexy' in name_list[i]:
                    TN += 1
                # for target is sexy
                else:
                    FN += 1
            # for prediction is sexy
            else:
                # for target is not-sexy
                if 'not-sexy' in name_list[i]:
                    FP += 1
                # for target is sexy
                else:
                    TP += 1

        # print the method name
        print(item)
        
        # calculate results and compute metrics
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        accuracy = (TP + TN) / (TP + FP + TN + FN)
        table = PrettyTable(['TP', 'FP', 'TN', 'FN', 'total', 'precision', 'recall', 'accuracy'])
        table.add_row([TP, FP, TN, FN, length, precision, recall, accuracy])
        print(table)
