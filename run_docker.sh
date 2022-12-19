#! /bin/bash
BASE=$(dirname $(realpath $0))

docker run \
    --runtime=nvidia \
    -v ${BASE}:/app/project/ \
    --network=host \
    -ti \
    --shm-size=14gb \
    project-dev bash
