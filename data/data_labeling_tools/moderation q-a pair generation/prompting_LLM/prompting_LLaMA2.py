# -*- coding: utf-8 -*-
import os
import json
from typing import List, Optional
from llama import Llama, Dialog
import time
import argparse

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding='utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read a txt expect EOF
def text_readlines(filename, mode = 'r'):
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

# use LLaMA 2
def load_llama_model(
    ckpt_dir: str,
    tokenizer_path: str,
    max_seq_len: int = 512,
    max_batch_size: int = 1,
):
    """
    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
    """
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    return generator

# call LLM
def llm_client(
    generator,
    prompt: str,
    temperature: float = 0.1,
    top_p: float = 0.9,
    max_gen_len: Optional[int] = None,
):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """
    dialogs: List[Dialog] = [
        [{"role": "user", "content": prompt}],
    ]
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    """
    """
    for dialog, result in zip(dialogs, results):
        for msg in dialog:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )
        print("\n==================================\n")
    return results[0]['generation']['content']

if __name__ == '__main__':

    # using Meta's LLaMA 2 to label data
    # Note:
    # if running on 2 A800 GPU cards, the program takes around 67000 Mb memory on each card
    # if running on 4 A800 GPU cards, the program takes around 33500 Mb memory on each card
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type = str, default = '/home/zyz/pretrained_models/llama-2-70b-chat', help = 'Model path')
    parser.add_argument('--tokenizer_path', type = str, default = '/home/zyz/pretrained_models/llama-2-70b-chat/tokenizer.model', help = 'Tokenizer path')
    parser.add_argument('--txt_path', type = str, default = '/home/zyz/pretrained_models/llama-2-70b-chat-hf', help = 'File path')
    parser.add_argument('--q_type', default = 'mix', choices = ['mc', 'qa', 'mix'], help = 'The choices of prompting')
    opt = parser.parse_args()
    print(opt)

    # define base
    max_seq_len = 2048
    max_batch_size = 8
    generator = load_llama_model(opt.ckpt_dir, opt.tokenizer_path, max_seq_len, max_batch_size)

    # define base
    text_list = text_readlines(opt.txt_path)
    text_list_half_length = len(text_list) // 2
    save_path = opt.txt_path.split('/')[-1].split('.')[0] + '_' + opt.q_type
    check_path(save_path)

    # define input
    system_message = 'You are an image content moderator who can analyze a single image.'
    if opt.q_type == 'mc':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 5 multiple-choice questions (4 choices, A, B, C, D, per question). The response is in the format of a table. The columns are \'Question\', \'Choices\' (only for multiple-choice questions), and \'Answer\'. All answers can be derived from the description and should be concise and accurate.\nDescription: '
    if opt.q_type == 'qa':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 6 yes/no questions, 2 what questions, and 2 how questions. The response is in the format of a table. The columns are \'Type of Question\', \'Question\' and \'Answer\'. All answers can be derived from the description and should be concise and accurate.\nDescription: '
    if opt.q_type == 'mix':
        instruction = 'You receive a description of an image. Your task is to use the provided description, and then create plausible questions about the image with answers.\nThe questions include 3 yes/no questions, 3 multiple-choice questions (4 choices, A, B, C, D, per question), 2 what questions, and 2 how questions. The response is in the format of a table. The columns are \'Type of Question\', \'Question\', \'Choices\' (only for multiple-choice questions), and \'Answer\'. All questions are related to content moderation. All answers can be derived from the description and should be concise and accurate.\nDescription: '
        #instruction = 'You are an image content moderator who can analyze a single image. You receive a long description of an image. Your task is to analyze and rewrite the provided long description using a specific format.\nThe format includes 3 long sentences. The first long sentence is a brief description of the image. The second long sentence is the reason why this image is sexy (e.g., Because ..., this image is a sexy image.) The third long sentence is a conclusion of the image\'s atmosphere and the sexy level of this image. Each long sentence is not longer than two sentences.\nLong description: '
    
    # inference
    for i in range(text_list_half_length):

        # extract the image_name and user_content
        image_name = text_list[i*2]
        user_content = text_list[i*2+1]
        print(i, text_list_half_length, image_name)

        # define the specific format of input prompt
        input_content = system_message + instruction + user_content

        # forward LLM
        text = llm_client(generator, prompt = input_content)

        # save the generated contents to a file
        save_list = []
        save_list.append(image_name + '\n')
        save_list.append(text)
        text_save(save_list, os.path.join(save_path, '%d.txt' % i), mode = 'a')
        