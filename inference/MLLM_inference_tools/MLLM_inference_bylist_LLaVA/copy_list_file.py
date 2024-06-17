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

if __name__ == '__main__':

    '''
    copy the existing file list (in all_path) based on the name list (in tar_path)
    '''

    # all files
    all_path = 'C:\\Users\\z84295503\\Desktop\\code_yewu\\20231113_MLLM-inference-code-main\\CoT_prompts\\all_LLaVA_inputs'
    all_filelist = get_files(all_path)
    #print(filelist)
    tar_path = 'train_name_list.txt'
    tar_namelist = text_readlines(tar_path)
    #print(tar_namelist)

    # loop all files
    count = 0
    for i, filename in enumerate(all_filelist):
        # read files only containing 'list_file.txt'
        if 'list_file.txt' in filename:
            print(filename)
            # define the lists for saving
            save_filelist = []
            save_namelist = []
            # read all contents
            filecontentlist = text_readlines(filename)
            for j in range(len(filecontentlist) // 2):
                cur_imagename = filecontentlist[j * 2]
                cur_prompt = filecontentlist[j * 2 + 1]
                # judge
                if cur_imagename in tar_namelist:
                    save_namelist.append(cur_imagename)
                    save_filelist.append(cur_imagename)
                    save_filelist.append(cur_prompt)
                    count += 1
            # save
            save_folder_path = '\\'.join(filename.split('\\')[:-1]).replace('CoT_prompts', 'CoT_prompts_5')
            check_path(save_folder_path)
            text_save(save_namelist, os.path.join(save_folder_path, 'name_list.txt'))
            text_save(save_filelist, os.path.join(save_folder_path, 'list_file.txt'))
            print(cur_imagename.split('_202')[0], len(save_namelist), save_folder_path)
    print(count)
    