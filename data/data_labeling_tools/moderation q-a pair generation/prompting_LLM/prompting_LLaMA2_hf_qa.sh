export CUDA_VISIBLE_DEVICES=6,7

python prompting_LLaMA2_hf.py --txt_path txt/lower_hips.txt --q_type qa
