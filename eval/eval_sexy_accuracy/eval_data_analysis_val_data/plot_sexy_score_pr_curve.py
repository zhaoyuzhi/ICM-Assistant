import os
import json
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

# find the ground truth label
def search_gt(image_name):
    if 'normal' in image_name or 'no_person' in image_name or 'negative' in image_name:
        return 'No'
    else:
        return 'Yes'

# plot the pr curve
def validate_pr_curve(result_file):
    with open(result_file) as f:
        file_list = json.load(f)
    precision_list = []
    recall_list = []
    for t in range(1, 100):
        thres = t / 100.
        TP, TN, FP, FN = 0, 0, 0, 0
        for q in file_list:
            image_name = q["image_name"]
            sexy_score = q["sexy_score"]
            gt = search_gt(image_name)
            #print(sexy_score, gt)
            if sexy_score > thres and gt == 'Yes':
                TP += 1
            if sexy_score <= thres and gt == 'No':
                TN += 1
            if sexy_score > thres and gt == 'No':
                FP += 1
            if sexy_score <= thres and gt == 'Yes':
                FN += 1
        precision = TP * 1. / (TP + FP + 0.0001)
        recall = TP * 1. / (TP + FN + 0.0001)
        precision_list.append(precision)
        recall_list.append(recall)
    return precision_list, recall_list

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
    
    # compute the precision values, recall values, and obtain name_list, sexy_score_list
    precision_list1, recall_list1 = validate_pr_curve(result_file1)
    precision_list2, recall_list2 = validate_pr_curve(result_file2)
    precision_list3, recall_list3 = validate_pr_curve(result_file3)
    precision_list4, recall_list4 = validate_pr_curve(result_file4)
    precision_list5, recall_list5 = validate_pr_curve(result_file5)
    precision_list6, recall_list6 = validate_pr_curve(result_file6)
    
    name_list, sexy_score_list = read_json_file(result_file1)
    length = len(name_list)

    # ---------------------------------------------------------------

    # Draw pictures
    plt.title("P-R Curve on %d data" % length)
    plt.xlabel("Recall Value")
    plt.ylabel("Precision Value")
    plt.xlim((0.9, 1.02))
    plt.ylim((0.9, 1.02))
    plt.plot(recall_list1, precision_list1, color = 'hotpink', marker = ".", label = result_file1_split)
    plt.plot(recall_list2, precision_list2, color = 'black', marker = ".", label = result_file2_split)
    plt.plot(recall_list3, precision_list3, color = 'green', marker = ".", label = result_file3_split)
    plt.plot(recall_list4, precision_list4, color = 'blue', marker = ".", label = result_file4_split)
    plt.plot(recall_list5, precision_list5, color = 'red', marker = ".", label = result_file5_split)
    plt.plot(recall_list6, precision_list6, color = 'yellow', marker = ".", label = result_file6_split)
    plt.legend()
    plt.show()
    