#!/usr/bin/env bash
export CUDA_VISIBLE_DEVICES=0,1

bash ./tools/dist_train.sh ./configs/resnet/resnet50_8xb32_in1k_sexy.py 2
#bash ./tools/dist_train.sh ./configs/resnet/resnet152_8xb32_in1k_sexy.py 2
#bash ./tools/dist_train.sh ./configs/densenet/densenet201_4xb256_in1k_sexy.py 2
#bash ./tools/dist_train.sh ./configs/swin_transformer/swin-large_16xb64_in1k-384px_sexy.py 8
