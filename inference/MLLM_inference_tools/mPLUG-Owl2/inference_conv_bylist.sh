export CUDA_VISIBLE_DEVICES=0

python conv_bylist.py \
    --model-path /home/zyz/pretrained_models/mplug-owl2-llama2-7b \
    --folder-file /home/zyz/dataset/20230808_data/test/lieqi \
    --list-file list_file.txt \
    --save-file save_folder
    