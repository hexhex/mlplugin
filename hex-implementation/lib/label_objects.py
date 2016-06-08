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

colors = [(255, 0, 0),(255, 255, 0),(0, 255, 0),(0, 255, 255),(0, 0, 255),(255, 0, 255),(255, 0, 0),(255, 191, 0),(64, 255, 0),(0, 255, 191),(0, 64, 255),(191, 0, 255),(255, 0, 64),(128, 255, 0),(255, 128, 0),(0, 255, 128),(0, 128, 255),(128, 0, 255),(255, 0, 128),(0, 255, 64),(255, 64, 0),(191, 255, 0),(0, 191, 255),(64, 0, 255),(255, 0, 191)]

def displayImage(scr, px, polygons, names, show):
    elemnum = 0

    scr.blit(px, px.get_rect())
    im = pygame.Surface(scr.get_size(), pygame.SRCALPHA, 32)
    im = im.convert_alpha()

    for (poly,color,bounds) in polygons:
        elemnum += 1

        pointlist = poly[:]
        if elemnum == len(polygons) and show:
            pointlist.append([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]])

        if len(poly) > 0:
            polyRect = pygame.draw.polygon(im, color, pointlist, 2)

            font = pygame.font.Font(None, 24)
            if len(names) > elemnum-1:   
                text = font.render(names[elemnum-1], 1, color)
                textpos = text.get_rect()
                textpos.centerx = polyRect.left + (polyRect.right-polyRect.left)/2
                textpos.centery = polyRect.bottom + (polyRect.top-polyRect.bottom)/2
                scr.blit(text, textpos)
                polygons[elemnum-1][2] = (polyRect.left,polyRect.top,polyRect.right,polyRect.bottom)

    scr.blit(im, (0,0))
    
    pygame.display.flip()


def setup(path):
    px = pygame.image.load(path)
    scr = pygame.display.set_mode( px.get_rect()[2:] )
    scr.blit(px, px.get_rect())
    pygame.display.flip()
    return scr, px

def get_color():
    global colors
    color = colors.pop()
    colors.insert(0,color)
    return color

def mainLoop(scr, px, label_list):
    names = []
    polygons = []
    pointlist = []

    polygons.append([pointlist,get_color(),0])

    mouse_position = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    n=0
    end=False
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pointlist.append(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                displayImage(scr, px, polygons, names, False)
                name = inputbox.ask(scr, 'Label')
                while name not in label_list:
                    name = inputbox.ask(scr, 'Label')
                names.append(name)
                displayImage(scr, px, polygons, names, True)
                pointlist = []
                polygons.append([pointlist,get_color(),0])
            if event.type == pygame.KEYDOWN:
                if event.key == 8:
                    if len(polygons) > 1:
                        polygons.pop()
                        polygons.pop()
                        names.pop()        
                        pointlist = []
                        polygons.append([pointlist,get_color(),0])
                        displayImage(scr, px, polygons, names, True)
                if event.key == 27:
                    n = 1
                    end = True
                if event.key == 110:
                    n = 1
        if [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]] != mouse_position:
            displayImage(scr, px, polygons, names, True)
            mouse_position = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    return (polygons, names, end)


def segment_and_label(state):
    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    if not os.path.exists('temp/labels.pkl'):
        labels = raw_input("Comma-separated list of labels: ") 
        label_list = labels.split(",")
        joblib.dump(label_list, "temp/labels.pkl", compress=1)
    else:
        label_list = joblib.load("temp/labels.pkl")

    if not os.path.exists('temp/' + state + '/objects/'):
        os.makedirs('temp/' + state + '/objects/')

    end = False    

    for item in os.listdir('scenes/' + state + '/'):

        if not os.path.exists('temp/' + state + '/objects/' + item[:-4] + '/') and not end:
            os.makedirs('temp/' + state + '/objects/' + item[:-4] + '/')
            if item[-4:] == ".jpg":
                input_path = 'scenes/' + state + '/' + item

                scr, px = setup(input_path)
                polygons, names, end = mainLoop(scr, px, label_list)

                image = cv2.imread(input_path, -1)
                
                n = 0        

                for poly in polygons:
                    n += 1
                    if n < len(polygons):
                        mask = np.zeros(image.shape, dtype=np.uint8)

                        output_path = 'temp/' + state + '/objects/' + item[:-4] + '/' + item[:-4] + '-' + str(n).zfill(3) + '-' + str(label_list.index(names[n-1])).zfill(3) + '-' + str(names[n-1]) + '-(' + str(poly[2][1]) + '-' + str(poly[2][3]) + '-' + str(poly[2][0]) + '-' + str(poly[2][2]) + ').jpg'
	
                        roi_corners = np.array([poly[0]], dtype=np.int32)

                        channel_count = image.shape[2]
                        ignore_mask_color = (255,)*channel_count
                        cv2.fillPoly(mask, roi_corners, ignore_mask_color)

                        masked_image = cv2.bitwise_and(image, mask)
                        masked_image = masked_image[poly[2][1]:poly[2][3], poly[2][0]:poly[2][2]]
                        cv2.imwrite(output_path,masked_image)

                joblib.dump((polygons), 'temp/' + state + '/objects/' + item[:-4] + '.pkl', compress=1)



