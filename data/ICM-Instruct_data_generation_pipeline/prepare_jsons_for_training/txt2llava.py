
# -*- coding: utf-8 -*-
import glob
import os
import json
import numpy as np
import random


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

mc_question_list = [
    'Answer with the option\'s letter from the given choices directly.',
    'Please indicate your response by selecting the corresponding letter from the provided options.',
    'Kindly choose the appropriate letter from the given choices as your answer.',
    'Respond directly by selecting the letter that represents your choice from the provided options.',
    'Indicate your answer by simply picking the letter associated with your choice from the given options.',
    'Select the letter corresponding to your choice from the provided options as your answer.',
    'Your response should be the letter that matches your choice from the given options.',
    'Choose the correct letter from the provided choices and use it as your answer.',
    'Please provide your answer by selecting the letter that corresponds to your choice from the given options.',
    'Your answer should be the letter that represents your chosen option from the provided choices.',
    'Select the appropriate letter from the given options to indicate your answer directly.',
    'Indicate your choice by selecting the letter that corresponds to your answer from the provided options.',
    'Please respond by directly choosing the letter associated with your answer from the given choices.',
    'Your answer should be the letter that best matches your choice from the provided options.',
    'Choose the correct letter from the given choices and use it as your response.',
    'Select the letter that corresponds to your chosen option from the provided choices as your answer.',
    'Indicate your response by choosing the letter associated with your choice from the given options.',
    'Please provide your answer directly by selecting the letter that represents your choice from the options provided.',
    'Your answer should be the letter that corresponds to your chosen option from the available choices.',
    'Select the appropriate letter from the options provided to indicate your chosen response.',
    'Indicate your answer by selecting the letter that corresponds to your choice from the given options directly.',
]

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if '.txt' in filespath:
                ret.append(os.path.join(root, filespath))
    return ret

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    file = open(filename, mode, encoding = 'utf-8')
    # file = open(filename, mode)
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


def post_process_output_llava_format_openqa(llm_output_folder, qa = True, wh = True):
    llm_output_list = get_files(llm_output_folder)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        # print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        llm_output_file = text_readlines(file_name)
        # post-process a llm_output_file
        for j, llm_output_line in enumerate(llm_output_file):
            # define error_detection symbol for this Q-A pair
            # print(llm_output_line)
            error_detection = False
            # define ids for a file

            # post-process question-answer table
            if '| Type of Question | Question | Answer |' in llm_output_line:
                continue
            if '| --- | --- | --- |' in llm_output_line:
                continue
                # post-process one question-answer pair
            llm_output_line_type_of_question = llm_output_line.split('|')[1].strip()
            llm_output_line_question = llm_output_line.split('|')[2].strip()
            llm_output_line_choices = llm_output_line.split('|')[3].strip()
            llm_output_line_answer = llm_output_line.split('|')[-2].strip()
            # post-process Yes or No questions
            if 'Yes/No' in llm_output_line_type_of_question:
                if 'yes' in llm_output_line_answer.lower():
                    llm_output_line_answer = 'Yes'
                elif 'no' in llm_output_line_answer.lower():
                    llm_output_line_answer = 'No'
                elif '✓' in llm_output_line_answer.lower():
                    llm_output_line_answer = 'Yes'
                elif '✘' in llm_output_line_answer.lower():
                    llm_output_line_answer = 'No'
                # else:
                # print(file_name)
                if qa == False:
                    error_detection = True
            # post-process what and how questions
            else:
                llm_output_line_answer = llm_output_line_answer.replace('✓', '').replace('✘', '').replace('-'
                                                                                                          ,'').strip()
                # LLM syntax error
                if len(llm_output_line_answer) == 0:
                    llm_output_line_answer = llm_output_line_choices
                # if still existing error
                if len(llm_output_line_answer) < 2:
                    # print(file_name)
                    error_detection = True
                if wh == False:
                    error_detection = True

            # add . to all answers
            llm_output_line_answer = llm_output_line_answer.strip()
            if not llm_output_line_answer.endswith("."):
                llm_output_line_answer = llm_output_line_answer + "."
            # print('yes')
            # write a Q-A pair to json
            file_name = file_name[5:-4]
            if not error_detection:
                img_json = {}
                img_json["id"] = "identity_" + file_name + '_pair' + str(j)
                img_json["image"] = 'sexy_check_all/' + file_name
                img_json["conversations"] = [
                    {
                        "from": "human",
                        "value": llm_output_line_question + "\n<image>"
                    },
                    {
                        "from": "gpt",
                        "value": llm_output_line_answer
                    }
                ]
                json_list.append(img_json)

    return json_list

