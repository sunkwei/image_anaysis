#!/usr/bin/python
# coding: utf-8
#
# @file: show.py
# @date: 2015-01-30
# @brief:
# @detail:
#
#################################################################

import cv2, time

FNAME = 'video/s.mp4'

cap = cv2.VideoCapture(FNAME)

cv2.namedWindow('origin')

while True:
    f, img = cap.read()
    cv2.imshow('origin', img)
    cv2.waitKey(30)





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

