export CUDA_VISIBLE_DEVICES=0

#python inference_qwenvl.py --model-path "/home/zyz/pretrained_models/Qwen-VL" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > qwen-vl-7b.txt
python inference_qwenvl.py --model-path "/home/zyz/pretrained_models/Qwen-VL-Chat" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > qwen-vl-chat-7b.txt
