export CUDA_VISIBLE_DEVICES=4

#python inference_internlm_xcomposer.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer-7b" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > internlm-xcomposer-7b.txt
python inference_internlm_xcomposer.py --model-path "/home/zyz/pretrained_models/internlm-xcomposer-vl-7b" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > internlm-xcomposer-vl-7b.txt
