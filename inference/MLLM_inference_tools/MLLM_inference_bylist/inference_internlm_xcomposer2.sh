export CUDA_VISIBLE_DEVICES=7

#python inference_internlm_xcomposer2.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer2-7b" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > internlm-xcomposer2-7b.txt
python inference_internlm_xcomposer2.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer2-vl-7b" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > internlm-xcomposer2-vl-7b.txt
