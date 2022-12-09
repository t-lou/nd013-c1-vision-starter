#!/bin/env python3
import os
import random
import shutil

base = os.path.dirname(os.path.realpath(__file__))
dir_in = os.path.join(base, 'processed')

def copy(fns: list, target: str, num: int) -> list:
    '''Copy some files to the target directory, then return the name of the rest.
    Params:
        fns: the candidate files
        target: the output path
        num: number of files to copy; if it is -1 or larger than the length of fns, all files will be copied
    Return:
        List of the uncopied files. If none left, the return value is None.
    '''
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

# prepare
fns = os.listdir(dir_in)
random.shuffle(fns)

# copy
fns = copy(fns, os.path.join(base, 'test'), 10)
fns = copy(fns, os.path.join(base, 'train'), int(0.7 * len(fns)))
fns = copy(fns, os.path.join(base, 'val'), -1)

# assure all files are used
assert fns is None