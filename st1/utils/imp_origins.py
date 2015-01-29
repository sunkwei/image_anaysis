#!/usr/bin/python
# coding: utf-8
#
# @file: imp_origins.py
# @date: 2015-01-29
# @brief: 将原始保存的 .yaml 转换为 .npy 只是为了降低磁盘占用 ...
# @detail:
#
#################################################################

import numpy as np
import cv2.cv as cv
import os, shutil

SRCPATH = os.getenv('HOME') + '/Desktop/bin'
DSTPATH = '../origin_data'
PICPATH = os.getenv('HOME') + '/Desktop/main'

for i in range(1000, 1502):
    sfname = SRCPATH + '/%d.yaml' % i
    dfname = DSTPATH + '/%d' % i
    pfname = DSTPATH + '/%d.jpg' % i
    qfname = PICPATH + '/%d.jpg' % i

    print '%s ==> %s ' % (sfname, dfname)
    print '%s --> %s ' % (qfname, pfname)

    f = cv.Load(sfname)
    d = np.asarray(f)
    
    np.save(dfname, d)

    shutil.copyfile(qfname, pfname)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

