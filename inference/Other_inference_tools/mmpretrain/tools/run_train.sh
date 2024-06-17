#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0

python tools/train.py ./configs/resnet/resnet50_8xb32_in1k_sexy.py
