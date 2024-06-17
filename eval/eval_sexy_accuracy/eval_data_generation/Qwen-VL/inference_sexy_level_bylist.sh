#!/bin/bash
export CUDA_VISIBLE_DEVICES=3

folder_file="/home/zyz/dataset/ECCV_2024_data/data/val_v2_all"
list_file="sexy_val_name_list.txt"
save_folder_path="mllm_ablation_study"

python sexy_level_bylist.py --model-path "/home/zyz/pretrained_models/Qwen-VL-Chat" --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/qwen-vl-chat-7b.json
python sexy_level_bylist.py --model-path "/home/zyz/pretrained_models/other_trained/qwen-vl-chat-7b-after" --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/qwen-vl-chat-7b-after.json
