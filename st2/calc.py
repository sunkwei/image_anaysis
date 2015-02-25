#!/usr/bin/python
# coding: utf-8
#
# @file: calc.py
# @date: 2015-02-01
# @brief: 
# @detail:
#
#################################################################

''' 1 累计得到光流长度的峰值，认为该峰值处周围的光流值得关注；
    2 腐蚀后，认为此处光流就是目标活动的区域；
    3 对目标区域作HOG，8方向直方图，认为是该目标的瞬时特征
    4 
'''

import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

# 衰减因子
P = 0.8

# 图像大小
ROWS, COLS = 270, 480


class FrameSum:
    ''' 保留10帧光流累加 ...
        累加之前，衰减 P
    '''
    def __init__(self):
        self.__cnt = 0
        self.__sum = np.zeros((ROWS, COLS, 2), np.float32) # 
        self.__length = np.zeros((ROWS, COLS), np.float32)

    def append(self, f):
        ''' 新增一帧光流矢量，（dx, dy)
        '''
        self.__sum *= P
        self.__sum += f

        l = f.reshape(f.size)
        x = l[::2]
        y = l[1::2]
        m = np.sqrt(x*x + y*y)
        self.__length *= P
        self.__length = self.__length + m.reshape((ROWS, COLS))
        
    def sum(self):
        return self.__sum


    def length(self):
        return self.__length


    def get_peaks(self):
        ''' 返回局部最大值
            来自：http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
        '''
        # define an 8-connected neighborhood
        neighborhood = generate_binary_structure(2, 2)

        # apply the local maximum filter; all pixel of maximal value
        # in their neighborhood are set to 1
        local_max = maximum_filter(self.__length, footprint = neighborhood) == self.__length

        # local_max is a mask that contains the peaks we are
        # looking for, but also the background.
        # In order to isolate the peaks we must remove the background from the mask

        # we create the mask of the background
        background = (self.__length == 0)

        # a little technicality: we must erode the background in order to 
        # successfully subtract it from local_max, otherwise a line will
        # appear along the background border(artifact of the local maximum filter)
        erode_background = binary_erosion(background, structure=neighborhood, border_value=1)

        # we obtain the final mask, containing only peaks,
        # by removing the background from the local_max mask
        detected_peaks = local_max - erode_background

        return detected_peaks




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

