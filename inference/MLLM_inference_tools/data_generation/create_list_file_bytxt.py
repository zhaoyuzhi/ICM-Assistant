# -*- coding: utf-8 -*-
import os

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

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

# read a folder, return the complete path of all files
def get_files_without_txt(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if '.txt' not in filespath:
                ret.append(os.path.join(root, filespath))
    return ret

# read a folder, return the complete path of all files
def get_files_only_txt(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if '.txt' in filespath:
                ret.append(os.path.join(root, filespath))
    return ret

if __name__ == '__main__':

    # define the fixed prefix and postfix
    prefix = 'Prior information: It is known that '
    postfix = ' Answer the following 2 questions sequentially based on the information. Do not use the first person, answer with an objective description: 1. Please use the prior information to describe the image in detail; 2. Please use the prior information to describe the overall atmosphere of the image and explain why this image is sexy based on the image content and the overall atmosphere.'

    # read
    folder_path = 'data'
    txtlist = get_files_only_txt(folder_path)

    # save to a list
    savelist = []
    for i in range(len(txtlist)):
        
        # read the pre-defined content and define questions
        content = text_readlines(txtlist[i], mode = 'r')[0]
        question = prefix + content + postfix

        # get the path
        txtname = txtlist[i].replace(folder_path, '')[1:]
        imgname = txtname.replace('\\', '/')

        # save to a list
        savelist.append(imgname)
        savelist.append(question)
        
    text_save(savelist, 'list_file.txt', mode = 'a')