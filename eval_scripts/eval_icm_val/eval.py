import os
import json
import matplotlib.pyplot as plt
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

# read a folder, return all the sub-folders
def get_dirs(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            category = os.path.join(root, filespath).split('\\')[-2]
            if category not in ret:
                ret.append(category)
    return sorted(ret)

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
def conclude_single_category(name_list1, sexy_score_list1, keywords = 'whole_normal', thres = 0.5, gt = True):
    False1, True1 = 0, 0
    for i in range(len(name_list1)):
        if keywords in name_list1[i]:
            if conclude_one_item(sexy_score_list1[i], thres, gt) == 'TP' or conclude_one_item(sexy_score_list1[i], thres, gt) == 'TN':
                True1 += 1
            else:
                False1 += 1
    return False1, True1

# conclude the true or false prediction on all categories
def conclude_all_category(name_list, sexy_score_list1, keywords_list, thres, gt_list):
    overall_False1, overall_True1 = 0, 0
    for i in range(len(keywords_list)):
        False1, True1 = conclude_single_category(name_list, sexy_score_list1, keywords = keywords_list[i], thres = thres, gt = gt_list[i])
        overall_False1 += False1
        overall_True1 += True1
    acc1 = overall_True1 / (overall_True1 + overall_False1)
    return acc1



# get the accuracy from a json file
def get_acc(result_file):
    # --------------------------------------------------------------------------------
    # Draw tables
    keywords_list = ['bite_finger', 'bite_lip', 'liftup', 'lower_hips', 'lower_large_bare', 'lower_leg', 'lower_normal', 'lower_shoulders_and_belly', 'male_sexy', 'middle_crotch', 'middle_hips', 'middle_leg', 'middle_normal', 'middle_shoulders_and_belly', 'pout', 'sexy_imagetext', 'sexy_implicit', 'sexy_kiss', 'skirt', 'stockings', 'takeoff', 'tongue', 'upper_backless', 'upper_bust', 'upper_large_bare', 'upper_normal', 'upper_shoulders_and_belly', 'wearing_bras', 'wearing_stockings', 'wet', 'whole_backless', 'whole_large_bare', 'whole_leg', 'whole_normal', 'whole_shoulders_and_belly']
    gt_list = []
    for j in range(len(keywords_list)):
        if 'normal' in keywords_list[j]:
            gt_list.append(False)
        else:
            gt_list.append(True)
    # --------------------------------------------------------------------------------
    # split the name
    result_file_split = result_file.split('/')[-1].split('.json')[0]
    # obtain all data
    name_list, sexy_score_list = read_json_file(result_file)
    # get the accuracy
    acc = conclude_all_category(name_list, sexy_score_list, keywords_list = keywords_list, thres = 0.5, gt_list = gt_list)
    return result_file_split, acc

if __name__ == "__main__":

    # define folder path
    folder_path = './'

    # read generated lists
    data_list = [
        '/llava-v1.5-7b-after-baseline.',
    ]

    # evaluate
    for i, item in enumerate(data_list):
        # read
        result_file = os.path.join(folder_path, item)
        # eval
        if os.path.exists(result_file):
            result_file_split, acc = get_acc(result_file)
            # print the results
            print(item)
            print(acc)
