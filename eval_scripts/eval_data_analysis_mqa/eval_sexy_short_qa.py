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
def eval_file(gen_file, gen_file_, gt_file, q_list):
    # for loop
    true_count = 0
    total_count = len(gt_file) // 2
    for i in range(total_count):
        gen_line = gen_file[i * 2 + 1]
        gt_line = gt_file[i * 2 + 1]
        gen_line_ = gen_file_[i * 2 + 1]
        judge = eval_line(gen_line, gt_line)
        judge_ = eval_line(gen_line_, gt_line)
        #print(gen_line, gt_line, judge)
        if judge and (not judge_):
            print(q_list[i*2])
            print(q_list[i*2+1])
            true_count += 1

    return true_count, total_count

if __name__ == '__main__':

    # read ground truth lists
    mc_folder_path = '../../eval_sexy_short_qa/eval_data_generation/eval_mc_data'
    openqa_folder_path = '../../eval_sexy_short_qa/eval_data_generation/eval_openqa_data'
    gt_mc_a_prompts_path = '../../eval_sexy_short_qa/eval_data_generation/mc_a_prompts.txt'
    gt_openqa_a_prompts_path = '../../eval_sexy_short_qa/eval_data_generation/openqa_a_prompts.txt'
    mc_q_prompts_list = text_readlines('../../eval_sexy_short_qa/eval_data_generation/mc_q_prompts.txt', mode = 'r')
    openqa_q_prompts_list = text_readlines('../../eval_sexy_short_qa/eval_data_generation/openqa_q_prompts.txt', mode = 'r')
    gt_mc_a_prompts_list = text_readlines(gt_mc_a_prompts_path, mode = 'r')
    gt_openqa_a_prompts_list = text_readlines(gt_openqa_a_prompts_path, mode = 'r')

    # read generated lists
    data_list = [
        'mllm_ablation_study/llava-v1.5-7b-cog-lamma.txt',
        'mllm_ablation_study/llava-v1.5-7b-qwen2-cog.txt',
        # 'mllm_ablation_study/llava-v1.5-7b-qwen2-sharegpt.txt',
        # 'mllm_ablation_study/llava-v1.5-7b-nab-salt.txt',
        # 'mllm_ablation_study/llava-v1.5-7b-qwen2-cog.txt',
    ]
    # evaluate
    # for i, item in enumerate(data_list):
    # read
    gen_mc_a_prompts_path = os.path.join(mc_folder_path, 'mllm_ablation_study/llava-v1.5-7b-cog-lamma.txt')
    gen_openqa_a_prompts_path = os.path.join(openqa_folder_path, 'mllm_ablation_study/llava-v1.5-7b-cog-lamma.txt')
    gen_mc_a_prompts_path_ = os.path.join(mc_folder_path, 'mllm_ablation_study/llava-v1.5-7b-qwen2-cog.txt')
    gen_openqa_a_prompts_path_ = os.path.join(openqa_folder_path, 'mllm_ablation_study/llava-v1.5-7b-qwen2-cog.txt')

    # eval
    if os.path.exists(gen_mc_a_prompts_path) and os.path.exists(gen_openqa_a_prompts_path):
        gen_mc_a_prompts_list = text_readlines(gen_mc_a_prompts_path, mode = 'r')
        gen_openqa_a_prompts_list = text_readlines(gen_openqa_a_prompts_path, mode = 'r')
        gen_mc_a_prompts_list_ = text_readlines(gen_mc_a_prompts_path_, mode='r')
        gen_openqa_a_prompts_list_ = text_readlines(gen_openqa_a_prompts_path_, mode='r')
        true_count_mc, total_count_mc = eval_file(gen_mc_a_prompts_list, gen_mc_a_prompts_list_, gt_mc_a_prompts_list, mc_q_prompts_list)
        true_count_openqa, total_count_openqa = eval_file(gen_openqa_a_prompts_list, gen_openqa_a_prompts_list_, gt_openqa_a_prompts_list, openqa_q_prompts_list)

        accuracy_total = (true_count_mc + true_count_openqa) / (total_count_mc + total_count_openqa)
        accuracy_openqa = (true_count_mc + true_count_openqa) / (total_count_mc + total_count_openqa)
        accuracy_mc = (true_count_mc + true_count_openqa) / (total_count_mc + total_count_openqa)

        # print the method name
        # print(item)

        # calculate results and compute metrics
        table = PrettyTable(['Accuracy (total)', 'Accuracy (openqa)', 'Accuracy (mc)'])
        table.add_row([accuracy_total, accuracy_openqa, accuracy_mc])
        print(table)
