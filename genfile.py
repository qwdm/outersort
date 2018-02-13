#!/usr/bin/env python3

import random
import string
import sys
import os.path
import os

import argparse


CHUNKSIZE = 1000000


def generate_chunks(strlen, strnum):

    numchunks = strnum // CHUNKSIZE
    rest = strnum % CHUNKSIZE

    for j in range(numchunks + 1):
        if j == numchunks:
            chunksize = rest
        else:
            chunksize = CHUNKSIZE

        letters = [chr(97 + x % 26) for x in os.urandom(chunksize * strlen)]
        chunk = '\n'.join([''.join(letters[i:i+strlen]) for i in range(0, len(letters), strlen)])
         
        yield chunk


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--strlen', type=int, required=True) 
    parser.add_argument('--strnum', type=int, required=True)
    parser.add_argument('--filename', type=str, required=True)

    args = parser.parse_args()

    if os.path.exists(args.filename):
        sys.exit('%s file exists and cannot be rewrited' % args.filename)

    with open(args.filename, 'w') as f:
        for chunk in generate_chunks(args.strlen, args.strnum):
            f.write(chunk)
            f.write('\n')

if __name__ == '__main__':
    main()
