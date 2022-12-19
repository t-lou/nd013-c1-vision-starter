#! /bin/bash

# create new config
python ./edit_config.py \
    --train_dir ./data/train/ \
    --eval_dir ./data/val/ \
    --batch_size 2 \
    --checkpoint ./experiments/pretrained_model/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/checkpoint/ckpt-0 \
    --label_map ./experiments/label_map.pbtxt

# move the new config files
mkdir -p experiments/reference/
mv pipeline_new.config experiments/reference/
