import argparse
import torch
import os

from mplug_owl2.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from mplug_owl2.conversation import conv_templates, SeparatorStyle
from mplug_owl2.model.builder import load_pretrained_model
from mplug_owl2.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

import numpy as np
import json
from tqdm import tqdm
import requests
from PIL import Image
from io import BytesIO
from transformers import TextStreamer


def load_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    # file = open(filename, mode, encoding = 'utf-8')
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

def softmax(a, b, temperature=1):
    a /= temperature
    b /= temperature
    return np.exp(a) / (np.exp(a) + np.exp(b))

def main(args):
    # Model
    #disable_torch_init()

    model_name = get_model_name_from_path(args.model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, args.model_base, model_name, args.load_8bit, args.load_4bit, device=args.device)

    inp = args.question
    conv = conv_templates[args.conv_mode].copy()
    inp = DEFAULT_IMAGE_TOKEN + inp
    conv.append_message(conv.roles[0], inp)
    image = None
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    
    # read a image list
    image_list = get_files(args.folder_file)

    # define a json list for saving all results
    json_list = []
    sexy_count = 0

    for image_id, image_file in enumerate(image_list):
        
        try:
            image = load_image(image_file)
            image_json = {}
            image_json["image_name"] = image_file.split('/')[-1]

            # Similar operation in model_worker.py
            image_tensor = process_images([image], image_processor, model.config)
            if type(image_tensor) is list:
                image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
            else:
                image_tensor = image_tensor.to(model.device, dtype=torch.float16)

            # obtain the probability
            input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(
                0).to(
                model.device)
            stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
            keywords = [stop_str]
            stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
            with torch.inference_mode():
                output_logits = model(input_ids, images=image_tensor)["logits"][:, -1]
            probs, inds = output_logits.sort(dim=-1, descending=True)

            # LLaMA 2 tokenizer: 3869: Yes, 1939: No
            lgood, lpoor = output_logits[0, 3869].item(), output_logits[0, 1939].item()
            sexy_score = softmax(lgood, lpoor, temperature=1)
            image_json["logit_yes"] = lgood
            image_json["logit_no"] = lpoor
            image_json["sexy_score"] = sexy_score

            # conclude the image sexy or not based on the threshold
            if sexy_score >= args.threshold:
                image_json["sexy_conclusion"] = "Yes"
                sexy_count += 1
            else:
                image_json["sexy_conclusion"] = "No"

            # save all current results to a json file and print
            json_list.append(image_json)
            print(image_id, image_file)
            print('logit_yes:', lgood, 'logit_no:', lpoor, 'sexy_score:', sexy_score)

        except OSError as error: 
            print(error)
    
    # save json_list to a json file and print
    json_save(json_list, args.save_file)
    print('There are %d images, in which there are %d sexy images.' % (len(image_list), sexy_count))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="MAGAer13/mplug-owl2-llama2-7b")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--folder-file", type=str, required=True)
    parser.add_argument("--list-file", type=str, default='name_list.txt', help='name list')
    parser.add_argument("--save-file", type=str, default="sexy_score.json")
    parser.add_argument("--question", type=str, default="Is the picture sexy?")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--conv-mode", type=str, default="mplug_owl2")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    main(args)
    