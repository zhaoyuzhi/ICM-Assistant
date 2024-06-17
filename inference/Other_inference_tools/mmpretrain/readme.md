# Usage

## 1 Replace the original files

- 1: download the original mmpretrain project

```bash
git clone https://github.com/open-mmlab/mmpretrain
```

- 2: copy the files under this folder path to the mmpretrain project

## 2 Build the training and validation sets

- this project uses the following organization as:

```
└── meta
│   ├── train.txt
│   └── val.txt
└── train
│   ├── not-sexy
│   └── sexy
└── val
    ├── not-sexy
    └── sexy
```

- build the organization using the **utils/gen_data_mmpretrain.py**

- analyze the data using the **utils/conclude_data_statistics.py** (optional)

## 3 Training

This file (**scripts/run_dist_train.sh**) can be found in the openmmlab project.
```bash
bash scripts/run_dist_train.sh
```

## 4 Validation

This file (**utils/inference_sexy_level_bylist.sh**) concludes the sexy score for validation images.
```bash
bash utils/inference_sexy_level_bylist.sh
```

## 5 Testing

This file (**utils/inference_sexy_level_folder.sh**) concludes the sexy score for testing images.
```bash
bash utils/inference_sexy_level_folder.sh
```
