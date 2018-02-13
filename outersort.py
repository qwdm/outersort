#!/usr/bin/env python3

import random
import bisect
import os
import sys


def get_quantiles(filename, n_splits, strnum):
    desirable_sample_size = min(n_splits * 1000, 100000)
    sample = []
    alpha = desirable_sample_size / strnum
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


def make_splits(filename, tmpdir, n_splits, strnum):

    quantiles = get_quantiles(filename, n_splits, strnum)

    split_counters = [0] * n_splits

    
    try:
        infile = open(filename)
        splits = [open(split_filename, 'w') for split_filename in make_split_filenames(tmpdir, n_splits)]

        for line in infile:
            index = bisect.bisect_left(quantiles, line)
            splits[index].write(line)
            split_counters[index] += 1

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


def main():

    filename = sys.argv[1]
    n_splits = int(sys.argv[2])
    strnum = int(sys.argv[3])

    tmpdir = os.path.dirname(os.path.abspath(filename))
    tmpdir = os.path.join(tmpdir, filename + '_tmpdir')

    try:
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)
        else:
            sys.exit('%s directory exists, cannot use this path as tmpdir' % tmpdir)

        make_splits(filename, tmpdir, n_splits, strnum)
        sort_splits(tmpdir, n_splits)
        merge(filename, tmpdir, n_splits)

    finally:
        if os.path.exists(tmpdir):
            for filename in os.listdir(tmpdir):
                os.remove(os.path.join(tmpdir, filename))
            os.rmdir(tmpdir)


if __name__ == '__main__':
    main()
