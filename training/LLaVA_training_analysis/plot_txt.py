# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt

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

if __name__ == '__main__':

    log_path = './LLaVA_training_analysis/trainer_state.txt'
    filelist = text_readlines(log_path)

    losslist = []
    lrlist = []
    for i in range(len(filelist)):
        if 'loss' in filelist[i] and 'learning_rate' in filelist[i] and 'epoch' in filelist[i]:
            loss_v = filelist[i].split('learning_rate')[0].split('loss')[-1]
            loss_v = loss_v.split(',')[0].split(':')[-1]
            loss_v = loss_v.strip()
            loss_v = float(loss_v)
            losslist.append(loss_v)
            
            lr_v = filelist[i].split('epoch')[0].split('learning_rate')[-1]
            lr_v = lr_v.split(',')[0].split(':')[-1]
            lr_v = lr_v.strip()
            lr_v = float(lr_v)
            lrlist.append(lr_v)
    
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.plot(lrlist, label = 'lr')
    plt.legend()
    plt.show()
    
    plt.xlabel('iteration')
    plt.ylabel('value')
    plt.plot(losslist, label = 'loss')
    plt.legend()
    plt.show()