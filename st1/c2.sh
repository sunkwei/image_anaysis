#!/bin/bash

# 并行计算, 共有501个样本

python c2.py 1000 120 &
python c2.py 1120 120 &
python c2.py 1240 120 &
python c2.py 1360 120 &
python c2.py 1480 21

