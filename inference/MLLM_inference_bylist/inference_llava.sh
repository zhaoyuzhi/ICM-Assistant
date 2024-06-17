export CUDA_VISIBLE_DEVICES=2

model_path="/home/zyz/pretrained_models/LLaVa/full/llava-v1.5-13b"
folder_file="/home/zyz/dataset/20231113_data/bite_finger"
list_file="list_file.txt"

python inference_llava.py --model-path $model_path --folder-file $folder_file --list-file $list_file > llava_bite_finger.txt
