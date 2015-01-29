#!/bin/bash

mkdir -p saved

# 并行计算, 共有501个样本

python c2.py 1000 30 &
python c2.py 1030 30 &

python c2.py 1060 30 &
python c2.py 1090 30 

python c2.py 1120 30 &
python c2.py 1150 30 &

python c2.py 1180 30 &
python c2.py 1210 30 

python c2.py 1240 30 &
python c2.py 1270 30 &

python c2.py 1300 30 &
python c2.py 1330 30 

python c2.py 1360 30 &
python c2.py 1390 30 &

python c2.py 1420 30 &
python c2.py 1450 30 

python c2.py 1480 21

