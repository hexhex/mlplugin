#!/usr/bin/python
from PIL import Image
import os, sys

paths = ['scenes/training/','scenes/test/']

def resize():
    for path in paths:
        n = 0
        images = os.listdir(path)[:]
        for item in images:
            if item[-4:] == ".jpg":
                im = Image.open(path+item)
                imResize = im.resize((1024,768), Image.ANTIALIAS)
                imResize.save(path+str(n).zfill(6) + '.jpg', 'JPEG', quality=90)
                os.remove(path+item)
                n += 1

resize()
