#!/usr/bin/python
# coding: utf-8
#
# @file: oflk.py
# @date: 2015-04-03
# @brief:
# @detail:
#
#################################################################

import cv2 as cv
import numpy as np


class OFTracking:
    ''' 基于稀疏光流的跟踪 '''
    def __init__(self, img, rect):
        ''' 在 rect 范围内选择角点，保存每个角点 '''
        roi = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        self.__corners = cv.goodFeaturesOfTrack(roi, 100, 0.3, 7)

    
    def update_frame(self, img):
        pass








# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

