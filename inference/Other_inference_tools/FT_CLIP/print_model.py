import argparse
import datetime
import numpy as np
import time
import torch
import torch.backends.cudnn as cudnn
import json
import os

from pathlib import Path

from timm.data.mixup import Mixup
from timm.models import create_model
from timm.loss import LabelSmoothingCrossEntropy, SoftTargetCrossEntropy
from timm.utils import ModelEma
from optim_factory import create_optimizer, get_parameter_groups, LayerDecayValueAssigner

from datasets import build_dataset
from engine_for_finetuning import train_one_epoch, evaluate
from utils import NativeScalerWithGradNormCount as NativeScaler
import utils
from scipy import interpolate
import models

import clip

import warnings

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    
    model_states = torch.load("EVA02_CLIP_L_psz14_224to336.pt")
    model_states = torch.load("CLIP-ViT-L-14-336px.pt")
    print(model_states.RecursiveScriptModule)
    for key, value in model_states.items():
        print(key)
