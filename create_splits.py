import argparse
import glob
import os
import random
import shutil

import numpy as np

from utils import get_module_logger


def copy(fns: list, dir_in: str, target: str, num: int=-1) -> list:
    '''Copy some files to the target directory, then return the name of the rest.
    args:
        fns: the candidate files
        dir_in: input directory
        target: the output path
        num: number of files to copy; if it is -1 or larger than the length of fns, all files will be copied
    return:
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


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # prepare
    fns = os.listdir(source)
    random.shuffle(fns)

    # copy
    fns = copy(fns, source, os.path.join(destination, 'test'), 10)
    fns = copy(fns, source, os.path.join(destination, 'train'), int(0.7 * len(fns)))
    fns = copy(fns, source, os.path.join(destination, 'val'), -1)

    # assure all files are used
    assert fns is None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)