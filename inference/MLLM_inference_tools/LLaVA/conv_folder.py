import argparse
import torch
import os

from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.conversation import conv_templates, SeparatorStyle
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria

from PIL import Image

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
    file = open(filename, mode)
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

def main(args, conv_list):
    # Model
    disable_torch_init()

    model_name = get_model_name_from_path(args.model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(args.model_path, args.model_base, model_name, args.load_8bit, args.load_4bit, device=args.device)

    if 'llama-2' in model_name.lower():
        conv_mode = "llava_llama_2"
    elif "v1" in model_name.lower():
        conv_mode = "llava_v1"
    elif "mpt" in model_name.lower():
        conv_mode = "mpt"
    else:
        conv_mode = "llava_v0"

    if args.conv_mode is not None and conv_mode != args.conv_mode:
        print('[WARNING] the auto inferred conversation mode is {}, while `--conv-mode` is {}, using {}'.format(conv_mode, args.conv_mode, args.conv_mode))
    else:
        args.conv_mode = conv_mode

    # read a image list
    image_list = get_files(args.folder_file)

    for image_id, image_file in enumerate(image_list):
        
        image_relative_file = image_file.replace(args.folder_file, '')
        save_full_path = image_file.replace(args.folder_file, args.save_file) + '.txt'
        save_folder_path = '/'.join(save_full_path.split('/')[:-1])
        check_path(save_folder_path)
        save_list = []
        
        # print
        print(image_relative_file)

        # append information to save_list
        save_list.append(image_relative_file)

        conv = conv_templates[args.conv_mode].copy()
        if "mpt" in model_name.lower():
            roles = ('user', 'assistant')
        else:
            roles = conv.roles

        image = load_image(image_file)
        image_size = image.size
        # Similar operation in model_worker.py
        image_tensor = process_images([image], image_processor, model.config)
        if type(image_tensor) is list:
            image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
        else:
            image_tensor = image_tensor.to(model.device, dtype=torch.float16)

        # multi-turn conversation
        for index in range(len(conv_list)):
        
            inp = "%s: %s" % (roles[0], conv_list[index])

            print(f"{roles[1]}: ", end="")

            if image is not None:
                # first message
                if model.config.mm_use_im_start_end:
                    inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
                else:
                    inp = DEFAULT_IMAGE_TOKEN + '\n' + inp
                conv.append_message(conv.roles[0], inp)
                image = None
            else:
                # later messages
                conv.append_message(conv.roles[0], inp)
            conv.append_message(conv.roles[1], None)
            prompt = conv.get_prompt()

            input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)
            stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
            keywords = [stop_str]
            stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
            streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

            with torch.inference_mode():
                output_ids = model.generate(
                    input_ids,
                    images=image_tensor,
                    do_sample=True if args.temperature > 0 else False,
                    temperature=args.temperature,
                    max_new_tokens=args.max_new_tokens,
                    streamer=streamer,
                    use_cache=True,
                    stopping_criteria=[stopping_criteria])

            outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
            conv.messages[-1][-1] = outputs

            if args.debug:
                print("\n", {"prompt": prompt, "outputs": outputs}, "\n")

            # append information to save_list
            save_list.append(conv_list[index])
            save_list.append(outputs)

        # save save_list to file
        text_save(save_list, save_full_path)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="facebook/opt-350m")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--folder-file", type=str, required=True)
    parser.add_argument("--save-file", type=str, default='save_folder')
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--conv-mode", type=str, default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    
    # define the multi-turn conversation list
    conv_list = [
        'Describe the image in 3 or 4 sentences.',
        'Answer following questions with only yes or no and question numbers, without repeating questions: 1. Is this image sexually suggestive?; 2. Is this image related to violence or abuse?; 3. Does this image contain abnormal or unusual content in daily life?; 4. Does this image contain porn content?; 5. Does this image contain scary or frightening content?; 6. Does this image contain violent content?; 7. Does this image contain disgusting content?; 8. Does this image contain political content?; 9. Does this image look ugly?'
    ]

    main(args, conv_list)
