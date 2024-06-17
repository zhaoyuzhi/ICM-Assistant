export CUDA_VISIBLE_DEVICES=0

python conv_bylist.py \
    --model-path /home/zyz/pretrained_models/internlm-xcomposer-7b \
    --folder-file /home/zyz/dataset/20230808_data/test/lieqi \
    --save-file save_folder
    