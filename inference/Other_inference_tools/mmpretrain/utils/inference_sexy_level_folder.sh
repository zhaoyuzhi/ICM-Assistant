export CUDA_VISIBLE_DEVICES=7

DATA_PATH=/home/zyz/dataset/ECCV_2024_data/data/test
MODEL_PATH=./configs
OUTPUT_PATH=./work_dirs

python ./utils/test_sexy_score_folder.py --folder_path ${DATA_PATH} --model_path ${MODEL_PATH}/resnet/resnet50_8xb32_in1k_ECCV2024.py --output_path ${OUTPUT_PATH}/resnet50_8xb32_in1k_ECCV2024/epoch_1000.pth --save_path ./test_data/resnet50_8xb32_in1k_ECCV2024.json
python ./utils/test_sexy_score_folder.py --folder_path ${DATA_PATH} --model_path ${MODEL_PATH}/resnet/resnet152_8xb32_in1k_ECCV2024.py --output_path ${OUTPUT_PATH}/resnet152_8xb32_in1k_ECCV2024/epoch_1000.pth --save_path ./test_data/resnet152_8xb32_in1k_ECCV2024.json
python ./utils/test_sexy_score_folder.py --folder_path ${DATA_PATH} --model_path ${MODEL_PATH}/densenet/densenet201_4xb256_in1k_ECCV2024.py --output_path ${OUTPUT_PATH}/densenet201_4xb256_in1k_ECCV2024/epoch_1000.pth --save_path ./test_data/densenet201_4xb256_in1k_ECCV2024.json
