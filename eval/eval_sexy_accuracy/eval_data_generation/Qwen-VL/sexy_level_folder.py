# -*- coding: utf-8 -*-
import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import json

torch.manual_seed(1234)

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

# save a dictionary object to a json file
def json_save(json_content, json_file):
    with open(json_file, 'a') as fp:
        json.dump(json_content, fp, indent=4)

def main(args, conv_list):
    # define image list
    image_list = get_files(args.folder_file)

    # Note: The default behavior now has injection attack prevention off.
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)

    if args.bf16:
        # use bf16
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="auto", trust_remote_code=True, bf16=True).eval()
    elif args.fp16:
        # use fp16
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="auto", trust_remote_code=True, fp16=True).eval()
    elif args.cpu:
        # use cpu only
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="cpu", trust_remote_code=True).eval()
    else:
        # use cuda device
        model = AutoModelForCausalLM.from_pretrained(args.model_path, device_map="cuda", trust_remote_code=True).eval()
    
    # Specify hyperparameters for generation
    model.generation_config = GenerationConfig.from_pretrained(args.model_path, trust_remote_code=True)

    # define a json list for saving all results
    json_list = []
    sexy_count = 0

    for image_id, image_file in enumerate(image_list):

        # define the image file
        image_relative_file = image_file.replace(args.folder_file, '')
        save_full_path = image_file.replace(args.folder_file, args.save_file).split('.')[0] + '.txt'
        save_folder_path = '/'.join(save_full_path.split('/')[:-1])
        check_path(save_folder_path)
        image_json = {}
        image_json["image_name"] = image_file.split('/')[-1]

        # print
        print(image_relative_file)

        # 1st dialogue turn
        query = tokenizer.from_list_format([
            {'image': image_file}, # Either a local path or an url
            {'text': conv_list[0]},
        ])
        response, history = model.chat(tokenizer, query=query, history=None)
        print('USER:', conv_list[0])
        print('ASSISTANT:', response)
        
        if response[0].lower() == 'y':
            image_json["logit_yes"] = 1
            image_json["logit_no"] = 0
            image_json["sexy_score"] = 1
            image_json["sexy_conclusion"] = "Yes"
            sexy_count += 1
        else:
            image_json["logit_yes"] = 0
            image_json["logit_no"] = 1
            image_json["sexy_score"] = 0
            image_json["sexy_conclusion"] = "No"
        
        # save all current results to a json file and print
        json_list.append(image_json)
        print(image_id, image_file)
        print('response:', response, 'logit_yes:', image_json["logit_yes"], 'logit_no:', image_json["logit_no"], 'sexy_score:', image_json["sexy_score"])

    # save json_list to a json file and print
    json_save(json_list, args.save_file)
    print('There are %d images, in which there are %d sexy images.' % (len(image_list), sexy_count))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default='Qwen-VL-Chat', help='path to model file')
    parser.add_argument("--folder-file", type=str, default='img', help='path to all image files')
    parser.add_argument("--save-file", type=str, default='sexy_score.json')
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()

    # define the caption
    conv_list = [
        'Is this picture sexy? Please answer with only yes or no.'
    ]

    main(args, conv_list)
    