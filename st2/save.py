#!/usr/bin/python
# coding: utf-8
#
# @file: save.py
# @date: 2015-01-30
# @brief: 从 video/s.mp4 中提取连续 100 帧，保存到 saved/ 目录
# @detail:
#
#################################################################

import cv2, sys
import numpy as np

FNAME = 'video/s.mp4'

cap = cv2.VideoCapture(FNAME)

last = None
opflow = None


def get_opflow(prev, curr):
    ''' 计算img的稠密光流'''
    flow = cv2.calcOpticalFlowFarneback(prev, curr, 
            0.5, 1, 3, 15, 3, 5, 1)
    return flow

def save_opflow(flow, fname):
    np.save(fname, flow)

if __name__ == '__main__':
    skip = 0
    frames = 100

    if len(sys.argv) > 1:
        skip = int(sys.argv[1])

    while skip > 0: # 跳过 skip 帧
        f, img = cap.read()
        skip -= 1

    n = 0
    for i in range(0, 101):
        f, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if last is not None:
            opflow = get_opflow(last, gray)
            save_opflow(opflow, 'saved/%03d.npy' % n)
            n += 1

        last = gray




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

