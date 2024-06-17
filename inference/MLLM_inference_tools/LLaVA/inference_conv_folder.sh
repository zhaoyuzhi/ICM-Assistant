# Uncomment if using quantization:
# --load-4bit
export CUDA_VISIBLE_DEVICES=0,1,2,3

python conv_folder.py \
    --model-path /home/zyz/pretrained_models/LLaVa/full/llava-v1-0719-336px-lora-merge-vicuna-13b-v1.3 \
    --folder-file /home/zyz/dataset/20230808_data/test/lieqi \
    --save-file save_folder
    