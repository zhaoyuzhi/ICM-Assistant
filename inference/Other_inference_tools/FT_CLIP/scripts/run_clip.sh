export CUDA_VISIBLE_DEVICES=6

MODEL=CLIP_L14_336
OUTPUT_DIR=./output
DATA_PATH=/home/zyz/dataset/ECCV_2024_data_ftclip/sexy-determination

echo $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
cp $0 $OUTPUT_DIR

python run_class_finetuning.py \
    --model ${MODEL} --data_path $DATA_PATH \
    --input_size 336 \
    --num_workers 8 \
    --output_dir ${OUTPUT_DIR} \
    --batch_size 8 --lr 6e-4 --update_freq 1 \
    --warmup_epochs 5 --epochs 30 \
    --layer_decay 0.6 \
    --drop_path 0 \
    --dist_eval --eval_all \
    --clip_mean_and_std \
    --layer_scale_init_value 0 \
    --abs_pos_emb --disable_rel_pos_bias \
    --weight_decay 0.05 --mixup 0 --cutmix 0 \
    --nb_classes 2 --model_prefix visual. \
    --model_ema --model_ema_decay 0.9998 \
