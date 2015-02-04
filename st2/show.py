#!/usr/bin/python
# coding: utf-8
#
# @file: show.py
# @date: 2015-01-30
# @brief:
# @detail:
#
#################################################################

import cv2, time, math
import numpy as np
from calc import FrameSum

FNAME = 'video/s.mp4'

cap = cv2.VideoCapture(FNAME)
cv2.namedWindow('origin')
cv2.namedWindow('calc')

last = None
opflow = None
framesum = FrameSum()

def draw_flow(img, flow, step = 16):
    ''' 在img中画光流方向 '''
    h,w = img.shape[:2]
    y,x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
    fx,fy = flow[y,x].T

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines)

    #            蓝:左      黄:下        红:右       绿:上
    colors = [ (255,0,0), (0,255,255), (0,0,255), (0,255,0) ]

    for (x1,y1),(x2,y2) in lines:
        length = np.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
        if length > 10: # 光流计算错误
            continue
            
        if length > 3: # 仅仅显示较大距离的移动
            # 根据方向决定颜色
            ang = np.arctan2(-(y2-y1), x2-x1) # y轴反方向
            ang += math.pi + math.pi/4
            ang %= math.pi * 2
            index = int(ang / (math.pi/2))
            cv2.line(img, (x1,y1), (x2,y2), colors[index], 2)
            cv2.circle(img, (x1,y1), 1, (0, 255, 0), -1)

    return img 


def draw_length(c):
    ''' c 为光流累加和，如何转换为方便显示的颜色呢？？？ '''
    img = cv2.cvtColor(c, cv2.COLOR_GRAY2BGR)
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
        framesum.append(opflow)

    last = gray

    if opflow is not None:
        m = draw_flow(img, opflow)
        c = draw_length(framesum.get_peaks())
        cv2.imshow('origin', m)
        cv2.imshow('calc', c)

    cv2.waitKey(1)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

