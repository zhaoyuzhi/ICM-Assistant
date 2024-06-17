import os
from prettytable import PrettyTable

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

# evaluate a line
def eval_line(gen_line, gt_line):
    gen_choice = gen_line[0].upper()
    gt_choice = gt_line[0].upper()
    # for multiple choices: A, B, C, D
    # for yes/no questions: Yes, No (Y, N)
    if gen_choice not in ['A', 'B', 'C', 'D', 'Y', 'N']:
        return False
    else:
        if gen_choice == gt_choice:
            return True
        else:
            return False

# evaluate a file
def eval_file(gen_file, gt_file):
    # for loop
    true_count = 0
    total_count = len(gt_file) // 2
    for i in range(total_count):
        gen_line = gen_file[i * 2 + 1]
        gt_line = gt_file[i * 2 + 1]
        judge = eval_line(gen_line, gt_line)
        #print(gen_line, gt_line, judge)
        if judge:
            true_count += 1
    return true_count, total_count

if __name__ == '__main__':

    # read ground truth lists
    mc_folder_path = './eval_sexy_shortqa/result_mc_data'
    openqa_folder_path = './eval_sexy_shortqa/result_openqa_data'

    gt_mc_a_prompts_path = './eval_sexy_shortqa/eval_data_generation/mc_a_prompts.txt'
    gt_openqa_a_prompts_path = './eval_sexy_shortqa/eval_data_generation/openqa_a_prompts.txt'

    gt_mc_a_prompts_list = text_readlines(gt_mc_a_prompts_path, mode = 'r')
    gt_openqa_a_prompts_list = text_readlines(gt_openqa_a_prompts_path, mode = 'r')

    # read generated lists
    data_list_comparison_with_other_methods = [
        'llava_ablation_study/llava-v1.5-7b-after-baseline.txt',
        'raw_mllm/llava-v1.5-7b.txt',
        'raw_mllm/llava-v1.5-13b.txt',
        'raw_mllm/llava-sharegpt4v-7b.txt',
        'raw_mllm/llava-sharegpt4v-13b.txt',
        'raw_mllm/llava-lvis-mix880k-7b.txt',
        'raw_mllm/llava-lvis-mix880k-13b.txt',
        'raw_mllm/llava-v1.6-7b.txt',
        'raw_mllm/llava-v1.6-13b.txt',
        'raw_mllm/qwen-vl-chat-7b.txt',
        'raw_mllm/mplug-owl2-7b.txt',
        'raw_mllm/internlm-xcomposer-7b.txt',
        'raw_mllm/internlm-xcomposer-vl-7b.txt',
        'raw_mllm/internlm-xcomposer2-7b.txt',
        'raw_mllm/internlm-xcomposer2-vl-7b.txt'
    ]

    data_list_mllm_ablation_study = [
        'llava_ablation_study/llava-v1.5-7b-after-baseline.txt',
        'mllm_ablation_study/llava-v1.5-7b-mix.txt',
        'mllm_ablation_study/llava-v1.5-13b-after.txt',
        'mllm_ablation_study/llava-v1.5-13b-mix.txt',
        'mllm_ablation_study/llava-sharegpt4v-7b-after.txt',
        'mllm_ablation_study/llava-sharegpt4v-13b-after.txt',
        'mllm_ablation_study/llava-v1.6-7b-after.txt',
        'mllm_ablation_study/llava-v1.6-13b-after.txt',
        'mllm_ablation_study/qwen-vl-chat-7b-after.txt',
        'mllm_ablation_study/mplug-owl2-7b-after.txt',
        'mllm_ablation_study/internlm-xcomposer2-vl-7b-after.txt'
    ]

    data_list_llava_ablation_study = [
        'llava_ablation_study/llava-v1.5-7b-after-baseline.txt',
        'llava_ablation_study/llava-v1.5-7b-ab1-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab1-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab1-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-6.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-7.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-8.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-9.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-10.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-11.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-12.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-13.txt',
        'llava_ablation_study/llava-v1.5-7b-ab2-14.txt',
        'llava_ablation_study/llava-v1.5-7b-ab3-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab3-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab3-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab3-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab3-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab4-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab4-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab4-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab4-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab4-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab5-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab5-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab5-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab5-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab5-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab6-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab6-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab6-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab6-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab6-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab7-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab7-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab7-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab7-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab7-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab8-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab8-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab8-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab8-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab8-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab9-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab9-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab9-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab9-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab9-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab10-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab10-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab10-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab10-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab10-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab11-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab11-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab11-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab11-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-5.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-6.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-7.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-8.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-9.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-10.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-11.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-12.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-13.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-14.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-15.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-16.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-17.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-18.txt',
        'llava_ablation_study/llava-v1.5-7b-ab12-19.txt',
        'llava_ablation_study/llava-v1.5-7b-ab13-1.txt',
        'llava_ablation_study/llava-v1.5-7b-ab13-2.txt',
        'llava_ablation_study/llava-v1.5-7b-ab13-3.txt',
        'llava_ablation_study/llava-v1.5-7b-ab13-4.txt',
        'llava_ablation_study/llava-v1.5-7b-ab13-5.txt'
    ]

    # choose
    # data_list_comparison_with_other_methods, data_list_mllm_ablation_study, data_list_llava_ablation_study
    data_list = data_list_mllm_ablation_study

    # evaluate
    for i, item in enumerate(data_list):

        # read
        gen_mc_a_prompts_path = os.path.join(mc_folder_path, item)
        gen_openqa_a_prompts_path = os.path.join(openqa_folder_path, item)

        # eval
        if os.path.exists(gen_mc_a_prompts_path) and os.path.exists(gen_openqa_a_prompts_path):
            gen_mc_a_prompts_list = text_readlines(gen_mc_a_prompts_path, mode = 'r')
            gen_openqa_a_prompts_list = text_readlines(gen_openqa_a_prompts_path, mode = 'r')
            true_count_mc, total_count_mc = eval_file(gen_mc_a_prompts_list, gt_mc_a_prompts_list)
            true_count_openqa, total_count_openqa = eval_file(gen_openqa_a_prompts_list, gt_openqa_a_prompts_list)
            
            accuracy_total = (true_count_mc + true_count_openqa) / (total_count_mc + total_count_openqa)
            accuracy_openqa = true_count_openqa / total_count_openqa
            accuracy_mc = true_count_mc / total_count_mc

            # print the method name
            print(item)
            
            # calculate results and compute metrics
            table = PrettyTable(['Accuracy (total)', 'Accuracy (openqa)', 'Accuracy (mc)'])
            table.add_row([accuracy_total, accuracy_openqa, accuracy_mc])
            print(table)
