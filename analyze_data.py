import os
import shutil

import matplotlib
import matplotlib.pyplot
import cv2
import numpy

import utils

NAMES = {
    1: 'vehicle',
    2: 'pedestrian',
    4: 'cyclist',
}
MAX_LEN = 30000
MAX_IDX = 64
FREQ_OBJECTS = {k: [0] * 64 for k in NAMES.keys()}


def get_counts(batch):
    gt_classes = batch['groundtruth_classes'].numpy().tolist()
    return {c: gt_classes.count(c) for c in set(gt_classes)}


def update(counts):
    global FREQ_OBJECTS
    for k, v in counts.items():
        if v < MAX_IDX:
            FREQ_OBJECTS[k][v] += 1


def analyze(fn, dir_out):
    global FREQ_OBJECTS
    FREQ_OBJECTS = {k: [0] * MAX_IDX for k in NAMES.keys()}
    dataset = utils.get_dataset(fn)
    c = 0
    for data in dataset.shuffle(10):
        count_batch = get_counts(data)
        update(count_batch)
        c += 1
        if c > MAX_LEN:
            break

    order = sorted(list(NAMES.keys()))
    for i in order:
        matplotlib.pyplot.bar(list(range(len(FREQ_OBJECTS[i]))),
                              FREQ_OBJECTS[i],
                              label=NAMES[i])
    matplotlib.pyplot.legend()
    matplotlib.pyplot.grid(1)
    matplotlib.pyplot.title('Number of objects in batches')
    matplotlib.pyplot.xlabel('Number of objects in one frame')
    matplotlib.pyplot.ylabel('Number of Frames with the number of objects')
    fn_out = os.path.join(dir_out, os.path.basename(fn) + '.png')
    print(fn_out)
    matplotlib.pyplot.savefig(fn_out)
    matplotlib.pyplot.clf()


def analyze_set(dir_in, dir_out):
    fns = tuple(
        os.path.join(dir_in, fn) for fn in os.listdir(dir_in)
        if fn.endswith('.tfrecord'))

    if os.path.isdir(dir_out):
        shutil.rmtree(dir_out)
    os.makedirs(dir_out)

    for fn in fns[:6]:
        analyze(fn, dir_out)


analyze_set('/app/project/data/train', '/app/project/analyze/train')
analyze_set('/app/project/data/val', '/app/project/analyze/val')
analyze_set('/app/project/data/test', '/app/project/analyze/test')


def concat(dir_in, fn_out):
    img = None
    fns = tuple(
        os.path.join(dir_in, fn) for fn in os.listdir(dir_in)
        if fn.endswith('.png'))
    if len(fns) > 6:
        fns = fns[:6]

    for i, fn in enumerate(fns):
        sub = cv2.imread(fn, 1)
        row = i // 3
        col = i % 3
        if img is None:
            img = numpy.ones([sub.shape[0] * 2, sub.shape[1] * 3, 3],
                             dtype=numpy.uint8) * 255
        img[(sub.shape[0] * row):(sub.shape[0] * (row + 1)),
            (sub.shape[1] * col):(sub.shape[1] * (col + 1)), :] = sub
    cv2.imwrite(fn_out, img)


concat('/app/project/analyze/train', 'train.png')
concat('/app/project/analyze/val', 'val.png')
concat('/app/project/analyze/test', 'test.png')
