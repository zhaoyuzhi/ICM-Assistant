from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

from torch.utils.data import Dataset, DataLoader
from timm.data import create_loader
import torch
import torch.utils.data
import torchvision.datasets as datasets
from pathlib import Path
from PIL import Image

from .labeled_memcached_dataset import McDataset

# read a folder, return the complete path of all files
def get_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret

class CustomDataset(Dataset):
    def __init__(self, label_file_path, transform):
        self.imgs = get_files(label_file_path)
        self.transform = transform
    
    def __getitem__(self, index):
        img_path = self.imgs[index]
        img_label = img_path.split('/')[-2]

        label = 0 if img_label == 'not-sexy' else 1
        img = self.transform(Image.open(img_path).convert('RGB'))

        return img, label, img_path
    
    def __len__(self):
        return len(self.imgs)

def build_imagenet_dataset(args, is_train, transform):
    if is_train:
        dataset = datasets.ImageFolder(os.path.join(args.data_path, "train"), transform=transform)
    else:
        dataset = CustomDataset(os.path.join(args.data_path, "val"), transform=transform)

    return dataset
