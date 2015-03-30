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
import cv2, time, math, sys

P = 0.8 # 累计时，每帧衰减
ROWS, COLS = 270, 480
THRESHOLD = 8 # 累计长度必须大于此值，才有效


class Frames:
    def __init__(self):
        self.__sums = np.zeros((ROWS, COLS, 2))

    def append(self, m):
        #self.__filter(m)
        self.__sums = self.__sums * P
        self.__sums = self.__sums + m

    def __filter(self, m):
        ''' 删除 m 中变化巨大的值，有可能是光流错误值 '''
        MAX = 10
        it = np.nditer(m)

        for r in range(0, ROWS):
            for c in range(0, COLS):
                x,y = it.next(), it.next() # 取一个点的x,y方向分量
                if math.sqrt(x*x + y*y) > MAX:
                    m[r][c][0], m[r][c][1] = 0, 0

    def length(self):
        l = self.__sums.reshape(ROWS * COLS * 2)
        x,y = l[::2], l[1::2]
        lengths = np.sqrt(x*x + y*y)
        return lengths.reshape((ROWS, COLS)) # 恢复图像形状

    def gray(self):
        ''' 返回长度的二值图，形状
        '''
        l = self.length()
        r = l / THRESHOLD
        l = np.trunc(r)
        l = l * THRESHOLD
        low, high = np.amin(l), np.amax(l)
        x = (l - low) * (255.0 / (high - low))
        g = np.uint8(x)
        retv, b = cv2.threshold(g, THRESHOLD, 255, cv2.THRESH_BINARY) # 二值化
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9, 9))
        b = cv2.erode(b, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(19, 19))
        b = cv2.dilate(b, kernel)

        m = b.copy()
        contours, hierarchy = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return b, contours, hierarchy
            


def get_opflow(prev, curr):
    ''' 计算img的稠密光流'''
    flow = cv2.calcOpticalFlowFarneback(prev, curr, 
            0.5, 1, 3, 15, 3, 5, 1)
    return flow


def save_opflow(n, flow):
    fname = 'saved/%04d.npy' % n
    print fname, 'saved'
    np.save(fname, flow)

def load_opflow(n):
    fname = 'saved/%04d.npy' % n
    return np.load(fname)
        

if __name__ == '__main__':
    save = False

    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        save = True

    video = cv2.VideoCapture('video/s.mp4')

    if not save:
        cv2.namedWindow('gray')
        cv2.moveWindow('gray', 0, 340)
        cv2.namedWindow('video')
        cv2.moveWindow('video', 0, 0)

    fs = Frames()

    #src = np.array([[0, 80], [150, 269], [479, 150], [230, 40]], np.float32)
    #dst = np.array([[0, 0], [100, 269],[400, 269],  [479, 0]], np.float32)
    #mt = cv2.getPerspectiveTransform(src, dst)
    #print mt
    
    cnt = 0
    last = None
    while True:
        f, m = video.read()
        m = cv2.resize(m, (COLS, ROWS))
        #m = cv2.warpPerspective(m, mt, (COLS, ROWS))

        cnt += 1
        if cnt % 2 == 0: # 扔帧
            continue

        g = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)

        n = int(cnt/2)
        if last is not None:
            if save:
                flow = get_opflow(last, g)
                save_opflow(n, flow)
            else:
                flow = load_opflow(n)
                fs.append(flow)

        last = g

        if save:
            continue

        gray, contours, hierarchy = fs.gray() 
        
#        for contour in contours:
#            r = cv2.boundingRect(contour)
#            tl = (r[0], r[1])
#            br = (r[0]+r[2], r[1]+r[3])
#            cv2.rectangle(m, tl, br, (0, 0, 255))
        cv2.drawContours(m, contours, -1, (0, 0, 255))

        cv2.imshow('gray', gray)
        cv2.imshow('video', m)

        key = cv2.waitKey(30)
        if key == 113: # 'q'
            break


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

