import os
import json
from prettytable import PrettyTable

# ------------------------------------------------------------------
#                           base function
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
#                read the ground truth labeled data
# ------------------------------------------------------------------
def load_sexy_gt(path_sexy, path_no_sexy):
    f = open(path_sexy, encoding = 'utf-8')
    json_list = json.load(f)
    f = open(path_no_sexy, encoding = 'utf-8')
    json_list.extend(json.load(f))
    sexy_score = {}
    score_set = set()
    # read sexy score
    for j in json_list:
        img_name = j["data"]["image"].split('-')[-1]
        cnt = 0
        sum = 0
        for anno in j["annotations"]:
            try:
                # print(anno['result'][0])
                if anno['result'][0]['value']['choices'][0][0] == '-': # 如果有负数，读两位
                    sum += int(anno['result'][0]['value']['choices'][0][:2])
                else: # 如果不是负数，读一位
                    sum += int(anno['result'][0]['value']['choices'][0][0])
                cnt += 1
            except:
                pass
        if cnt == 0:
            pass
        else:
            # sum
            sum = (1. * sum / cnt)
            # 总分为5分，要除以5
            sum = sum / 5
            sexy_score[img_name] = sum
            score_set.add(sum)
        # quit()
    return sexy_score

# ------------------------------------------------------------------
#                 read the algorithm labeled data
# ------------------------------------------------------------------
def load_sexy_mc(score_path):
    sexy_score = {}
    if '.json' in score_path:
        lines = open(score_path, 'r').readlines()[1:]
        for idx in range(len(lines) // 2):
            name = lines[idx*2].split('/')[-1][:-1]
            cid = lines[idx*2+1][0]
            score = -1
            # there are 5 choices
            if cid == 'A': score = 0.
            if cid == 'B': score = 0.25
            if cid == 'C': score = 0.5
            if cid == 'D': score = 0.75
            if cid == 'E': score = 1.
            else: score = 0.
            # check score
            if score == -1:
                # print('error')
                pass
            else:
                if 'normal' in name:
                    score = score * -1
                sexy_score[name] = score
    if '.txt' in score_path:
        lines = text_readlines(score_path, mode = 'r')
        for idx in range(len(lines) // 2):
            name = lines[idx*2].split('/')[-1]
            cid = lines[idx*2+1][0]
            score = -1
            # there are 5 choices
            if cid == 'A': score = 0.
            elif cid == 'B': score = 0.25
            elif cid == 'C': score = 0.5
            elif cid == 'D': score = 0.75
            elif cid == 'E': score = 1.
            else: score = 0.
            # check score
            if score == -1:
                # print('error')
                pass
            else:
                if 'normal' in name:
                    score = score * -1
                sexy_score[name] = score
    return sexy_score

# ------------------------------------------------------------------
#                    post-processing data
# ------------------------------------------------------------------
def convert_sexy_rank_score_normalized(sexy_score):
    dMax, dMin = max(sexy_score.values()), min(sexy_score.values())
    for name, score in sexy_score.items():
        sexy_score[name] = (score - dMin) / (dMax - dMin)
    return sexy_score

def compute_mse(sexy_score_gt, sexy_score):
    sum = 0.
    file_list = set()
    file_list_gt = set()
    for name, v in sexy_score.items():
        file_list.add(name)
    for name, v in sexy_score_gt.items():
        file_list_gt.add(name)
    inter = file_list.intersection(file_list_gt)
    for file in inter:
        sum += (sexy_score_gt[file] - sexy_score[file]) * (sexy_score_gt[file] - sexy_score[file])
    mse = sum / len(inter)
    return mse

if __name__ == '__main__':

    # load human labeled data
    path_sexy = './eval_sexy_extent/eval_data_gt/project-16-at-2024-02-21-06-13-b02766f3.json'
    path_no_sexy = './eval_sexy_extent/eval_data_gt/project-17-at-2024-02-21-06-13-bda17fd7.json'
    sexy_score_gt = load_sexy_gt(path_sexy, path_no_sexy)
    
    # normalization
    # sexy_score_gt = convert_sexy_rank_score_normalized(sexy_score_gt)

    # read ground truth lists
    extent_folder_path = './eval_sexy_extent/result_sexy_degree_data'
    
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
        'llava_ablation_study/llava-v1.5-7b-ab11-1.txt',
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
    data_list = data_list_comparison_with_other_methods

    # evaluate
    for i, item in enumerate(data_list):

        # read
        gen_extent_path = os.path.join(extent_folder_path, item)

        # eval
        if os.path.exists(gen_extent_path):
            # load algorithm labeled data
            sexy_score_extent = load_sexy_mc(gen_extent_path)

            # normalization
            # sexy_score_extent = convert_sexy_rank_score_normalized(sexy_score_extent)

            # compute the MSE
            mse = compute_mse(sexy_score_extent, sexy_score_gt)
            
            # print the method name
            print(item)
            
            # calculate results and compute metrics
            table = PrettyTable(['MSE'])
            table.add_row([mse])
            print(table)
