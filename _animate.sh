#! /bin/bash

DIR_IN="./data/test"
DIR_OUT="./gifs"

rm -rf ${DIR_OUT}
mkdir -p ${DIR_OUT}

for f in ${DIR_IN}/*.tfrecord
do
    python inference_video.py \
        --labelmap_path ./label_map.pbtxt \
        --model_path ./experiments/reference/exported/saved_model \
        --tf_record_path ${f} \
        --config_path ./experiments/reference/pipeline_new.config \
        --output_path ${DIR_OUT}/$(basename $f).gif
done