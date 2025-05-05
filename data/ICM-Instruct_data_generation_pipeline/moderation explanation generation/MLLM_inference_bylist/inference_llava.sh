export CUDA_VISIBLE_DEVICES=2

model_path="/home/zyz/pretrained_models/LLaVa/full/llava-v1.5-13b"
folder_file="/home/zyz/dataset/20231113_data"
list_file="list_file.txt"
sub_folder="bite_finger"

python inference_llava.py --model-path ${model_path} --folder-file ${folder_file}/${sub_folder} --list-file ${list_file} > ${sub_folder}.txt
