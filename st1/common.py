#!/usr/bin/python
# coding: utf-8
#
# @file: common.py
# @date: 2015-01-27
# @brief:
# @detail:
#
#################################################################

from cv2 import *
import numpy as np

def load_from_yaml(fname):
    ''' 从 fname 中加载光流描述文件 '''
    e = cv.Load(fname)
    return np.asarray(e) # 每个元素为 [dx, dy]，为光流矢量的x,y 分量


def load_all(n):
    ds = []
    for i in range(0, n):
        e = load_from_yaml('data/%d.yaml' % i)
        ds.append(e)

    print 'load %d samples' % len(ds)

    return ds

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

