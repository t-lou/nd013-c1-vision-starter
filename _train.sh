#! /bin/bash

python3 ./experiments/model_main_tf2.py \
    --model_dir=./experiments/reference/ \
    --pipeline_config_path=./experiments/reference/pipeline_new.config
