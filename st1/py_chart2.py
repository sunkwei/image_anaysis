#!/usr/bin/python
# coding: utf-8
#
# @file: py_chart2.py
# @date: 2015-01-26
# @brief:
# @detail:
#
#################################################################

from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import math


def op_mod(e):
    ''' e 为 [dx, dy] 实例，计算每个点的 sqrt(dx*dx + dy*dy)
        返回 row * col 的矩阵，每个元素为 mod
    '''
    r,c = e.shape[0], e.shape[1]
    le = e.reshape(e.size) # 变为一行
    x = le[::2]            # 提取 x
    y = le[1::2]           # 提取 y

    ms = np.sqrt(x*x + y*y) # 
    return ms.reshape((r,c)) # 还原 e 的模样，但是每个元素为向量长度


def load_from_yaml(fname):
    ''' 从 fname 中加载光流描述文件 '''
    e = cv.Load(fname)
    return np.asarray(e) # 每个元素为 [dx, dy]，为光流矢量的x,y 分量


def load_all():
    ds = []
    for i in range(0, 20):
        e = load_from_yaml('data/%d.yaml' % i)
        m = op_mod(e)
        ds.append(m)

    print 'load %d samples' % len(ds)

    return ds


def show(ds):
    ''' 显示到图表中'''
    fig = plt.figure(1)

    ROWS = 3
    COLS = 3

    n = 1
    for r in range(0, ROWS):
        for c in range(0, COLS):
            plt.subplot(ROWS, COLS, n) # 选择子图
            plt.imshow(ds[n-1])        # 画图,plt自动使用cool-->warm的颜色显示值大小 
            print 'sample #%d drawed' % n
            n += 1
    plt.show()




if __name__ == '__main__':
    data = load_all()
    show(data)




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

