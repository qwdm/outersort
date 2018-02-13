#!/usr/bin/env python3

import random
import bisect
import os
import sys
import re


def get_n_splits(filename):

    filesize = os.path.getsize(filename)  # in bytes

    try:
        meminfo = open('/proc/meminfo').read()
        matched = re.search(r'MemAvailable:\s+(\d+)', meminfo)
        mem_available = int(matched.groups()[0]) * 1024  # kB -> bytes
    except:
        mem_available = 1024 * 1024 * 1024  # 1GB has almost any machine nowdays (c)
        print('available memory set to 1GB, cannot measure memory', file=sys.stderr)

    n_splits = 10 * (filesize // mem_available + 1)  # 10 just for test purpouses, it takes long time to test on really big data
                                                     # and for less memory usage while working

    ## if filesize < mem_available one can sort file just in memory, but we want to test our algorightm

    return n_splits


def get_quantiles(filename, n_splits):

    filesize = os.path.getsize(filename)  
    
    alpha = min(1, (10 * 1024 * 1024 / filesize))

    sample = []
    with open(filename) as infile:
        for line in infile:
            if random.random() < alpha:
                sample.append(line)
            lastline = line

    sample.sort()

    quantiles = [sample[round(i*len(sample)/n_splits)] for i in range(1,n_splits)]
    quantiles = [line.strip() for line in quantiles]

    return quantiles


def make_split_filenames(tmpdir, n_splits):
    return [os.path.join(tmpdir, 'split%04d' % n) for n in range(n_splits)]


def make_splits(filename, tmpdir, n_splits):

    quantiles = get_quantiles(filename, n_splits)
    
    try:
        infile = open(filename)
        splits = [open(split_filename, 'w') for split_filename in make_split_filenames(tmpdir, n_splits)]

        for line in infile:
            index = bisect.bisect_left(quantiles, line)
            splits[index].write(line)

    finally:
        infile.close()
        for split in splits:
            split.close()


def sort_splits(tmpdir, n_splits):
    for split_filename in make_split_filenames(tmpdir, n_splits):
        with open(split_filename) as split_file:
            lines = split_file.readlines()

        lines.sort()

        with open(split_filename, 'w') as split_file:
            split_file.writelines(lines)
        

def merge(filename, tmpdir, n_splits):

    with open(filename + '_tmp', 'w') as outfile:
        for split_filename in make_split_filenames(tmpdir, n_splits):
            with open(split_filename) as split_file:
                lines = split_file.readlines()
                outfile.writelines(lines)

            os.remove(split_filename)

    os.remove(filename)
    os.rename(filename + '_tmp', filename)


def main():

    # simple sys.argv, argparse is overkill here
    filename = sys.argv[1]
    n_splits = int(sys.argv[2]) if len(sys.argv) == 3 else get_n_splits(filename)

    print('Use %s splits' % n_splits, file=sys.stderr)

    tmpdir = os.path.dirname(os.path.abspath(filename))
    tmpdir = os.path.join(tmpdir, filename + '_tmpdir')

    try:
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)
        else:
            sys.exit('%s directory exists, cannot use this path as tmpdir' % tmpdir)

        make_splits(filename, tmpdir, n_splits)
        sort_splits(tmpdir, n_splits)
        merge(filename, tmpdir, n_splits)

    finally:
        if os.path.exists(tmpdir):
            for filename in os.listdir(tmpdir):
                os.remove(os.path.join(tmpdir, filename))
            os.rmdir(tmpdir)


if __name__ == '__main__':
    main()
