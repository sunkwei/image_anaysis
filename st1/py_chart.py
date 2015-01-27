#!/usr/bin/python
# coding: utf-8
#
# @file: py_chart.py
# @date: 2015-01-21
# @brief: 利用 matplotlib 绘制学生探测的历史记录的三维图，便于观察数据的特性
# @detail:
#
#################################################################

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sys


def load_data(fname):
    ''' 从 fname 文件中加载数据，每行格式：
            frame_id  x  y
        frame_id 为帧序号
    
        返回 { "frame_begin": xxx, "frame_end": xxx, "data": xxx }
    '''
    ret = { "frame_begin": -1, "frame_end": -1, "x": [], "y": [] }

    f = open(fname, 'r')
    last = -1
    last_fid = -1
    last_x, last_y = -1, -1

    for line in f:
        if len(line) < 3:
            continue
        sfid, x, y = line.split(' ')
        fid = int(sfid)

        if ret['frame_begin'] == -1:
            ret['frame_begin'] = fid

        if last_fid < 0:
            pass
        else:
            delta = fid - last_fid
            for i in range(1, delta):
                ret['x'].append(last_x)
                ret['y'].append(last_y)

        last_fid = fid
        last_x = int(x)
        last_y = int(y)
            
        ret['x'].append(last_x)
        ret['y'].append(last_y)

        last = fid
    ret['frame_end'] = last
    f.close()

    if len(ret['x']) < 3 or len(ret['x']) != len(ret['y']):
        return None

    return ret;


def load_datas():
    ''' 加载数据文件 '''
    ds = {}
    for i in range(0, 131):
        fname = 'data/obj' + str(i)
        d = load_data(fname)
        if d:
            ds['obj' + str(i)] = d
    return ds


def get_duration(ds):
    ''' 得到数据集中，持续时间 '''
    t0, tn = 1000000, -1
    for i in ds:
        d = ds[i]
        if t0 > d['frame_begin']:
            t0 = d['frame_begin']
        if tn < d['frame_end']:
            tn = d['frame_end']
    return t0, tn


def show(ds):
    ''' 根据数据集，构造图表数据 '''
    t0, tn = get_duration(ds)
    x0, xn = 0, 480 # X 轴大小
    y0, yn = 0, 270 # y 轴大小

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection = '3d')

    ax.set_xlabel('frames')
    ax.set_ylabel('X')
    ax.set_zlabel('Y')

    ax.set_xlim([t0, tn])
    ax.set_ylim([x0, xn])
    ax.set_zlim([y0, yn])
    
    for i in ds:
        d = ds[i]

        print 'draw:', i

        # 在整个 t 空间,必须都有数值 ?:
        x = d['x']
        y = d['y']
        t = [ t for t in range(d['frame_begin'], d['frame_end'] + 1)] #

#ax.plot(xs = t, ys = x, zs = y, label=i)
        ax.scatter(xs = t, ys = x, zs = y)

    plt.legend()
    plt.show()
        


if __name__ == '__main__':
    ds = load_datas()
    show(ds)

    sys.exit()
    


mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection = '3d')

theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)

z = np.linspace(-2, -2, 100)

r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.show()




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

