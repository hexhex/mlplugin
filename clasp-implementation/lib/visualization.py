import pygame, sys
import PIL.Image
import random
from Tkinter import *
import inputbox
import cv2
import numpy as np
import os
import shutil
from sklearn.externals import joblib

pygame.init()

def setup(path,polygons,names,scene,model):
    elemnum = 0
    px = pygame.image.load(path)
    srf = pygame.Surface(px.get_rect()[2:])
    srf.set_alpha(128)
    srf.set_colorkey((0,0,0))

    tsrf = pygame.Surface(px.get_rect()[2:])
    tsrf.set_colorkey((0,0,0))

    for (poly,color,bounds) in polygons:
        elemnum += 1

        if len(poly) > 0:
            polyRect = pygame.draw.polygon(srf, color, poly, 0)

            font = pygame.font.Font(None, 24)
            if len(names) > elemnum-1:   
                text = font.render(names[elemnum-1], 1, pygame.Color(255, 255, 255, 255))
                textpos = text.get_rect()
                textpos.centerx = polyRect.left + (polyRect.right-polyRect.left)/2
                textpos.centery = polyRect.bottom + (polyRect.top-polyRect.bottom)/2
                tsrf.blit(text, textpos)
    px.blit(srf,(0,0))
    px.blit(tsrf,(0,0))
    if model:
        pygame.image.save(px,'results/' + scene + '-model.jpg')
    else:
        pygame.image.save(px,'results/' + scene + '-hex.jpg')


def visualize(predictions,scene,model=False):
    if not os.path.exists('results/'):
        os.makedirs('results/')

    names = []
    sorted_predictions = sorted(predictions, key=lambda tup: int(tup[0]))

    n = 1
    for pred in sorted_predictions:
        while pred[0] != str(n):
            n += 1
            names.append("v")
        names.append(pred[1])
        n += 1

    polygons = joblib.load('temp/test/objects/' + scene + '.pkl')

    setup('scenes/test/' + scene + '.jpg',polygons,names,scene,model)



