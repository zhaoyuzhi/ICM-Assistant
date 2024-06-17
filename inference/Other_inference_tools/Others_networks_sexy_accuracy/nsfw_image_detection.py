import argparse
import json
import os

import numpy as np
from nsfw_detector import predict

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
    parser.add_argument("--model_path", type=str, default="nsfw_mobilenet2.224x224.h5")
    parser.add_argument("--save_path", type=str, default="sexy_score_nsfw_mobilenet2.json")
    args = parser.parse_args()

    # read a image list
    content_list = get_files(args.folder_path)

    # define inference
    model = predict.load_model(args.model_path)

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

        result = predict.classify(model, content_file)

        result = result[content_file]
        output = [result['sexy'], result['neutral'], result['porn'], result['hentai'], result['drawings']]
        top = np.argmax(output)

        if top == 1 or top == 4:
            if gt_id != 1:
                true_count += 1
            else:
                false_count += 1
        elif gt_id == 1:
            true_count += 1
        else:
            false_count += 1
        sexy_logit_yes = output[top if not top == 1 else 0]
        sexy_logit_no = output[1]

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
