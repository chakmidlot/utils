#!/usr/bin/env python

"""
Shows movie by chunks.

TODO:
* Maybe I need to add possibility to store many checkpoints for many movies.
"""

from __future__ import print_function

import argparse
import os

__version__ = '0.1.1'

parser = argparse.ArgumentParser(description='Runs movie in mplayer by chunks')
parser.add_argument('-m', '--movie-path', help='path to movie file')
parser.add_argument('-w', '--watching-time', type=int, help='watching time in seconds')
parser.add_argument('-f', '--forward', action='store_true', help='slide forward on one batch')
parser.add_argument('-b', '--backward', action='store_true', help='slide back on one batch')
parser.add_argument('-V', '--version', action='version', version='Version: {}'.format(__version__))

args = parser.parse_args()

checkpoint_path = os.path.join(os.path.dirname(__file__), 'movie_checkpoint.dat')


if not os.path.exists(checkpoint_path):
    with open(checkpoint_path, 'wb') as fp:
        fp.write(b'0')

start = int(open(checkpoint_path, 'rb').read()) or 0

if args.backward:
    value = start - args.watching_time if start > args.watching_time else 0
    open(checkpoint_path, 'wb').write(str(value).encode())
    print('back to {}'.format(value))

elif args.forward:
    value = start + args.watching_time
    open(checkpoint_path, 'wb').write(str(value).encode())
    print('forward to {}'.format(value))

else:
    open(checkpoint_path, 'wb').write(str(start + args.watching_time).encode())

    os.system('mplayer -fs -ss {} -endpos {} {}'.format(start, args.watching_time, args.movie_path))
