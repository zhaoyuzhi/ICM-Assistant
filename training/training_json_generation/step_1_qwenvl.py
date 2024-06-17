# -*- coding: utf-8 -*-
import glob
import os
import json

delete_files = [
    'whole_large_bare_2022072011061720431_v2.JPEG',
    'middle_normal_202207201106175373_v2.jpg',
    'no_person_2022072011061726486_v2.jpg',
    'no_person_2022072011061752385_v2.jpg',
    'male_sexy_2022072011061754125_v2.PNG',
    'male_sexy_2022072011061753566_v2.JPEG',
    'middle_leg_2022072011061749814_v2.JPEG',
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
def post_process_output_llava_format(llm_output_folder):
    llm_output_list = get_files(llm_output_folder)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        # print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        llm_output_file = text_readlines(file_name)
        # post-process a llm_output_file
        try:
            for j, llm_output_line in enumerate(llm_output_file):
                # define error_detection symbol for this Q-A pair
                error_detection = False
                # define ids for a file
                if j == 0:
                    table_start_id = 0
                    json_start_id = 0
                # post-process question-answer table
                if j == 0:
                    name = llm_output_line
                    if name in delete_files:
                        error_detection = True
                        print(name)
                if '| Type of Question | Question | Answer |' in llm_output_line:
                    table_start_id = j
                    # print(j)
                if table_start_id > 0 and j > table_start_id + 1 and '|' in llm_output_line:
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
                        # error_detection = True
                    # post-process multiple choice questions
                    if 'Multiple Choice' in llm_output_line_type_of_question:
                        llm_output_line_question = llm_output_line_question + ' (Choices: ' + llm_output_line_choices + ')'
                        # error_detection = True
                    # post-process what and how questions
                    else:
                        llm_output_line_answer = llm_output_line_answer.replace('✓', '').replace('✘', '').replace('-',
                                                                                                                  '').strip()
                        # LLM syntax error
                        if len(llm_output_line_answer) == 0:
                            llm_output_line_answer = llm_output_line_choices
                        # if still existing error
                        if len(llm_output_line_answer) < 2:
                            # print(file_name)
                            error_detection = True
                    # add . to all answers
                    llm_output_line_answer = llm_output_line_answer.strip()
                    if not llm_output_line_answer.endswith("."):
                        llm_output_line_answer = llm_output_line_answer + "."
                    # print('yes')
                    # write a Q-A pair to json
                    if not error_detection:
                        if name in delete_files:
                            print(name)
                            continue
                        img_json = {}
                        img_json["id"] = "identity_" + name.split('.')[0] + '_pair' + str(json_start_id)
                        json_start_id += 1
                        img_json["image"] = '/home/mywu/data/sexy_check_all/' + name

                        img_json["conversations"] = [
                            {
                                "from": "user",
                                "value": '<img>' + '/home/mywu/data/sexy_check_all/' + name + '</img>\n' + llm_output_line_question
                            },
                            {
                                "from": "assistant",
                                "value": llm_output_line_answer
                            }
                        ]
                        json_list.append(img_json)
        except:
            print(file_name)
            continue

    return json_list

def post_process_output_llava_format_multi_choice(llm_output_folder):
    llm_output_list = get_files(llm_output_folder)
    json_list = []
    for i, file_name in enumerate(llm_output_list):
        # print('Now processing the %d-th file. Overall %d files.' % (i + 1, len(llm_output_list)))
        llm_output_file = text_readlines(file_name)
        # post-process a llm_output_file
        try:
            for j, llm_output_line in enumerate(llm_output_file):
                # define error_detection symbol for this Q-A pair
                error_detection = False
                # define ids for a file
                if j == 0:
                    table_start_id = 0
                    json_start_id = 0
                # post-process question-answer table
                if j == 0:
                    name = llm_output_line
                    if name in delete_files:
                        error_detection = True
                        print(name)
                if '| Question | Choices | Answer |' in llm_output_line:
                    table_start_id = j
                    # print(j)
                if table_start_id > 0 and j > table_start_id + 1 and '|' in llm_output_line and len(
                        llm_output_line.split('|')) > 7:
                    # post-process one question-answer pair
                    # llm_output_line_type_of_question = llm_output_line.split('|')[1].strip()
                    llm_output_line_question = llm_output_line.split('|')[1].strip()
                    llm_output_line_choices = ''
                    for idx in range(2, len(llm_output_line.split('|')) - 2):
                        llm_output_line_choices += '\n' + llm_output_line.split('|')[idx].strip()
                    llm_output_line_answer = llm_output_line.split('|')[-2].strip()
                    # post-process Yes or No questions
                    # if 'Yes/No' in llm_output_line_type_of_question:
                    #     if 'yes' in llm_output_line_answer.lower():
                    #         llm_output_line_answer = 'Yes'
                    #     elif 'no' in llm_output_line_answer.lower():
                    #         llm_output_line_answer = 'No'
                    #     elif '✓' in llm_output_line_answer.lower():
                    #         llm_output_line_answer = 'Yes'
                    #     elif '✘' in llm_output_line_answer.lower():
                    #         llm_output_line_answer = 'No'
                    #     else:
                    #         print(file_name)
                    #         error_detection = True
                    # post-process multiple choice questions
                    # if 'Multiple Choice' in llm_output_line_type_of_question:
                    llm_output_line_question = llm_output_line_question + ' (Choices: ' + llm_output_line_choices + ')'
                    # post-process what and how questions
                    # else:
                    #     llm_output_line_answer = llm_output_line_answer.replace('✓', '').replace('✘', '').replace('-', '').strip()
                    #     # LLM syntax error
                    #     if len(llm_output_line_answer) == 0:
                    #         llm_output_line_answer = llm_output_line_choices
                    #     # if still existing error
                    #     if len(llm_output_line_answer) < 2:
                    #         print(file_name)
                    #         error_detection = True
                    # add . to all answers
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
                        if name in delete_files:
                            print(name)
                            continue
                        img_json = {}
                        img_json["id"] = "identity_" + name.split('.')[0] + '_mc_pair' + str(json_start_id)
                        json_start_id += 1
                        img_json["image"] = '/home/mywu/data/sexy_check_all/' + name

                        img_json["conversations"] = [
                            {
                                "from": "user",
                                "value": '<img>' + '/home/mywu/data/sexy_check_all/' + name + '</img>\n' + llm_output_line_question
                            },
                            {
                                "from": "assistant",
                                "value": llm_output_line_answer
                            }
                        ]
                        json_list.append(img_json)
        except:
            print(file_name)
            continue
    return json_list


def json_stat(name=''):
    f = open(name, 'r')
    json_list = json.load(f)
    print('loaded.')
    cnt_yn= 0
    cnt_mc=0
    cnt_ans=0
    for j in json_list:
        if 'identity' in str(j['id']):
            name = j['image']
            if 'sexy' in name:
                ans = j['conversations'][1]['value'].upper()
                print(ans)
                cnt_ans += 1
                if len(ans) < 5:
                    if 'YES' in ans or 'NO' in ans:
                        cnt_yn += 1
                    if 'A.' in ans or 'B.' in ans or 'C.' in ans or 'D.' in ans or 'E.' in ans:
                        cnt_mc += 1
    print('qa:')
    print(cnt_yn)
    print('mc:')
    print(cnt_mc)
    print('wh:')
    print(cnt_ans - cnt_mc - cnt_yn)
    print(cnt_ans)


def generate_qa_wh_mc_step1(json_name='s1.json', open_qa_path='../../qa/open_qa/'):
    # load 665k data
    f = open('../../llava_v1_5_mix665k.json', 'r')
    json_list = json.load(f)
    for j in json_list:
        # print(j)
        for idx in range(len(j["conversations"])):
            j["conversations"][idx]["from"] = j["conversations"][idx]["from"].replace('human', 'user')
            j["conversations"][idx]["from"] = j["conversations"][idx]["from"].replace('gpt', 'assistant')
            if '<image>' in j["conversations"][idx]["value"]:
                j["conversations"][idx]["value"] = 'Picture 1: <img>' + '/home/mywu/data/' + j["image"] + '</img>'+ j["conversations"][idx]["value"].replace('<image>', '')

    import random
    print(json_list[:5])
    # not load 665k data
    # json_list = []
    base_folder_path = open_qa_path
    our_list = []
    # trainlist = text_readlines('20231030_xingganluolu_train_v1.txt')
    # trainlist = text_readlines('33c_train_list.txt')
    # trainlist = text_readlines('safe_train_list_folder.txt')
    trainlist = text_readlines('train_name_list.txt')

    file_name_set = set()
    for file in trainlist:
        if 'porn' not in file:
            file_name_set.add(file.split('/')[-1])
    print(len(file_name_set))
    # sample train name set
    # random.sample(file_name_set, len(file_name_set) // 2)

    # n of train images
    # print(len(file_name_set))
    for folder in glob.glob(base_folder_path + '*'):
        # print(folder)
        keywords = folder.split('/')[-1]
        if 'open_qa' in keywords:
            our_list.extend(post_process_output_llava_format(os.path.join(base_folder_path, keywords)))
        if 'multiple_choices' in keywords:
            our_list.extend(post_process_output_llava_format_multi_choice(os.path.join(base_folder_path, keywords)))

    # choose questions with selected image name set
    filtered_list = []
    # print(file_name_set)
    for j in our_list:
        name = j['image'].split('/')[-1]
        if name in file_name_set:
            filtered_list.append(j)
    print(len(filtered_list))
    # filtered_list = random.sample(filtered_list, 157000)
    # print(len(filtered_list))
    json_list.extend(filtered_list)
    print(len(json_list))
    # save to a json file
    with open(json_name, 'a') as fp:
        json.dump(json_list, fp, indent=4)


if __name__ == '__main__':
    import random
    # -------------------------------------------------
    # run this script after prompting LLM to get training JSON
    # -------------------------------------------------
    # read and post-process lists
    generate_qa_wh_mc_step1()
    # json_stat()
