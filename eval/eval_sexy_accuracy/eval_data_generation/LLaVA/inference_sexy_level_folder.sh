#!/bin/bash
export CUDA_VISIBLE_DEVICES=2

model_folder_path="/home/zyz/pretrained_models/LLaVa"
folder_file="/home/zyz/dataset/ECCV_2024_data/data/test"
save_folder_path="testset_sexy_score"
question="Is the picture sexy?"
threshold=0.5

python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-13b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-13b-mix --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-13b-mix.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-7b-mix --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-7b-mix.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.5-7b-ab-after-baseline --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-7b-after-baseline.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.6-7b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.6-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-v1.6-13b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.6-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/lvis-7b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-lvis-mix880k-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/lvis-13b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-lvis-mix880k-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-sharegpt4v-7b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-sharegpt4v-7b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/trained/ablations/llava-sharegpt4v-13b-after --folder-file ${folder_file} --save-file ${save_folder_path}/llava-sharegpt4v-13b-after.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-v1.5-7b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-v1.5-13b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.5-13b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-v1.6-vicuna-7b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.6-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-v1.6-vicuna-13b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-v1.6-13b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-ShareGPT4V-7B --folder-file ${folder_file} --save-file ${save_folder_path}/llava-sharegpt4v-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/llava-ShareGPT4V-13B --folder-file ${folder_file} --save-file ${save_folder_path}/llava-sharegpt4v-13b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/LVIS-Instruct4V-LLaVA-Instruct-mix880k-7b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-lvis-mix880k-7b.json --question "${question}" --threshold ${threshold}
python sexy_level_folder.py --model-path ${model_folder_path}/full/LVIS-Instruct4V-LLaVA-Instruct-mix880k-13b --folder-file ${folder_file} --save-file ${save_folder_path}/llava-lvis-mix880k-13b.json --question "${question}" --threshold ${threshold}
