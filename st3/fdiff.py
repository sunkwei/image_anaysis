#!/usr/bin/python
# coding: utf-8
# 
# @file: fdiff.py
# @date: 2015-04-02
# @brief:
# @detail:
#
#################################################################

import cv2 as cv
import numpy as np

class FrameDiff:
    def __init__(self):
        self.__prev = None

    def diff(self, curr):
        if self.__prev is None:
            self.__prev = curr

        d = cv.absdiff(self.__prev, curr)
        self.__prev = curr.copy()
        return d

    def bounding_rects(self, diff, image):
        ''' 根据diff，在 image 中画出变化矩形 '''
        tmp = diff.copy()

        ker = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        tmp = cv.erode(tmp, ker)
        ker = cv.getStructuringElement(cv.MORPH_RECT, (51, 51))
        tmp = cv.dilate(tmp, ker, 5)
        r, tmp = cv.threshold(tmp, 20, 255, cv.THRESH_BINARY)

        mask = np.zeros_like(image) # 用于轮廓内包含掩码

        contours, h = cv.findContours(tmp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        rcs = []
        for ct in contours:
            rect = cv.boundingRect(ct)
            rcs.append(rect)

        cv.drawContours(mask, contours, -1, (255, 255, 255), -1) # 生成掩码

        return rcs, mask




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

