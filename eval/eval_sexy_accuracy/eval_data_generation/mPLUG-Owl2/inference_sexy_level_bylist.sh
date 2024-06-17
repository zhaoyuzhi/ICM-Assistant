#!/bin/bash
export CUDA_VISIBLE_DEVICES=7

folder_file="/home/zyz/dataset/ECCV_2024_data/data/val_v2_all"
list_file="sexy_val_name_list.txt"
save_folder_path="mllm_ablation_study"
question="Is the picture sexy?"
threshold=0.5

python sexy_level_bylist.py --model-path "/home/zyz/pretrained_models/mplug-owl2-llama2-7b" --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/mplug-owl2-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path "/home/zyz/pretrained_models/other_trained/mplug-owl2-finetune" --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/mplug-owl2-7b-after.json --question "${question}" --threshold ${threshold}
