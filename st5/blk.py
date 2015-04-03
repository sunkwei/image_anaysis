#!/usr/bin/python
# coding: utf-8
#
# @file: blk.py
# @date: 2015-04-03
# @brief:
# @detail:
#
#################################################################

import numpy as np
import cv2 as cv
import sys, time


SOURCE = '../st3/student.mp4'

WIDTH, HEIGHT = 960, 540
ROWS, COLS = 3, 3

feature_params = dict(maxCorners = 500, \
        qualityLevel = 0.3, \
        minDistance = 7, \
        blockSize = 7)

lk_params = dict(winSize  = (15,15), \
        maxLevel = 2, \
        criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))


class OpticalFlow:
    def __init__(self, motions):
        self.__motions = motions
        self.__rows, self.__cols = motions.shape
        self.__prev = None
        self.__corners = np.zeros((self.__rows, self.__cols, 2))
        for r in range(0, self.__rows):
            for c in range(0, self.__cols):
                self.__corners[r][c] = [-1, -1]
        self.__next_corners = self.__corners.copy()


    def calc(self, frame):
        if self.__prev is None:
            pass
        else:
            for r in range(0, self.__rows):
                for c in range(0, self.__cols):
                    block1 = self.__get_block(frame, r, c)
                    block0 = self.__get_block(self.__prev, r, c)
                    self.__calc_lk(block0, block1, r, c)
        self.__prepare_corners(frame)
        self.__prev = frame


    def __calc_lk(self, block0, block1, r, c):
        if self.__corners[r][c][0] != -1:
            p0 = []
            p0 = np.array([[self.__corners[r][c][0], self.__corners[r][c][1]]], dtype=np.float32)
            p1, st, err = cv.calcOpticalFlowPyrLK(block0, block1, p0, None, **lk_params)
            print '%02d:%02d from %f, %f ==>' % (r,c, p0[0][0], p0[0][1]), p1
            self.__next_corners[r][c] = p1[0]
            self.__corners = self.__next_corners.copy()
            

    def draw(self, image):
        pass

    def draw_str(self, dst, (x, y), s):
        cv.putText(dst, s, (x+1, y+1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv.CV_AA)
        cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.CV_AA)


    def __prepare_corners(self, frame):
        ''' 每个小块选择一个角点 '''
        cr, cc = 0, 0
        rstep, cstep = HEIGHT / ROWS, WIDTH / COLS

        n = 0
        t0 = time.time()
        for r in range(0, self.__rows):
            for c in range(0, self.__cols):
                if self.__corners[r][c][0] == -1:
                    n += 1
                    block = self.__get_block(frame, r, c)
                    corners = cv.goodFeaturesToTrack(block, **feature_params)
                    if corners is not None:
                        self.__corners[r][c] = corners[0][0]
                else:
                    print 'prepared'
        t1 = time.time()
        print 'prepare_corners(%d) using:' % n, t1 - t0
                

    def __get_block(self, frame, r, c):
        rstep, cstep = HEIGHT / ROWS, WIDTH / COLS
        rr, cc = r*rstep, c*cstep
        block = frame[rr:rr+rstep, cc:cc+cstep]
        return block


cap = cv.VideoCapture(SOURCE)
cv.namedWindow('origin')
cv.namedWindow('block')

quit = False
motions = np.zeros((ROWS, COLS), np.int8)   # 描述每个块的方向
of = OpticalFlow(motions)

while not quit:
    r, img = cap.read()
    if not r:
        continue

    img = cv.resize(img, (WIDTH, HEIGHT))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    of.calc(gray)
    of.draw(img)

    cv.imshow('origin', img)

    if cv.waitKey(40) == 27:
        quit = True

cap.release()

 

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

