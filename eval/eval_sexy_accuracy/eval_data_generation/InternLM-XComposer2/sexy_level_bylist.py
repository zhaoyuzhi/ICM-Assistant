from transformers import AutoModel, AutoTokenizer
import torch

import random
from copy import deepcopy
from PIL import Image
import json
from tqdm import tqdm
import numpy as np
torch.set_grad_enabled(False)
import argparse
import os


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
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# save a dictionary object to a json file
def json_save(json_content, json_file):
    with open(json_file, 'a') as fp:
        json.dump(json_content, fp, indent = 4)

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

# read all files under a path
def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

def get_logits(model, text, image_path):
    image = Image.open(image_path).convert("RGB")
    with torch.cuda.amp.autocast():
        image = model.vis_processor(image).unsqueeze(0).to(model.device)
        img_embeds = model.encode_img(image)
    prompt_segs = text.split('<ImageHere>')
    prompt_seg_tokens = [
        model.tokenizer(seg,
                        return_tensors='pt',
                        add_special_tokens=i == 0).
        to('cuda:0').input_ids
        for i, seg in enumerate(prompt_segs)
    ]
    prompt_seg_embs = [
        model.model.tok_embeddings(seg)
        for seg in prompt_seg_tokens
    ]
    prompt_seg_embs = [prompt_seg_embs[0], img_embeds, prompt_seg_embs[1]]
    prompt_embs = torch.cat(prompt_seg_embs, dim=1)
    return model(
        inputs_embeds=prompt_embs)['logits'][:, -1]

def softmax(a, b, temperature=1):
    a /= temperature
    b /= temperature
    return np.exp(a) / (np.exp(a) + np.exp(b))

def main(args):
    
    #torch.manual_seed(1234)

    # init model and tokenizer
    model = AutoModel.from_pretrained(args.model_path,
                                      trust_remote_code=True).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    model.tokenizer = tokenizer
    
    # print the token id of "yes" and "no"
    #print(tokenizer('Yes', allowed_special="all", disallowed_special=()))
    #print(tokenizer('No', allowed_special="all", disallowed_special=()))

    # read a image list
    image_list = text_readlines(args.list_file)

    # define a json list for saving all results
    json_list = []
    sexy_count = 0

    for image_id, image_file in enumerate(image_list):
        
        image_file = os.path.join(args.folder_file, image_file)
        image = load_image(image_file)
        image_json = {}
        image_json["image_name"] = image_file.split('/')[-1]
        message = args.question
        with torch.inference_mode():
            output_logits = get_logits(model, message, image_file)
        probs, inds = output_logits.sort(dim=-1, descending=True)
        lgood, lpoor = output_logits[0, 9583].item(), output_logits[0, 2917].item()
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

    # save json_list to a json file and print
    json_save(json_list, args.save_file)
    print('There are %d images, in which there are %d sexy images.' % (len(image_list), sexy_count))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="internlm-xcomposer2-vl-7b")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--folder-file", type=str, required=True)
    parser.add_argument("--list-file", type=str, default='name_list.txt', help='name list')
    parser.add_argument("--save-file", type=str, default='sexy_score.json')
    parser.add_argument("--question", type=str, default='<ImageHere>Is the picture sexy?')
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    main(args)
    