def post_process_output_llava_format_multi_choice(llm_output_folder):
    llm_output_list = get_files(llm_output_folder)
    # print(llm_output_list)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        # print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        llm_output_file = text_readlines(file_name)
        # post-process a llm_output_file
        error_detection = False
        for j, llm_output_line in enumerate(llm_output_file):
            # define error_detection symbol for this Q-A pair

            if '| Question | Choices | Answer |' in llm_output_line:
                continue
            if '| --- | --- | --- |' in llm_output_line:
                continue
                # print(j)

            # post-process one question-answer pair
            # llm_output_line_type_of_question = llm_output_line.split('|')[1].strip()
            llm_output_line_question = llm_output_line.split('|')[1].strip()
            for idx in range(len(llm_output_line_question)):
                if  (ord(llm_output_line_question[idx]) >= 65 and ord(llm_output_line_question[idx]) <= 90) or \
                        (ord(llm_output_line_question[idx]) >= 97 and ord(llm_output_line_question[idx]) <= 122):
                    llm_output_line_question = llm_output_line_question[idx:]
                    break
            llm_output_line_choices = ''
            for idx in range(2, len(llm_output_line.split('|')) - 2):
                llm_output_line_choices += '\n' + llm_output_line.split('|')[idx].strip()
            llm_output_line_question_index = np.random.randint(0, len(mc_question_list))
            llm_output_line_choices += '\n ' + mc_question_list[llm_output_line_question_index]
            llm_output_line_answer = llm_output_line.split('|')[-2].strip()

            llm_output_line_question = llm_output_line_question + llm_output_line_choices

            llm_output_line_answer = llm_output_line_answer.strip().upper()[:2]
            if 'A' in llm_output_line_answer: llm_output_line_answer = 'A.'
            if 'B' in llm_output_line_answer: llm_output_line_answer = 'B.'
            if 'C' in llm_output_line_answer: llm_output_line_answer = 'C.'
            if 'D' in llm_output_line_answer: llm_output_line_answer = 'D.'
            if 'E' in llm_output_line_answer: llm_output_line_answer = 'E.'

            if not llm_output_line_answer.endswith("."):
                llm_output_line_answer = llm_output_line_answer + "."

            # write a Q-A pair to json
            if not error_detection:

                name = file_name[5:-4]
                img_json = {}
                img_json["id"] = "identity_" + name + '_mc_pair' + str(j)
                img_json["image"] = 'sexy_check_all/' + name
                img_json["conversations"] = [
                    {
                        "from": "human",
                        "value": llm_output_line_question + "\n<image>"
                    },
                    {
                        "from": "gpt",
                        "value": llm_output_line_answer
                    }
                ]
                json_list.append(img_json)

    return json_list

def post_process_output_llava_format_reason(llm_output_folder, quesion_list, cnt):
    llm_output_list = get_files(llm_output_folder)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        # print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        # file_name
        llm_output_file = text_readlines(file_name)
        if len(llm_output_file) == 0:
            # print(file_name)
            continue
        llm_output_line_answer = llm_output_file[0]
        # get the question randomly
        llm_output_line_question_index = np.random.randint(0, len(quesion_list))
        llm_output_line_question = quesion_list[llm_output_line_question_index]
        # write a Q-A pair to json
        name = file_name.split('/')[-1][:-4]
        img_json = {}
        img_json["id"] = "identity_" + name + '_description' + str(cnt)
        img_json["image"] = 'sexy_check_all/' + name
        img_json["conversations"] = [
            {
                "from": "human",
                "value": llm_output_line_question + "\n<image>"
            },
            {
                "from": "gpt",
                "value": llm_output_line_answer
            }
        ]
        json_list.append(img_json)
    return json_list

def generate_json(json_name):
    json_list = []
    print('generating qa pairs ...')
    qa_list = post_process_output_llava_format_openqa('./qa/')
    mc_list = post_process_output_llava_format_multi_choice('./mc/')
    json_list.extend(qa_list)
    json_list.extend(mc_list)
    # 1x reasoning data
    print('generating moderation explanation ...')
    re_list = post_process_output_llava_format_reason('./reason/1/', quesion_list=quesion_list, cnt=1)
    json_list.extend(re_list)
    # 5x reasoning date
    re_list = post_process_output_llava_format_reason('./reason/2/', quesion_list=quesion_list, cnt=2)
    json_list.extend(re_list)
    re_list = post_process_output_llava_format_reason('./reason/3/', quesion_list=quesion_list, cnt=3)
    json_list.extend(re_list)
    re_list = post_process_output_llava_format_reason('./reason/4/', quesion_list=quesion_list, cnt=4)
    json_list.extend(re_list)
    re_list = post_process_output_llava_format_reason('./reason/5/', quesion_list=quesion_list, cnt=5)
    json_list.extend(re_list)

    # save to a json file
    with open(json_name, 'a') as fp:
        json.dump(json_list, fp, indent=4)


if __name__ == '__main__':
    generate_json('./llava_baseline.json')
