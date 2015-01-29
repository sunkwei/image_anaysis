#!/usr/bin/python
# coding: utf-8
#
# @file: py_chart2.py
# @date: 2015-01-26
# @brief:
# @detail:
#
#################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math, cv2.cv as cv
from matplotlib import colors
import sys

ROWS = 3 # 显示三帧
COLS = 3 # 每帧显示光流大小,原始图像,光流方向
THRESHOLD = 5 # 如果长度小于此,则大小置为0

def op_mod(e):
    ''' e 为 [dx, dy] 实例，计算每个点的 sqrt(dx*dx + dy*dy)
        返回 row * col 的矩阵，每个元素为 mod
    '''
    r,c = e.shape[0], e.shape[1]
    le = e.reshape(e.size) # 变为一行
    x = le[::2]            # 提取 x
    y = le[1::2]           # 提取 y

    ms = np.sqrt(x*x + y*y) # 

    for i in range(0, ms.size):
        if ms[i] < THRESHOLD:
            ms[i] = 0.0

    return ms.reshape((r,c)) # 还原 e 的模样，但是每个元素为向量长度

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

    angv = np.arctan2(yv, xv) # 计算每个点的偏角, 范围 [-pi .. pi]
    colv = np.zeros(angv.size)

    LEFT = 4 # green
    RIGHT = 3 # yellow
    UP = 2 # red
    DOWN = 1 # blue

    dirs = [ DOWN, LEFT, UP, RIGHT  ]

    for i in range(0, angv.size):
        if lv[i] < 0.000001: # 0
            continue

        ang = angv[i]
        ang += math.pi # 取正值
        ang += math.pi/4 # 旋转
        ang %= math.pi*2

        index = int(ang / (math.pi/2))

        colv[i] = dirs[index]

    return colv.reshape(r, c)


def show(ds, imgs, dds, fs):
    ''' 显示到图表中'''
    fig = plt.figure()
    n = 0
    for i in range(0, ROWS):
        plt.subplot(ROWS, COLS, n*COLS+1) # 选择子图
        plt.imshow(ds[n])        # 画图,plt自动使用cool-->warm的颜色显示值大小 
        n += 1
            
    n = 0
    for r in range(0, ROWS):
        plt.subplot(ROWS, COLS, n*COLS+2)
        img = mpimg.imread(imgs[n])
        plt.imshow(img)
        n += 1

    cmap2 = colors.ListedColormap(['black', 'blue', 'red', 'yellow', 'green']) # 向上 red, 向下 blue
    bounds2 = [0, 0.5, 1.5, 2.5, 3.5, 5]
    norm2 = colors.BoundaryNorm(bounds2, cmap2.N)
    n = 0
    for r in range(0, ROWS):
        plt.subplot(ROWS, COLS, n*COLS+3)
        plt.imshow(dds[n], cmap=cmap2, norm=norm2)
        n += 1

    fname = 'saved/f'
    for i in fs:
        fname += '-'
        fname += str(i)
    fname += '.jpg'
    fig.savefig(fname) # 保存到文件, 更方便比较

    #plt.show()


def load_all(n, base=1440):
    ds = []
    imgs = []
    for i in range(base, n+base):
        p = np.load('origin_data/%d.npy' % i)
        ds.append(p)

        imgs.append('origin_data/%d.jpg' % i)
    return ds, imgs


def do_once(base):
    ds = []
    dds = []
    
    fs = []
    ds0, imgs0 = load_all(ROWS, base)
    n = 0
    for d in ds0:
        print 'op_mod for ', base + n
        fs.append(base + n)
        n += 1

        m = op_mod(d)
        ds.append(m)

        dd = op_element(d)
        dds.append(dd)

    show(ds, imgs0, dds, fs)


if __name__ == '__main__':
    ''' 保存到 saved/ 目录中,方便查看 '''
    n = 1442
    while n < 1498:
        do_once(n)
        n += 3


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

