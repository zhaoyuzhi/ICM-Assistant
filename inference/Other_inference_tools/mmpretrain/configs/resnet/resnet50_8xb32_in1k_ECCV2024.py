# 在 'configs/resnet/' 创建此文件
_base_ = './resnet50_8xb32_in1k.py'

# 使用自己的数据集目录
data_preprocessor = dict(
    num_classes=2,
    # RGB format normalization parameters
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    # convert image from BGR to RGB
    to_rgb=True,
)

train_dataloader = dict(
    batch_size=32,
    dataset=dict(
        data_root='/home/zyz/dataset/ECCV_2024_data_mmpretrain',
        with_label=True,                # or False for unsupervised tasks
        classes=['not_sexy', 'sexy']  # The name of every category.
        ),
)
val_dataloader = dict(
    batch_size=64,                  # 验证时没有反向传播，可以使用更大的 batchsize
    dataset=dict(
        data_root='/home/zyz/dataset/ECCV_2024_data_mmpretrain',
        with_label=True,                # or False for unsupervised tasks
        classes=['not_sexy', 'sexy']  # The name of every category.
        ),
)
test_dataloader = dict(
    batch_size=64,                  # 测试时没有反向传播，可以使用更大的 batchsize
    dataset=dict(
        data_root='/home/zyz/dataset/ECCV_2024_data_mmpretrain',
        with_label=True,                # or False for unsupervised tasks
        classes=['not_sexy', 'sexy']  # The name of every category.
        ),
)

# learning policy
param_scheduler = dict(
    type='MultiStepLR', by_epoch=True, milestones=[300, 600, 900], gamma=0.1)

# train, val, test setting
train_cfg = dict(by_epoch=True, max_epochs=1000, val_interval=1)

# NOTE: `auto_scale_lr` is for automatically scaling LR
# based on the actual training batch size.
# base_batch_size = (2 GPUs) x (32 samples per GPU)
auto_scale_lr = dict(base_batch_size=64)
