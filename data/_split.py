#!/bin/env python3
import os
import random
import shutil

base = os.path.dirname(os.path.realpath(__file__))

dir_in = os.path.join(base, 'processed')

def move(fns: list, target: str, num: int) -> list:
    if not os.path.isdir(target):
        os.mkdir(target)
    if num < 0 or num > len(fns):
        todo = fns
        ret = None
    else:
        todo = fns[:num]
        ret = fns[num:]
    for fn in todo:
        shutil.copy(os.path.join(dir_in, fn), os.path.join(target, fn))
    return ret

fns = os.listdir(dir_in)
random.shuffle(fns)

fns = move(fns, os.path.join(base, 'test'), 10)
fns = move(fns, os.path.join(base, 'train'), int(0.7 * len(fns)))
fns = move(fns, os.path.join(base, 'val'), -1)

assert fns is None