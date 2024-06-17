# Usage

## 1 Replace the original files

- 1: download the original files

```bash
git clone https://github.com/LightDXY/FT-CLIP
```

- 2: replace the original files by copying the files under this folder path

## 2 Build the training and validation sets

- this project uses the `torchvision.datasets.ImageFolder` class by defualt; therefore the data folder is organized as:

```
└── train
│   ├── not-sexy
│   └── sexy
└── val
    ├── not-sexy
    └── sexy
```

## 3 Training

```bash
bash scripts/run_clip.sh
```

## 4 Validation

This file (**scripts/eval_clip.sh**) concludes the sexy score for validation images.
```bash
bash scripts/eval_clip.sh
```

## 5 Testing

Change the **DATA_PATH** parameter in file (**scripts/eval_clip.sh**) to testing image dataset.
