#-*- coding: utf-8 -*-
"""
thumbnail: 用以生成图像缩略图
"""
import os, sys
import glob
from PIL import Image

allow_posfix = ("*.jpg", "*.png", "*.jpeg")
def thumbnail_pic(path):
    files = []
    for postfix in allow_posfix:
        files.update(glob.glob(os.path.join(path, postfix, True))

    for item in files:
        infile = os.path.join(path, item)
        im = Image.open(infile)
        im.thumbnail((128, 128))
        print(im.format, im.size, im.mode)
        fn, ext = os.path.splitext(infile)
        im.save(fn + ".thumbnail." + ext, ext)

    print("DONE")

def usage():
    print("""
    Usage: python {} <dir>
    """.format(sys.argv[0]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit()

    thumbnail_pic(sys.argv[1])