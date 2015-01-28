#!/usr/bin/python
# coding: utf-8
#
# @file: py_show_op_dir.py
# @date: 2015-01-27
# @brief: 显示光流的方向
# @detail:
#
#################################################################

import math
import numpy as np
from common import *
import matplotlib.pyplot as plt
from matplotlib import colors

THRESHOLD = 3 # 只有大于该值,才显示方向
ROWS = 5
COLS = 5

ds0 = load_all(ROWS * COLS) # 加载所有数据


def op_element(d0):
    '''处理原始数据, 如果某点的光流大小小于阈值,则使用黑色, 其他方向使用不同颜色标示:
    '''
    r, c = d0.shape[0], d0.shape[1] # 行,列
    dv = d0.reshape(d0.size)
    xv, yv = dv[::2], dv[1::2]          # 分离 x,y 分量

    lv = np.sqrt(xv*xv + yv*yv)
    for i in range(0, lv.size):
        if lv[i] < THRESHOLD:
            lv[i] = 0.0

    angv = np.arctan2(xv, yv) # 计算每个点的偏角, 范围 [-pi .. pi]
    colv = np.zeros(angv.size)

    for i in range(0, angv.size):
        if lv[i] < 0.000001: # 0
            continue

        # 此处不考虑水平方向,
        if angv[i] < 0:
            colv[i] = 2.5 # up
        else:
            colv[i] = 1.5

    return colv.reshape(r, c)


def show(cvs):
    cmap2 = colors.ListedColormap(['black', 'blue', 'red']) # 向上 red, 向下 blue
    bounds2 = [0, 1, 2, 3]
    norm2 = colors.BoundaryNorm(bounds2, cmap2.N)

    fig = plt.figure(1)
    n = 0
    for i in range(0, ROWS*COLS):
        plt.subplot(ROWS, COLS, n+1)
        plt.imshow(cvs[n], cmap=cmap2, norm=norm2)
        n += 1

    plt.show()


if __name__ == '__main__':
    cvs = []
    for i in range(0, ROWS*COLS):
        cv = op_element(ds0[i])
        print 'append sample:', i
        cvs.append(cv)

    show(cvs)
        


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

