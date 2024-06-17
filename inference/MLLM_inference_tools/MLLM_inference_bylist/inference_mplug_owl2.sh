export CUDA_VISIBLE_DEVICES=6

python inference_mplug_owl2.py --model-path "/home/zyz/pretrained_models/mplug-owl2-llama2-7b" --folder-file "/home/zyz/dataset/ECCV_2024_data/data/val_v2_evaluating_description" --list-file "reasoning_prompts.txt" > mplug_owl2.txt
