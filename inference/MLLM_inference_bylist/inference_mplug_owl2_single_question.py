# -*- coding: utf-8 -*-
import argparse
import os

import torch
from PIL import Image
from transformers import TextStreamer

from mplug_owl2.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from mplug_owl2.conversation import conv_templates, SeparatorStyle
from mplug_owl2.model.builder import load_pretrained_model
from mplug_owl2.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

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

def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

def main(args):
    
    model_name = get_model_name_from_path(args.model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, None, model_name, load_8bit=False, load_4bit=False, device="cuda")

    # read list_file
    # image path for odd-numbered actions, multi-turn dialogue for even-numbered actions
    list_file = text_readlines(args.list_file)
    num_of_samples = len(list_file) // 2

    for image_id in range(num_of_samples):

        # define the image file and conversations
        image_relative_file = list_file[image_id * 2]
        image_file = os.path.join(args.folder_file, image_relative_file)
        save_full_path = os.path.join(args.save_file, image_relative_file).split('.')[0] + '.txt'
        save_folder_path = '/'.join(save_full_path.split('/')[:-1])
        check_path(save_folder_path)

        query = list_file[image_id * 2 + 1]
        
        save_list = []

        # append information to save_list
        save_list.append(image_relative_file)
        
        # print
        print(image_relative_file)

        conv = conv_templates["mplug_owl2"].copy()
        roles = conv.roles

        image = Image.open(image_file).convert('RGB')
        max_edge = max(image.size) # We recommand you to resize to squared image for BEST performance.
        image = image.resize((max_edge, max_edge))

        image_tensor = process_images([image], image_processor)
        image_tensor = image_tensor.to(model.device, dtype=torch.float16)

        inp = DEFAULT_IMAGE_TOKEN + query
        conv.append_message(conv.roles[0], inp)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)
        stop_str = conv.sep2
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
        streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=image_tensor,
                do_sample=True,
                temperature=args.temperature,
                max_new_tokens=args.max_new_tokens,
                streamer=streamer,
                use_cache=True,
                stopping_criteria=[stopping_criteria])

        outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
        
        if args.debug:
            print("\n", {"prompt": query, "outputs": outputs}, "\n")

        # append information to save_list
        save_list.append(query)
        save_list.append(outputs)

    # save save_list to file
    # text_save(save_list, save_full_path)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="mplug-owl2-llama2-7b")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--folder-file", type=str, required=True)
    parser.add_argument("--list-file", type=str, default='list_file.txt', help='multiple questions are divided by \t')
    parser.add_argument("--save-file", type=str, default='save_folder')
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--conv-mode", type=str, default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    main(args)
