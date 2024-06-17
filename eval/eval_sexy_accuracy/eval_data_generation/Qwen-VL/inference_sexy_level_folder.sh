#!/bin/bash
export CUDA_VISIBLE_DEVICES=3

folder_file="/home/zyz/dataset/ECCV_2024_data/data/test"
save_folder_path="testset_sexy_score"

python sexy_level_folder.py --model-path "/home/zyz/pretrained_models/Qwen-VL-Chat" --folder-file ${folder_file} --save-file ${save_folder_path}/qwen-vl-chat-7b.json
python sexy_level_folder.py --model-path "/home/zyz/pretrained_models/other_trained/qwen-vl-chat-7b-after" --folder-file ${folder_file} --save-file ${save_folder_path}/qwen-vl-chat-7b-after.json
