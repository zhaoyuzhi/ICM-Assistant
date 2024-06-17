#!/bin/bash
export CUDA_VISIBLE_DEVICES=4

model_folder_path="/home/zyz/pretrained_models"
folder_file="/home/zyz/dataset/ECCV_2024_data/data/val_v2"
list_file="eval_sexy_reasoning_prompts.txt"
save_folder_path="eval_sexy_reasoning_data"

python inference_internlm_xcomposer.py --model-path ${model_folder_path}/internlm-xcomposer-7b --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/internlm-xcomposer-7b.txt
python inference_internlm_xcomposer.py --model-path ${model_folder_path}/internlm-xcomposer-vl-7b --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/internlm-xcomposer-vl-7b.txt
python inference_internlm_xcomposer2.py --model-path ${model_folder_path}/internlm-xcomposer2-7b --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/internlm-xcomposer2-7b.txt
python inference_internlm_xcomposer2.py --model-path ${model_folder_path}/internlm-xcomposer2-vl-7b --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/internlm-xcomposer2-vl-7b.txt
python inference_internlm_xcomposer2.py --model-path ${model_folder_path}/other_trained/internlm-xcomposer2-vl-7b-after --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/mllm_ablation_study/internlm-xcomposer2-vl-7b-after.txt
python inference_internlm_xcomposer2.py --model-path ${model_folder_path}/other_trained/internlm-xcomposer2-vl-7b-mix --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/mllm_ablation_study/internlm-xcomposer2-vl-7b-mix.txt
python inference_mplug_owl2.py --model-path ${model_folder_path}/mplug-owl2-llama2-7b --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/mplug_owl2.txt
python inference_mplug_owl2.py --model-path ${model_folder_path}/other_trained/mplug-owl2-finetune --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/mllm_ablation_study/mplug_owl2_after.txt
python inference_qwenvl.py --model-path ${model_folder_path}/Qwen-VL-Chat --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/raw_mllm/qwen-vl-chat-7b.txt
python inference_qwenvl.py --model-path ${model_folder_path}/other_trained/qwen-vl-chat-7b-after --folder-file $folder_file --list-file $list_file > ./${save_folder_path}/mllm_ablation_study/qwen-vl-chat-7b-after.txt
