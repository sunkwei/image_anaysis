#!/usr/bin/python
# coding: utf-8
#
# @file: opt_sum.py
# @date: 2015-03-23
# @brief:
# @detail:
#
#################################################################

import numpy as np
import cv2 as cv
import time, math, sys
import collections as cl

#SOURCE = 0
SOURCE = 'student.mp4'
#SOURCE = 'rtsp://172.16.1.56/av0_0?tcp=1'
#SOURCE = 'c:/Users/sunkw/work/1.mp4'


def get_opflow(prev, curr):
    ''' 计算img的稠密光流'''
    flow = cv.calcOpticalFlowFarneback(prev, curr, 0.5, 1, 3, 15, 3, 5, 1)
    return flow


def mask_threshold(mag):
    ''' 图像从上往下，使用不同阈值 '''
    t0,t1 = 1.0, 10.0 # 阈值从上到下每行的改变
    r,c = mag.shape
    for i in range(0, r):
        pass



cap = cv.VideoCapture(SOURCE)
size = (int(cap.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)), \
        int(cap.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)))
print size

cv.namedWindow('origin')
cv.namedWindow('flow')

prev = None
flow = None
quit = False

discard = 5
cnt = 0

while not quit:
    r, img = cap.read()
    if not r:
        time.sleep(0.1)
        continue

    cnt += 1
    if cnt % discard == 0:
        continue

    img = cv.resize(img, (480, 270))
    curr = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if prev is None:
        hsv = np.zeros_like(img)
        hsv[..., 1] = 255

        qu = cl.deque()
    else:
        flow = get_opflow(prev, curr)
        qu.append(flow)

        if len(qu) < 10:
            continue
        else:
            pass
            flow_sum = np.zeros_like(flow)
            for q in qu:
                flow_sum += q
            qu.popleft()
            flow = flow_sum

    prev = curr



    if flow is not None:
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        a = ang * 180 / np.pi

        # 为了方便仅仅取四个方向
        a += 45
        a %= 360
        a /= 90
        a = np.rint(a)
        a *= 90

        a = a / 2 # opencv hsv 从 0 .. 179
        hsv[..., 0] = a

        
#        b = mask_threshold(mag)
#        sys.exit()
        N = 10 # 光流距离阈值
        b = cv.threshold(mag, N, 255, cv.THRESH_BINARY)
        hsv[..., 2] = b[1]


#        c = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
#        hsv[..., 2] = c

        rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        
#        gray = cv.cvtColor(rgb, cv.COLOR_BGR2GRAY)
#        cv.erode(gray, gray, iterations=3)
#        cv.dilate(gray, gray, iterations=5)
        
    
        cv.imshow('flow', rgb)
        cv.imshow('origin', img)

    key = cv.waitKey(1)
    if key == 27:
        quit = True

cap.release()


