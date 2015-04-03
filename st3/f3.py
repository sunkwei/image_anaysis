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

SOURCE = 0

cap = cv.VideoCapture(SOURCE)
cv.namedWindow('origin')
cv.namedWindow('diff')

quit = False
df = FrameDiff()

while not quit:
    r, img = cap.read()
    if not r:
        continue

    img = cv.resize(img, (480, 270))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    diff = df.diff(gray)

    m = df.bindingrects(diff, None)

    cv.imshow('diff', m)

    if cv.waitKey(10) == 27:
        quit = True

cap.release()





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

