#!/usr/bin/python
# coding: utf-8
# 
# @file: f3.py
# @date: 2015-04-02
# @brief:
# @detail:
#
#################################################################

import numpy as np
import cv2 as cv
import time, math, sys

from fdiff import FrameDiff
from oflk import OFTracking
from tracking import Tracking

SOURCE = 'student.mp4'
WIDTH, HEIGHT = 960, 540

cap = cv.VideoCapture(SOURCE)
cv.namedWindow('origin')
cv.namedWindow('diff')
cv.namedWindow('masked')

quit = False
df = FrameDiff()
tracking = Tracking()

while not quit:
    r, img = cap.read()
    if not r:
        continue

    img = cv.resize(img, (WIDTH, HEIGHT))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    diff = df.diff(gray)

    rcs, mask = df.bounding_rects(diff, img)
    regions = tracking.update(img, rcs)
    for region in regions:
        r = region.rect()
        cv.rectangle(img, (r[0], r[1]), (r[0]+r[2], r[1]+r[3]), (0,0,255), 3)


    cv.imshow('masked', cv.bitwise_and(img, mask))
    cv.imshow('diff', diff)
    cv.imshow('origin', img)

    if cv.waitKey(40) == 27:
        quit = True

cap.release()





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

