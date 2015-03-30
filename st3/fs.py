#!/usr/bin/python
# coding: utf-8
#
# @file: fs.py
# @date: 2015-03-30
# @brief:
# @detail: 利用帧差法
#
#################################################################

import numpy as np
import cv2 as cv
import time, math, sys
import collections as cl
from common import clock, nothing

#SOURCE = 0
SOURCE = 'student.mp4'
#SOURCE = 'rtsp://172.16.1.56/av0_0?tcp=1'
#SOURCE = 'c:/Users/sunkw/work/1.mp4'

MHI_DURATION = 1.0
MAX_TIME_DELTA = 0.5
MIN_TIME_DELTA = 0.1

cap = cv.VideoCapture(SOURCE)
cv.namedWindow('origin')
cv.namedWindow('fs')

quit = False
prev = None

while not quit:
    r, img = cap.read()
    if not r:
        continue

    img = cv.resize(img, (480, 270))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if prev is None:
        h, w = 270, 480
        diff = np.zeros_like(gray)
        mh = np.zeros((h, w), np.float32)
    else:
        diff = cv.absdiff(prev, gray)

        stamp = clock()
        cv.updateMotionHistory(diff, mh, stamp, MHI_DURATION)

        mg_mask, mg_orient = cv.calcMotionGradient(mh, MAX_TIME_DELTA, MIN_TIME_DELTA, apertureSize=5)


    prev = gray

    cv.imshow('origin', img)
    cv.imshow('fs', diff)

    key = cv.waitKey(30)
    if key == 27:
        quit = True





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

