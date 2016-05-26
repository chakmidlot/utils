#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import shutil
import sys


parser = argparse.ArgumentParser(description='Moves old files from one directory to another.')
parser.add_argument('-s', '--src', required=True, help='source directory')
parser.add_argument('-d', '--dst', required=True, help='destination directory')
parser.add_argument('-t', '--threshold-days', type=int, required=True,  help='days since last access to file')

args = parser.parse_args()


src = os.path.expanduser(args.src)
dst = os.path.expanduser(args.dst)

lifetime = args.threshold_days * 24 * 3600


deadline = datetime.utcnow().timestamp() - lifetime


def move():

    for item in os.scandir(src):
        if item.stat().st_atime < deadline:
            shutil.move(item.path, prepare_name(os.path.join(dst, item.name)))
            print("mongo: {}".format(item.path))


def prepare_dst_folder():
    if os.path.isfile(dst):
        sys.stderr.write('Destination is a file')
        exit(1)

    os.makedirs(dst, exist_ok=True)


def prepare_name(path):
    if not os.path.exists(path):
        return path

    dir_name = os.path.dirname(path)
    base_name = os.path.basename(path)

    if '.' not in base_name:
        name = base_name
        ext = ''
    else:
        name = '.'.join(base_name.split('.')[:-1])
        ext = '.' + base_name.split('.')[-1]

    print(name)
    i = 1
    while True:
        new_path = os.path.join(dir_name, '{}({}){}'.format(name, i, ext))
        if not os.path.exists(new_path):
            return new_path
        i += 1


if __name__ == '__main__':
    prepare_dst_folder()
    move()
