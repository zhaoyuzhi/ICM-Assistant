MODEL=eva_clip_l_14_336
DATA_PATH=/home/zyz/dataset/ECCV_2024_data_ftclip/sexy-determination/

python run_class_finetuning.py --model ${MODEL} \
--data_path ${DATA_PATH} --input_size 336 \
--num_workers 1 --output_dir ./output --batch_size 128 --lr 6e-4 --update_freq 4 \
--warmup_epochs 5 --epochs 30 --layer_decay 0.65 --backbone_decay 1 --drop_path 0 \
--dist_eval --eval_all --clip_mean_and_std --layer_scale_init_value 0 --abs_pos_emb \
--disable_rel_pos_bias --weight_decay 0.05 --mixup 0 --cutmix 0 --nb_classes 2 \
--model_ema_decay 0.998