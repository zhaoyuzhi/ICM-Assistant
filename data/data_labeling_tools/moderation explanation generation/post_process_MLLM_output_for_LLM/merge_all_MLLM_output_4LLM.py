# -*- coding: utf-8 -*-
import os

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

# read a folder, return all the file names
def get_filespaths(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(filespath)
    return ret

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

if __name__ == '__main__':

    # run this after getting all results
    base_folder_path_list = ['./CoT_prompts_2/all_LLaVA_results_revised', './CoT_prompts_3/all_LLaVA_results_revised', './CoT_prompts_4/all_LLaVA_results_revised', './CoT_prompts_5/all_LLaVA_results_revised', './CoT_prompts/all_LLaVA_results_revised']
    save_folder_path = './CoT_prompts/all_LLaVA_results_all_revised'
    MLLM_output_name_list = get_filespaths(base_folder_path_list[0])
    check_path(save_folder_path)
    
    print(MLLM_output_name_list)

    for i, MLLM_output_name in enumerate(MLLM_output_name_list):
        # read all files output
        content_MLLM_output_name_list = []
        for j in range(len(base_folder_path_list)):
            llava_list = text_readlines(os.path.join(base_folder_path_list[j], MLLM_output_name))
            content_MLLM_output_name_list.append(llava_list)

        # merge all files output
        # -----------------------------------------------------------
        # the first file is regarded as anchor
        # only read the image name from the anchor
        save_list = []
        for k in range(len(content_MLLM_output_name_list[0]) // 2):
            image_name = content_MLLM_output_name_list[0][k * 2]
            save_list.append(image_name) # save the image name to the save_list
            save_list.append(content_MLLM_output_name_list[0][k * 2 + 1]) # save the prompting result from the anchor to the save_list
            for l in range(1, len(content_MLLM_output_name_list)):
                image_name_index = content_MLLM_output_name_list[l].index(image_name)
                save_list.append(content_MLLM_output_name_list[l][image_name_index + 1]) # save the prompting result from the current prompting file to the save_list
        # -----------------------------------------------------------
        
        # save
        save_path = os.path.join(save_folder_path, MLLM_output_name)
        text_save(save_list, save_path)
        
