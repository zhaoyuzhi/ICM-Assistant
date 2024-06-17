# -*- coding: utf-8 -*-
import os
from shutil import copyfile, move

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

def get_files_(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            fullpath = os.path.join(root, filespath)
            relapath = fullpath.split('\\')[-2] + '/' + fullpath.split('\\')[-1]
            if relapath.split('.')[-1] != 'py' and relapath.split('.')[-1] != 'txt':
                ret.append(relapath)
    return ret

def get_class(imglist):
    all_class = []
    for i in range(len(imglist)):
        class_name = imglist[i].split('/')[0]
        if class_name not in all_class:
            all_class.append(class_name)
    return all_class

# multi-layer folder creation
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == '__main__':
    
    # read the image lists
    trainlist = text_readlines('sexy_train_list.txt')
    vallist = text_readlines('sexy_val_list.txt')
    
    # 只提取class name，保存到classlist
    classlist = []
    for i in range(len(trainlist)):
        nn = trainlist[i]
        cla = nn.split('/')[0]
        if cla not in classlist:
            classlist.append(cla)
    print(classlist)
    
    # 统计每个class中的图像个数
    vlist = [0 for ii in range(len(classlist))]
    for j in range(len(trainlist)):
        nn = trainlist[j]
        cla = nn.split('/')[0]
        for k in range(len(classlist)):
            if cla == classlist[k]:
                vlist[k] += 1
    print(vlist)