#!/bin/bash
export CUDA_VISIBLE_DEVICES=6

model_folder_path="/home/zyz/pretrained_models/LLaVa"
folder_file="/home/zyz/dataset/ECCV_2024_Horror_data/data_all"
list_file="horror_val_name_list.txt"
save_folder_path="ab_horror_score"
question="Is the picture horrifying?"
threshold=0.5

python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-7b-ab-after-baseline --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.5-7b-after-baseline.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-13b-mix --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.5-13b-mix.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-13b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.5-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-v1.6-7b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.6-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-v1.6-13b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.6-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/lvis-7b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-lvis-mix880k-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/lvis-13b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-lvis-mix880k-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-sharegpt4v-7b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-sharegpt4v-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/trained/ablations/llava-sharegpt4v-13b-after --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-sharegpt4v-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_bylist.py --model-path ${model_folder_path}/full/llava-v1.5-7b --folder-file ${folder_file} --list-file ${list_file} --save-file ${save_folder_path}/llava-v1.5-7b.json --question "${question}" --threshold ${threshold}
