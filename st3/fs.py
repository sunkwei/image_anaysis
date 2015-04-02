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
#SOURCE = 'rtsp://172.16.1.56/av0_1'
#SOURCE = 'c:/Users/sunkw/work/1.mp4'


WIDTH = 720
HEIGHT = 405

feature_params = dict(maxCorners = 500, \
        qualityLevel = 0.3, \
        minDistance = 7, \
        blockSize = 7)

lk_params = dict(winSize  = (15,15), \
        maxLevel = 2, \
        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))


class OpticalFlow:
    def __init__(self):
        self.track_len = 3
        self.detect_interval = 5
        self.tracks = []
        self.frame_idx = 0
        self.prev = None
        self.hsv = None

    def one_frame(self, frame, diff):
        vis = frame.copy()
        # 帧差阈值
        r, diff = cv.threshold(diff, 30, 255, cv.THRESH_BINARY)
        gray = diff
        if len(self.tracks) > 0:
            img0, img1 = self.prev_gray, gray
            p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
            p1, st, err = cv.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
            p0r, st, err = cv.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
            d = abs(p0 - p0r).reshape(-1, 2).max(-1)
            good = d < 1
            new_tracks = []
            for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                if not good_flag:
                    continue
                tr.append((x, y))
                if len(tr) > self.track_len:
                    del tr[0]
                new_tracks.append(tr)
                cv.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))

        
        if self.frame_idx % self.detect_interval == 0:
            mask = np.zeros_like(gray)
            mask[:] = 255
            for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                cv.circle(mask, (x, y), 5, 0, -1)
            p = cv.goodFeaturesToTrack(gray, mask = mask, **feature_params)
            if p is not None:
                for x, y in np.float32(p).reshape(-1, 2):
                    self.tracks.append([(x,y)])

        self.frame_idx += 1
        self.prev_gray = gray
        return vis

    def one_frame2(self, frame, curr):
        ''' 计算img的稠密光流'''
        if self.prev is None:
            self.prev = curr
            self.hsv = np.zeros_like(img)
            self.hsv[..., 1] = 255

        flow = cv.calcOpticalFlowFarneback(self.prev, curr, 0.5, 1, 3, 15, 3, 5, 1)
        self.prev = curr

        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        a = ang * 180 / np.pi

        # 为了方便仅仅取四个方向
        a += 45
        a %= 360
        a /= 90
        a = np.rint(a)
        a *= 90

        a = a / 2 # opencv hsv 从 0 .. 179
        self.hsv[..., 0] = a
        
        N = 10 # 光流距离阈值
        b = cv.threshold(mag, N, 255, cv.THRESH_BINARY)
        self.hsv[..., 2] = b[1]

        rgb = cv.cvtColor(self.hsv, cv.COLOR_HSV2BGR)
 
        return rgb



cap = cv.VideoCapture(SOURCE)
cv.namedWindow('origin')
cv.namedWindow('fs')

quit = False
prev = None

while not quit:
    r, img = cap.read()
    if not r:
        continue

    img = cv.resize(img, (WIDTH, HEIGHT))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if prev is None:
        h, w = HEIGHT, WIDTH
        of = OpticalFlow()
        vis = None
    else:
        diff = cv.absdiff(prev, gray)
        diff = cv.GaussianBlur(diff, (7, 7), sigmaX=0)
        vis = of.one_frame(img, diff)


    prev = gray

    if vis is not None:
        cv.imshow('origin', diff)
        cv.imshow('fs', vis)

    key = cv.waitKey(30)
    if key == 27:
        quit = True





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

