import argparse
import json
import os

import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

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

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# save a dictionary object to a json file
def json_save(json_content, json_file):
    with open(json_file, 'a') as fp:
        json.dump(json_content, fp, indent = 4)

# read all files under a path
def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

def softmax(a, b, temperature = 1):
    a /= temperature
    b /= temperature
    return np.exp(a) / (np.exp(a) + np.exp(b))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", type=str, default="/home/zyz/dataset/ECCV_2024_data_mmpretrain")
    parser.add_argument("--model_path", type=str, default="configs/resnet/resnet50_8xb32_in1k_ECCV2024.py")
    parser.add_argument("--output_path", type=str,
                        default="/home/zyz/code/20231219_mmpretrain-main/work_dirs/resnet50_8xb32_in1k_ECCV2024/epoch_1000.pth")
    parser.add_argument("--save_path", type=str, default="sexy_score_resnet50_8xb32_in1k_ECCV2024.json")
    args = parser.parse_args()

    # read a image list
    content_list = get_files(args.folder_path)

    # define inference
    inferencer = AutoModelForImageClassification.from_pretrained(args.model_path).to('cuda')
    processor = ViTImageProcessor.from_pretrained(args.model_path)

    # define a json list for saving all results
    json_list = []

    true_count, false_count = 0, 0
    for image_id, content_file in enumerate(content_list):

        # get the image file and ground truth id
        if 'not-sexy' in content_file:
            gt_id = 0
        else:
            gt_id = 1
        print(image_id, len(content_list), content_file, gt_id)

        img = Image.open(content_file)
        with torch.no_grad():
            inputs = processor(images=img, return_tensors='pt').to('cuda')
            result = inferencer(**inputs)

        top = torch.argmax(result['logits'][0])
        if top == 1 and gt_id == 1:
            true_count += 1
        elif top != 1 and gt_id == 0:
            true_count += 1
        else:
            false_count += 1
        sexy_logit_yes = float(result['logits'][0][0])
        sexy_logit_no = float(result['logits'][0][1])
        sexy_score = softmax(sexy_logit_yes, sexy_logit_no, temperature=1)

        # save the results to a json file
        image_json = {}
        image_json["image_name"] = content_file.split('/')[-1]
        image_json["logit_yes"] = sexy_logit_yes
        image_json["logit_no"] = sexy_logit_no
        image_json["sexy_score"] = sexy_score
        json_list.append(image_json)

    # compute accuracy
    acc = true_count / (true_count + false_count)
    print('The overall accuracy is:', acc)

    # save json_list to a json file
    json_save(json_list, args.save_path)
