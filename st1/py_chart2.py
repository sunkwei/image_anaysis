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
import math
from common import *

ROWS = 5
COLS = 5
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

def show(ds):
    ''' 显示到图表中'''
    fig = plt.figure(1)

    n = 1
    for r in range(0, ROWS):
        for c in range(0, COLS):
            plt.subplot(ROWS, COLS, n) # 选择子图
            plt.imshow(ds[n-1])        # 画图,plt自动使用cool-->warm的颜色显示值大小 
            print 'sample #%d drawed' % n
            n += 1
    plt.show()




if __name__ == '__main__':
    ds0 = load_all(ROWS * COLS)
    ds = []
    for d in ds0:
        ds.append(op_mod(d))
    show(ds)




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

