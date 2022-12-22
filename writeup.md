# Overview

As the eyes are an important method of perception in driving, camera based methods of object detection is also crucial in automonous driving perception. It can recognize other vehicles, depestrians, signs and lane markings with optical textures. With relatively low price, it also provide good detections in near field under proper conditions (such as lighting and weather).

In this project, Single-Shot-Detection method is trained and tested.

# Setup

Docker container is used in this project as virtualization method, to provide a safe and unified working environment for machine learning.

1. build the container with modified Dockerfile, there a normal user is created so that the generated files can be accessed also outside of container: `docker build -t project-dev -f Dockerfile --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg UNAME=$(whoami) .` in `build` directory.
2. login in gcloud and run `python ./download_process.py --data_dir ./data` in directory `/app/project`.
3. Split data with `python create_splits.py --source ./data/processed --destination ./data` and download the pretrained model.
4. Change config to use the real data `./_edit_config.sh`. The original config is saved as "pipeline.config.backup", and can be restored.
5. Train with `./_train.sh`, export model with `./_evaluate.sh`, and inference with some tfrecord from test.

# Dataset

The dataset contains a variation of traffic scenes, such as scenarios with parked cars and pedestrans.

![with_parked](docs/with_parked.png)
![with_ped](docs/with_ped.png)

However, the number of different types are very biased. Below is the distribution of different object types in six train tfrecords (subset).

![test](docs/test.png)

It can be observed that the number of vehicles is dominent, compared with the other two types. There are also many more frames with only vehicles. It is meaningful for the data capture, as many streets are not suited for pedestrians and bicycles; but for the model training. it may make the prediction of pedestrians and bicycles bad. If it would be observed, the data will need to be balanced between data types.

The analysis can be reproduced with script analyze_data.py.

During the training, cross-validation is used for overfitting checking. The dataset is randomly shuffled, then 10 tfrecords are chosen as test data. The reason for chosing 10 files is that we only require very detailed evaluation on the model, which is usually the purpose of test data. When the performance of the model is desired for real-world-use, then I would prefer to have 10-20% of the whole dataset as test data. Then I put 70% of the rest of data as training data, and the rest as validation data. The three parts are randomly chosen and without repetition, to avoid hidding of overfitting and biased evaluation.

# Training
