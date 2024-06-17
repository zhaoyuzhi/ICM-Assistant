# -*- coding: utf-8 -*-
import os
import json
import random

import numpy as np


# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if '.txt' in filespath:
                ret.append(os.path.join(root, filespath))
    return ret


# save a list to a txt
def text_save(content, filename, mode='a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding='utf-8')
    # file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()


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


# output txt
def post_process_output_llava_format(llm_output_folder, quesion_list):
    llm_output_list = get_files(llm_output_folder)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        # file_name
        llm_output_file = text_readlines(file_name)
        # post-process a llm_output_file
        llm_output_file_half_len = len(llm_output_file) // 2
        for j in range(llm_output_file_half_len):
            # get the image name and the description
            name = llm_output_file[j * 2]
            llm_output_line_answer = llm_output_file[j * 2 + 1]
            # print(name)
            # print(llm_output_line_answer)
            # get the question randomly
            llm_output_line_question_index = np.random.randint(0, len(quesion_list))
            llm_output_line_question = quesion_list[llm_output_line_question_index]
            # write a Q-A pair to json
            img_json = {}
            img_json["id"] = "identity_" + name.split('.')[0] + '_description'
            img_json["image"] = '/home/mywu/data/sexy_check_all/' + name

            img_json["conversations"] = [
                {
                    "from": "user",
                    "value": 'Picture 1:<img>' + '/home/mywu/data/sexy_check_all/' + name + '</img>\n' + llm_output_line_question
                },
                {
                    "from": "assistant",
                    "value": llm_output_line_answer
                }
            ]
            json_list.append(img_json)
    return json_list


def generate_reasoning_step2(step1_name, step2_name, reasoning_path='../../qa/reasoning_5x/'):
    # load json from step 1
    f = open(step1_name, 'r')
    json_list = json.load(f)
    # n of QA-WH-MC
    print(len(json_list) - 665000)
    file_name_set = set()
    for j in json_list:
        # print(j)
        if 'identity' in str(j['id']):
            name = j["image"].split('/')[-1]
            file_name_set.add(name.split('/')[-1])
    print(len(file_name_set))

    base_folder_path = reasoning_path
    d_list = post_process_output_llava_format(base_folder_path, quesion_list)
    filtered_list = []
    current_name_set = set()
    for j in d_list:
        name = j['image'].split('/')[-1]
        if name in file_name_set:
            filtered_list.append(j)
            current_name_set.add(name)
    print(len(filtered_list))
    extend_list = []
    # for no qa-mc-wh settings
    # ff = open('/home/deveco/Desktop/models/llava_v1_5_mix665k.json', 'r')
    # json_list = json.load(ff)
    # for i in range(8):
    #     extend_list.extend(filtered_list)
    # extend_list = random.sample(extend_list, 104000)
    # print(len(extend_list))
    json_list.extend(filtered_list)
    # save to a final json file, for training
    with open(step2_name, 'a') as fp:
        json.dump(json_list, fp, indent=4)

quesion_list = [
    'Examine whether the image looks sexy and provide an evaluation based on your observations.',
    'Describe the sexy degree of the image, and the provide a final evaluation.',
    'Delve into the sexy degree of the photograph and give a verdict based on your scrutiny.',
    'Discuss and assess the sexy degree of the picture, and form conclusions based on your evaluation.',
    'Break down the sexy degree aspects of the image and judge it from your analysis.',
    'Study and appraise the sexy degree of the image, drawing conclusions from your examination.',
    'Analyze the characteristics of the image and determine its sexy degree based on your findings.',
    'Inspect the image closely and offer an evaluation on whether the image looks sexy rooted in your analysis.',
    'Take a detailed look at the image and rate its sexy level according to your assessment.',
    'Investigate the image\'s attributes and provide feedback on whether the image looks sexy based on your critique.',
    'Explore the sexy factors of the image and offer an evaluation based on your insights.',
    'Evaluate whether the image exudes sexiness and provide your observations.',
    'Describe the level of sexiness in the image and conclude with your evaluation.',
    'Examine the photograph\'s sexiness and deliver a verdict based on your careful examination.',
    'Discuss and assess the level of sexiness portrayed in the picture, drawing conclusions from your evaluation.',
    'Break down the elements that contribute to the image\'s sexiness and judge it based on your analysis.',
    'Study and appraise the level of sexiness in the image, formulating conclusions from your examination.',
    'Analyze the image\'s characteristics and determine its level of sexiness based on your findings.',
    'Inspect the image closely and provide an evaluation on whether it emanates sexiness, rooted in your analysis.',
    'Take a detailed look at the image and rate its level of sexiness according to your assessment.',
    'Investigate the image\'s attributes and offer feedback on whether it exudes sexiness based on your critique.',
    'Explore the factors that contribute to the image\'s sexiness and provide an evaluation based on your insights.',
    'Examine whether the image evokes sexiness and provide an evaluation based on your observations.',
    'Describe the sexy degree of the image and then provide a final evaluation.',
    'Delve into the sexy degree of the photograph and give a verdict based on your scrutiny.',
    'Discuss and assess the sexy degree of the picture, and form conclusions based on your evaluation.',
    'Break down the sexy degree aspects of the image and judge it from your analysis.',
    'Study and appraise the sexy degree of the image, drawing conclusions from your examination.',
    'Analyze the characteristics of the image and determine its sexy degree based on your findings.',
    'Inspect the image closely and offer an evaluation on whether the image evokes sexiness rooted in your analysis.',
    'Take a detailed look at the image and rate its sexy level according to your assessment.',
    'Investigate the image\'s attributes and provide feedback on whether the image evokes sexiness based on your critique.',
    'Explore the sexy factors of the image and offer an evaluation based on your insights.'
]
if __name__ == '__main__':
    # -------------------------------------------------
    # run this script after formatting the MLLM outputs
    # i.e., run this script after running post_process_MLLM_output_for_LLM.py
    # -------------------------------------------------

    # read and post-process lists
    generate_reasoning_step2()




