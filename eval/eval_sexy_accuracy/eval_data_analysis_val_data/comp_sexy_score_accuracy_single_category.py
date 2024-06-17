import os
import json
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
    acc1 = True1 / (True1 + False1)
    return acc1

if __name__ == "__main__":

    # define folder path
    folder_path = './eval_sexy_accuracy/result_val_data'

    # read generated lists
    data_list = [
        'llava_ablation_study/llava-v1.5-7b-ab1-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab1-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-3.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-4.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-5.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-6.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-7.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-8.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-9.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-10.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-11.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-12.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-13.json',
        'llava_ablation_study/llava-v1.5-7b-ab2-14.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-3.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-4.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-5.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-6.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-7.json',
        'llava_ablation_study/llava-v1.5-7b-ab3-8.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-3.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-4.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-5.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-6.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-7.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-8.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-9.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-10.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-11.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-12.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-13.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-14.json',
        'llava_ablation_study/llava-v1.5-7b-ab4-15.json',
        'llava_ablation_study/llava-v1.5-7b-ab5-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab5-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab5-3.json',
        'llava_ablation_study/llava-v1.5-7b-ab5-4.json',
        'llava_ablation_study/llava-v1.5-7b-ab5-5.json',
        'llava_ablation_study/llava-v1.5-7b-ab6-1.json',
        'llava_ablation_study/llava-v1.5-7b-ab6-2.json',
        'llava_ablation_study/llava-v1.5-7b-ab6-3.json',
        'llava_ablation_study/llava-v1.5-7b-ab6-4.json',
        'llava_ablation_study/llava-v1.5-7b-after-baseline.json',
        'mllm_ablation_study/internlm-xcomposer2-vl-7b-after.json',
        'mllm_ablation_study/llava-sharegpt4v-7b-after.json',
        'mllm_ablation_study/llava-sharegpt4v-13b-after.json',
        'mllm_ablation_study/llava-v1.5-7b-mix.json',
        'mllm_ablation_study/llava-v1.5-13b-after.json',
        'mllm_ablation_study/llava-v1.5-13b-mix.json',
        'mllm_ablation_study/llava-v1.6-7b-after.json',
        'mllm_ablation_study/llava-v1.6-13b-after.json',
        'mllm_ablation_study/mplug-owl2-7b-after.json',
        'mllm_ablation_study/qwen-vl-chat-7b-after.json',
        'raw_network/internlm-xcomposer-7b.json',
        'raw_network/internlm-xcomposer-vl-7b.json',
        'raw_network/internlm-xcomposer2-7b.json',
        'raw_network/internlm-xcomposer2-vl-7b.json',
        'raw_network/llava-lvis-mix880k-7b.json',
        'raw_network/llava-lvis-mix880k-13b.json',
        'raw_network/llava-sharegpt4v-7b.json',
        'raw_network/llava-sharegpt4v-13b.json',
        'raw_network/llava-v1.5-7b.json',
        'raw_network/llava-v1.5-13b.json',
        'raw_network/llava-v1.6-7b.json',
        'raw_network/llava-v1.6-13b.json',
        'raw_network/mplug-owl2-7b.json',
        'raw_network/qwen-vl-chat-7b.json',
    ]

    # define all the categories and choose one you want to test
    keywords_list = ['bite_finger', 'bite_lip', 'liftup', 'lower_hips', 'lower_large_bare', 'lower_leg', 'lower_normal', 'lower_shoulders_and_belly', 'male_sexy', 'middle_crotch', 'middle_hips', 'middle_leg', 'middle_normal', 'middle_shoulders_and_belly', 'pout', 'sexy_imagetext', 'sexy_implicit', 'sexy_kiss', 'skirt', 'stockings', 'takeoff', 'tongue', 'upper_backless', 'upper_bust', 'upper_large_bare', 'upper_normal', 'upper_shoulders_and_belly', 'wearing_bras', 'wearing_stockings', 'wet', 'whole_backless', 'whole_large_bare', 'whole_leg', 'whole_normal', 'whole_shoulders_and_belly']
    gt_list = []
    for j in range(len(keywords_list)):
        if 'normal' in keywords_list[j]:
            gt_list.append(False)
        else:
            gt_list.append(True)
    
    # evaluate
    for i in range(len(keywords_list)):
        keywords = keywords_list[i]
        gt = gt_list[i]
        # loop all methods
        for j, item in enumerate(data_list):
            # read
            result_file = os.path.join(folder_path, item)
            # eval
            if os.path.exists(result_file):
                name_list, sexy_score_list = read_json_file(result_file)
                acc = conclude_single_category(name_list, sexy_score_list, keywords = keywords, gt = gt)
                # print the results
                print('The statistics of category:', keywords, item, acc)
