import os
import matplotlib.pyplot as plt

image_format = ['.JPG', '.JPEG', '.PNG', '.jpg', '.jpeg', '.png']

# os.walk方法:
# read a path, return a list
# root 表示当前正在访问的文件夹路径
# dirs 表示该文件夹下的子目录名list
# files 表示该文件夹下的文件list

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

if __name__ == '__main__':

    # define a valfilelist
    valfilelist = text_readlines('D:\\dataset\\advertisement_data\\ECCV_2024_data\\ECCV_2024_val_v2_name_list.txt')
    
    # obtain the file list of all LLaMA 2 results
    filelist = get_files('./CoT_prompts_1/all_LLaMA2_results')

    # get all results
    indexlist_llama2file_name = []
    indexlist_name = []
    for i, filename in enumerate(filelist):
        filecontent = text_readlines(filename)
        #print(i, filename, filecontent[0])
        # e.g., 661 ./CoT_prompts_1/all_LLaMA2_results\bite_finger_open_qa\257.txt bite_finger_20231122110742_2242.JPEG
        indexlist_llama2file_name.append(filename)
        indexlist_name.append(filecontent[0])
    
    print(len(valfilelist), len(filelist), len(indexlist_name))

    # judge whether the name in valfilelist
    mc_for_labeling_list = []
    openqa_for_labeling_list = []
    for j in range(len(valfilelist)):
        count_multiple_choices = 0
        count_open_qa = 0
        for k in range(len(indexlist_name)):
            if valfilelist[j] == indexlist_name[k]:
                if 'multiple_choices' in indexlist_llama2file_name[k] and count_multiple_choices == 0:
                    mc_for_labeling_list.extend(text_readlines(indexlist_llama2file_name[k]))
                    count_multiple_choices += 1
                elif 'open_qa' in indexlist_llama2file_name[k] and count_open_qa == 0:
                    openqa_for_labeling_list.extend(text_readlines(indexlist_llama2file_name[k]))
                    count_open_qa += 1
                else:
                    pass
    
    # revise: delete unrelated representations
    mc_for_labeling_list_revised = []
    for k in range(len(mc_for_labeling_list)):
        if '_202' in mc_for_labeling_list[k]:
            mc_for_labeling_list_revised.append('')
            mc_for_labeling_list_revised.append(mc_for_labeling_list[k])
        if 'A' in mc_for_labeling_list[k] and 'B' in mc_for_labeling_list[k] and 'C' in mc_for_labeling_list[k] and 'D' in mc_for_labeling_list[k]:
            mc_for_labeling_list_revised.append(mc_for_labeling_list[k])

    # revise: delete unrelated representations and delete what/how questions
    openqa_for_labeling_list_revised = []
    for k in range(len(openqa_for_labeling_list)):
        if '_202' in openqa_for_labeling_list[k]:
            openqa_for_labeling_list_revised.append('')
            openqa_for_labeling_list_revised.append(openqa_for_labeling_list[k])
        if 'Yes/No' in openqa_for_labeling_list[k]:
            openqa_for_labeling_list_revised.append(openqa_for_labeling_list[k])

    # save
    text_save(mc_for_labeling_list_revised, 'mc_for_labeling_list.txt')
    text_save(openqa_for_labeling_list_revised, 'openqa_for_labeling_list.txt')
