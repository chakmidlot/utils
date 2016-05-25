from datetime import datetime
import os
import shutil


src = os.path.expanduser('~/Downloads')
dst = "/media/chakmidlot/DATA/Downloads"

lifetime = 3 * 24 * 3600


deadline = datetime.utcnow().timestamp() - lifetime


def move():
    for item in os.scandir(src):
        if item.stat().st_atime < deadline:
            shutil.move(item.path, os.path.join(dst, item.name))
            print("{} moved".format(item.path))


if __name__ == '__main__':
    move()
