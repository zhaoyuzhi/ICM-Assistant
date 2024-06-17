import argparse
import os

import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq

# read a txt expect EOF
def text_readlines(filename, mode='r'):
    # try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        # Use the following command if there is Chinese characters are read
        file = open(filename, mode, encoding='utf-8')
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
def text_save(content, filename, mode='a'):
    # try to save a list variable in txt file.
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read all files under a path
def get_files(path):
    # read a folder, return the complete path of all files
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", type=str, default="/home/zyz/dataset/ECCV_2024_data/data/val_v2")
    parser.add_argument("--model_path", type=str, default="/home/zyz/pretrained_models/kosmos-2-patch14-224")
    parser.add_argument("--file_path", type=str, default="eval_sexy_degree_prompts.txt")
    parser.add_argument("--save_path", type=str, default="./")
    args = parser.parse_args()

    # read all contents
    file_list = text_readlines(args.file_path)
    file_list_half_length = len(file_list) // 2
    
    # define a save_list
    save_list = []

    # main
    model = AutoModelForVision2Seq.from_pretrained(args.model_path)
    processor = AutoProcessor.from_pretrained(args.model_path)

    for i in range(0, file_list_half_length):

        # extract the image_name and user_content
        image_name = file_list[i*2]
        question = file_list[i*2+1]
        print(i, file_list_half_length, image_name)

        # forward
        image = Image.open(image_name).convert('RGB')
        inputs = processor(text=question, images=image, return_tensors="pt")

        generated_ids = model.generate(
            pixel_values=inputs["pixel_values"],
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            image_embeds=None,
            image_embeds_position_mask=inputs["image_embeds_position_mask"],
            use_cache=True,
            max_new_tokens=128,
        )
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        processed_text = processor.post_process_generation(generated_text, cleanup_and_extract=False)

        print(processed_text)

        # save the generated contents to a file
        save_list.append(image_name)
        save_list.append(processed_text)

    text_save(save_list, os.path.join(args.save_path, 'kosmos2.txt'), mode = 'a')
