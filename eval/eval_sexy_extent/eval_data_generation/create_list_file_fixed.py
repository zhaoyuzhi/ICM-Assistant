# -*- coding: utf-8 -*-
import os

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

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

if __name__ == '__main__':

    # define the fixed question list
    fix_q_pos = 'This is a sexy image. Please rate the sexy extent in this image. Choices from A, B, C, D to E are progressively more sexy, with A being somewhat sexy and E being the absolutely sexy. A: somewhat sexy; B: mildly sexy; C: sexy; D: very sexy; E: absolutely sexy. Answer with the option\'s letter (A to E) from the given choices directly.'
    fix_q_neg = 'This is a unsexy image. Please rate the unsexy extent in this image. Choices from A, B, C, D to E are progressively more unsexy, with A being somewhat unsexy and E being the totally unsexy. A: somewhat unsexy; B: mildly unsexy; C: unsexy; D: quite unsexy; E: totally unsexy. Answer with the option\'s letter (A to E) from the given choices directly.'
    
    # read
    folder_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data\\data\\val_v2'
    imglist = get_files(folder_path)

    # save to a list
    savelist = []
    for i in range(len(imglist)):

        # get the path
        imgname = imglist[i].replace(folder_path, '')[1:]
        imgname = imgname.replace('\\', '/')

        # define questions and print
        if 'normal' in imgname:
            question = fix_q_neg
        else:
            question = fix_q_pos
        print(i, imgname, question)

        # save to a list
        savelist.append(imgname)
        savelist.append(question)

    text_save(savelist, 'list_file.txt', mode = 'a')