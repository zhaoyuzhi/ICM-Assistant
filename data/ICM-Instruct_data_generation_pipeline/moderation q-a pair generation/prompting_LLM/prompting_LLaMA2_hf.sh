export CUDA_VISIBLE_DEVICES=0,1,2,3

python prompting_LLaMA2_hf.py --txt_path txt/lower_hips.txt --q_type mix
