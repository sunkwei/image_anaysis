#!/usr/bin/python
# coding: utf-8
#
# @file: len_contour.py
# @date: 2015-01-28
# @brief: 加载 tmp/npN 画等高线
# @detail:
#
#################################################################

import sys
import numpy as np
import matplotlib.pyplot as plt

n = 0

if len(sys.argv) > 0:
    n  = int(sys.argv[1])

d = np.load('tmp/np%d.npy' % n)

plt.figure(1)

plt.contour(d)
plt.show()



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

