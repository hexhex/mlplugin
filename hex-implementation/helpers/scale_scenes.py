#!/usr/bin/python
from PIL import Image
import os, sys

paths = ['scenes/training/','scenes/test/']

def rename():
    for path in paths:
        images = os.listdir(path)[:]
        for item in images:
            os.rename(path+item,path+'c'+item)

def resize():
    for path in paths:
        n = 0
        images = os.listdir(path)[:]
        for item in images:
            if item[-4:] == ".jpg":
                im = Image.open(path+item)
                imResize = im.resize((1280,960), Image.ANTIALIAS)
                imResize.save(path+str(n).zfill(6) + '.jpg', 'JPEG', quality=90)
                os.remove(path+item)
                n += 1

rename()
resize()
