#!/bin/bash
export CUDA_VISIBLE_DEVICES=6

folder_file="/home/zyz/dataset/ECCV_2024_data/data/test"
save_folder_path="testset_sexy_score"
question="<ImageHere>Is the picture sexy?"
threshold=0.5

python sexy_level_folder.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer2-7b" --folder-file ${folder_file} --save-file ${save_folder_path}/internlm-xcomposer2-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer2-vl-7b" --folder-file ${folder_file} --save-file ${save_folder_path}/internlm-xcomposer2-vl-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path "/home/mywu/mywu/models/InternLM-XComposer-main-2/finetune/output/internlm-xcomposer2-7b-after" --folder-file ${folder_file} --save-file ${save_folder_path}/internlm-xcomposer2-vl-7b-after.json --question "${question}" --threshold ${threshold}
