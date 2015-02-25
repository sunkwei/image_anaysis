#!/usr/bin/python
# coding: utf-8
#
# @file: n_show.py
# @date: 2015-02-03
# @brief: 从 saved/%03d.npy 加载，缓冲10帧, 计算10帧的累计光流长度，
# @detail:
#
#################################################################


import numpy as np
import cv2, time, math

P = 1.0 # 累计时，每帧衰减
ROWS, COLS = 270, 480 
THRESHOLD = 5.0 # 累计长度小于此，则置零

def load(n):
    fname = 'saved/%03d.npy' % n
    m = np.load(fname)
    return m

def save_length(n, l):
    fname = 'length/%03d.npy' % n
    np.save(fname, l)


class Frames:
    def __init__(self):
        self.__sums = np.zeros((ROWS, COLS, 2))

    def append(self, m):
        # self.__chk(m)
        self.__sums = self.__sums * P
        self.__sums = self.__sums + m

    def __chk(self, m):
        ''' 如果 m 的 sqrt(x*x + y*y) > MAX 则认为是光流探测错误，改为 0
        '''
        it = np.nditer(m)
        for r in range(0, ROWS):
            for c in range(0, COLS):
                x,y = it.next(), it.next()
                if x*x + y*y > 10:
                    m[r][c][0] = 0
                    m[r][c][1] = 0


    def length(self):
        l = self.__sums.reshape(ROWS * COLS * 2)
        x,y = l[::2], l[1::2]
        lengths = np.sqrt(x*x + y*y)
        return lengths.reshape((ROWS, COLS)) # 恢复图像形状

    def gray(self):
        ''' 返回长度的灰度图，[0 .. 255]
        '''
        l = self.length()
        r = l / THRESHOLD
        l = np.trunc(r)
        l = l * THRESHOLD
        low, high = np.amin(l), np.amax(l)
        x = (l - low) * (255.0 / (high - low))
        return np.uint8(x)


def get_opflow(prev, curr):
    ''' 计算img的稠密光流'''
    flow = cv2.calcOpticalFlowFarneback(prev, curr, 
            0.5, 1, 3, 15, 3, 5, 1)
    return flow


if __name__ == '__main__':
    cv2.namedWindow('gray')
    fs = Frames()

    video = cv2.VideoCapture('video/s.mp4')

    last = None
    while True:
        f, m = video.read()
        g = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)

        if last is not None:
            flow = get_opflow(last, g)
            fs.append(flow)

        last = g

        gray = fs.gray() 

#        cv2.erode(gray, gray)
#        cv2.dilate(gray, gray)

        cv2.imshow('gray', gray)

        c = cv2.waitKey(10)
        if c == 'q':
            break;


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

