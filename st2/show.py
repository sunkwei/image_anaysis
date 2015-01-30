#!/usr/bin/python
# coding: utf-8
#
# @file: show.py
# @date: 2015-01-30
# @brief:
# @detail:
#
#################################################################

import cv2, time
import numpy as np

FNAME = 'video/s.mp4'

cap = cv2.VideoCapture(FNAME)
cv2.namedWindow('origin')
last = None
opflow = None

def draw_flow(img, flow, step=16):
    ''' 在img中画光流方向 '''
    h,w = img.shape[:2]
    y,x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
    fx,fy = flow[y,x].T

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines)

    for (x1,y1),(x2,y2) in lines:
        if np.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)) > 3:
            cv2.line(img, (x1,y1), (x2,y2), (0,255,255), 1)
            cv2.circle(img, (x1,y1), 1, (0, 255, 0), -1)

    return img 

def get_opflow(prev, curr):
    ''' 计算img的稠密光流'''
    flow = cv2.calcOpticalFlowFarneback(prev, curr, 
            0.5, 1, 3, 15, 3, 5, 1)
    return flow

while True:
    f, img = cap.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if last is not None:
        opflow = get_opflow(last, gray)

    last = gray

    if opflow is not None:
        cv2.imshow('origin', draw_flow(img, opflow))

    cv2.waitKey(10)





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

