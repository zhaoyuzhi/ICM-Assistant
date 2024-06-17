# -*- coding: utf-8 -*-
import os
import openai
import time
import argparse

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

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

# call LLM
def llm_client(api_key, llm_model, user_content):
    request_start = time.time()

    # load api key
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=llm_model,
        messages=[
            {"role": "user",
             "content": user_content},
        ],
        temperature=0.2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    request_duration = time.time() - request_start

    print(f"Successful LLM query. It took {request_duration:.2f}s")

    return response.choices[0]["message"]["content"]


if __name__ == "__main__":

    # using OpenAI's ChatGPT to label data
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type = str, default = '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', help = 'api key of OpenAI')
    parser.add_argument('--txt_path', type = str, default = '/home/zyz/prompting_chatgpt/result_for_llm.txt', help = 'File path')
    parser.add_argument('--q_type', default = 'mix', choices = ['mc', 'qa', 'mix'], help = 'The choices of prompting')
    opt = parser.parse_args()
    print(opt)

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
    
    for i in range(text_list_half_length):
        
        # extract the image_name and user_content
        image_name = text_list[i*2]
        user_content = text_list[i*2+1]
        print(i, text_list_half_length, image_name)

        # define the specific format of input prompt
        input_content = instruction + user_content
        
        # forward LLM
        text = llm_client(opt.api_key, 'gpt-3.5-turbo-1106', input_content)

        # save the generated contents to a file
        save_list = []
        save_list.append(image_name + '\n')
        save_list.append(text)
        text_save(save_list, os.path.join(save_path, '%d.txt' % i), mode = 'a')
        