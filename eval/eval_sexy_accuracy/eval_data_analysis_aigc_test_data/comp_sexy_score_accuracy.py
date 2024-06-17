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
    folder_path = './eval_sexy_accuracy/result_aigc_test_data'

    # read generated lists
    data_list_comparison_with_other_methods = [
        'llava_ablation_study/llava-v1.5-7b-after-baseline.json',
        'raw_network/llava-v1.5-7b.json',
        'raw_network/llava-v1.5-13b.json',
        'raw_network/llava-sharegpt4v-7b.json',
        'raw_network/llava-sharegpt4v-13b.json',
        'raw_network/llava-lvis-mix880k-7b.json',
        'raw_network/llava-lvis-mix880k-13b.json',
        'raw_network/llava-v1.6-7b.json',
        'raw_network/llava-v1.6-13b.json',
        'raw_network/qwen-vl-chat-7b.json',
        'raw_network/mplug-owl2-7b.json',
        'raw_network/internlm-xcomposer-7b.json',
        'raw_network/internlm-xcomposer-vl-7b.json',
        'raw_network/internlm-xcomposer2-7b.json',
        'raw_network/internlm-xcomposer2-vl-7b.json',
        'raw_network/stable-diffusion-safety-checker.json',
        'raw_network/nsfw-detector.json',
        'raw_network/nsfw_image_detection.json',
        'raw_network/vit-base-nsfw-detector.json'
    ]

    data_list_mllm_ablation_study = [
        'llava_ablation_study/llava-v1.5-7b-after-baseline.json',
        'mllm_ablation_study/llava-v1.5-7b-mix.json',
        'mllm_ablation_study/llava-v1.5-13b-after.json',
        'mllm_ablation_study/llava-v1.5-13b-mix.json',
        'mllm_ablation_study/llava-sharegpt4v-7b-after.json',
        'mllm_ablation_study/llava-sharegpt4v-13b-after.json',
        'mllm_ablation_study/llava-v1.6-7b-after.json',
        'mllm_ablation_study/llava-v1.6-13b-after.json',
        'mllm_ablation_study/qwen-vl-chat-7b-after.json',
        'mllm_ablation_study/mplug-owl2-7b-after.json',
        'mllm_ablation_study/internlm-xcomposer2-vl-7b-after.json',
        'raw_network_ablation_study/resnet50_8xb32_in1k.json',
        'raw_network_ablation_study/resnet152_8xb32_in1k.json',
        'raw_network_ablation_study/densenet201_4xb256_in1k.json',
        'raw_network_ablation_study/clip-vit-l-14-336.json'
    ]

    # choose
    # data_list_comparison_with_other_methods, data_list_mllm_ablation_study
    data_list = data_list_comparison_with_other_methods

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
