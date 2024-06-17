import os
import numpy as np
import matplotlib.pyplot as plt

image_format = ['.JPG', '.JPEG', '.PNG', '.jpg', '.jpeg', '.png']

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

# post-process one question-answer pair
def post_process_output_multi_choice(llm_output_line):
    # post-process one question-answer pair
    llm_output_line_question = llm_output_line.split('|')[1].strip()
    for idx in range(len(llm_output_line_question)):
        if  (ord(llm_output_line_question[idx]) >= 65 and ord(llm_output_line_question[idx]) <= 90) or (ord(llm_output_line_question[idx]) >= 97 and ord(llm_output_line_question[idx]) <= 122):
            llm_output_line_question = llm_output_line_question[idx:]
            break
    llm_output_line_choices = ''
    for idx in range(2, len(llm_output_line.split('|')) - 2):
        llm_output_line_choices += '\n' + llm_output_line.split('|')[idx].strip()
    llm_output_line_question_index = np.random.randint(0, len(mc_question_list))
    llm_output_line_choices += '\n ' + mc_question_list[llm_output_line_question_index]
    llm_output_line_answer = llm_output_line.split('|')[-2].strip()
    # post-process multiple choice questions
    llm_output_line_question = llm_output_line_question + llm_output_line_choices
    # add . to all answers
    llm_output_line_answer = llm_output_line_answer.strip().upper()[:2]
    if 'A' in llm_output_line_answer: llm_output_line_answer = 'A.'
    if 'B' in llm_output_line_answer: llm_output_line_answer = 'B.'
    if 'C' in llm_output_line_answer: llm_output_line_answer = 'C.'
    if 'D' in llm_output_line_answer: llm_output_line_answer = 'D.'
    if 'E' in llm_output_line_answer: llm_output_line_answer = 'E.'
    # add . to all answers
    if not llm_output_line_answer.endswith("."):
        llm_output_line_answer = llm_output_line_answer + "."
    return llm_output_line_question, llm_output_line_answer

# post-process one question-answer pair
def post_process_output_openqa(llm_output_line):
    llm_output_line_type_of_question = llm_output_line.split('|')[1].strip()
    llm_output_line_question = llm_output_line.split('|')[2].strip()
    llm_output_line_choices = llm_output_line.split('|')[3].strip()
    llm_output_line_answer = llm_output_line.split('|')[-2].strip()
    # post-process questions
    llm_output_line_question = llm_output_line_question + ' Please answer only with yes or no.'
    # post-process Yes or No answers
    flag = True
    if 'Yes/No' in llm_output_line_type_of_question:
        if 'Yes' in llm_output_line_answer.lower():
            llm_output_line_answer = 'Yes'
        elif 'No' in llm_output_line_answer.lower():
            llm_output_line_answer = 'No'
        elif 'yes' in llm_output_line_answer.lower():
            llm_output_line_answer = 'Yes'
        elif 'no' in llm_output_line_answer.lower():
            llm_output_line_answer = 'No'
        elif '✓' in llm_output_line_answer.lower():
            llm_output_line_answer = 'Yes'
        elif '✘' in llm_output_line_answer.lower():
            llm_output_line_answer = 'No'
        else:
            flag = False
    # add . to all answers
    llm_output_line_answer = llm_output_line_answer.strip()
    if not llm_output_line_answer.endswith("."):
        llm_output_line_answer = llm_output_line_answer + "."
    if flag:
        return llm_output_line_question, llm_output_line_answer
    else:
        return '', ''

if __name__ == '__main__':

    # multiple-choice q-a pairs
    mc_for_labeling_list_path = 'mc_for_labeling_list.txt'
    mc_for_labeling_list = text_readlines(mc_for_labeling_list_path)
    mc_for_labeling_q_save_list = []
    mc_for_labeling_a_save_list = []

    for i, mc_llm_output_file in enumerate(mc_for_labeling_list):
        if '_202' in mc_llm_output_file:
            mc_llm_output_file_extend = mc_llm_output_file.split('_202')[0] + '/' + mc_llm_output_file
            for j in range(1, len(mc_for_labeling_list) - i):
                if len(mc_for_labeling_list[i + j]) > 1:
                    llm_output_line_question, llm_output_line_answer = post_process_output_multi_choice(mc_for_labeling_list[i + j])
                    print(i + j, mc_llm_output_file, repr(llm_output_line_question), repr(llm_output_line_answer))
                    # save the content
                    mc_for_labeling_q_save_list.append(mc_llm_output_file_extend)
                    mc_for_labeling_q_save_list.append(repr(llm_output_line_question)[1:-1])
                    mc_for_labeling_a_save_list.append(mc_llm_output_file_extend)
                    mc_for_labeling_a_save_list.append(llm_output_line_answer)
                else:
                    break

    text_save(mc_for_labeling_q_save_list, 'mc_q_prompts.txt')
    text_save(mc_for_labeling_a_save_list, 'mc_a_prompts.txt')

    # openqa q-a pairs
    openqa_for_labeling_list_path = 'openqa_for_labeling_list.txt'
    openqa_for_labeling_list = text_readlines(openqa_for_labeling_list_path)
    openqa_for_labeling_q_save_list = []
    openqa_for_labeling_a_save_list = []

    for i, qa_llm_output_file in enumerate(openqa_for_labeling_list):
        if '_202' in qa_llm_output_file:
            qa_llm_output_file_extend = qa_llm_output_file.split('_202')[0] + '/' + qa_llm_output_file
            for j in range(1, len(openqa_for_labeling_list) - i):
                if len(openqa_for_labeling_list[i + j]) > 1:
                    llm_output_line_question, llm_output_line_answer = post_process_output_openqa(openqa_for_labeling_list[i + j])
                    if len(llm_output_line_question) > 0:
                        print(i + j, qa_llm_output_file, repr(llm_output_line_question), repr(llm_output_line_answer))
                        # save the content
                        openqa_for_labeling_q_save_list.append(qa_llm_output_file_extend)
                        openqa_for_labeling_q_save_list.append(llm_output_line_question)
                        openqa_for_labeling_a_save_list.append(qa_llm_output_file_extend)
                        openqa_for_labeling_a_save_list.append(llm_output_line_answer)
                else:
                    break
    
    text_save(openqa_for_labeling_q_save_list, 'openqa_q_prompts.txt')
    text_save(openqa_for_labeling_a_save_list, 'openqa_a_prompts.txt')
