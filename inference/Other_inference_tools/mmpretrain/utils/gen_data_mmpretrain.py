# -*- coding: utf-8 -*-
import os
from shutil import copyfile, move

# save a list to a txt
def text_save(content, filename, mode = 'a'):
    # try to save a list variable in txt file.
    # Use the following command if Chinese characters are written (i.e., text in the file will be encoded in utf-8)
    # file = open(filename, mode, encoding='utf-8')
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]) + '\n')
    file.close()

# read a txt expect EOF
def text_readlines(filename, mode = 'r'):
    # try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        # Use the following command if there is Chinese characters are read
        # file = open(filename, mode, encoding='utf-8')
        file = open(filename, mode)
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
    
    # define the source paths
    base_train_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data\\data\\train_all'
    base_val_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data\\data\\val_v2_all'
    
    # define the target paths
    save_meta_path = 'D:\\dataset\\advertisement_data\ECCV_2024_data_mmpretrain\\meta'
    save_train_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data_mmpretrain\\train'
    save_val_path = 'D:\\dataset\\advertisement_data\\ECCV_2024_data_mmpretrain\\val'

    # read the image lists
    trainlist = text_readlines('./utils/sexy_train_list.txt')
    vallist = text_readlines('./utils/sexy_val_list.txt')
    
    # 复制train到目标文件夹，按照mmpretrain格式
    for i, item in enumerate(trainlist):
        if 'normal' in item or 'no_person' in item:
            category = 'not-sexy'
        else:
            category = 'sexy'
        read_image_path = os.path.join(base_train_path, item)
        save_folder_path = os.path.join(save_train_path, category)
        check_path(save_folder_path)
        save_image_path = os.path.join(save_train_path, category, item)
        copyfile(read_image_path, save_image_path)
    
    # 复制validation到目标文件夹，按照mmpretrain格式
    for i, item in enumerate(vallist):
        if 'normal' in item or 'no_person' in item:
            category = 'not-sexy'
        else:
            category = 'sexy'
        read_image_path = os.path.join(base_val_path, item)
        save_folder_path = os.path.join(save_val_path, category)
        check_path(save_folder_path)
        save_image_path = os.path.join(save_val_path, category, item)
        copyfile(read_image_path, save_image_path)
        
    # 复制train list到目标文件夹，按照mmpretrain格式
    check_path(save_meta_path)
    save_trainlist = []
    for i, item in enumerate(trainlist):
        if 'normal' in item or 'no_person' in item:
            item_revised = 'not-sexy/' + item + ' ' + '0'
        else:
            item_revised = 'sexy/' + item + ' ' + '1'
        save_trainlist.append(item_revised)
    text_save(save_trainlist, os.path.join(save_meta_path, 'train.txt'))
    
    # 复制val list到目标文件夹，按照mmpretrain格式
    save_vallist = []
    for i, item in enumerate(vallist):
        if 'normal' in item or 'no_person' in item:
            item_revised = 'not-sexy/' + item + ' ' + '0'
        else:
            item_revised = 'sexy/' + item + ' ' + '1'
        save_vallist.append(item_revised)
    text_save(save_vallist, os.path.join(save_meta_path, 'val.txt'))
    