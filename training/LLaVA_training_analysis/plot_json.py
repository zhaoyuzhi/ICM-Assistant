# -*- coding: utf-8 -*-
import os
import json
import matplotlib.pyplot as plt

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
    
# read a json file, return the json_content
def json_read(json_file):
    with open(json_file, 'r') as f:
        # json_content = json.load(f)
        json_content = json.loads(f.read())
        return json_content

if __name__ == '__main__':

    log_path = './LLaVA_training_analysis/trainer_state.json'
    filelist = json_read(log_path)
    
    print("epoch:", filelist["epoch"])
    print("global_step:", filelist["global_step"])
    print("train_runtime (seconds):", filelist["log_history"][-1]["train_runtime"], "train_runtime (hours):", filelist["log_history"][-1]["train_runtime"] / 3600)
    print("train_samples_per_second:", filelist["log_history"][-1]["train_samples_per_second"], "train_steps_per_second:", filelist["log_history"][-1]["train_steps_per_second"])

    losslist = []
    lrlist = []
    for i in range(filelist["global_step"]):
        #print(filelist["log_history"][i])
        losslist.append(filelist["log_history"][i]["loss"])
        lrlist.append(filelist["log_history"][i]["learning_rate"])
    
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
