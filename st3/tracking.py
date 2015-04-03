#!/usr/bin/python
# coding: utf-8
#
# @file: tracking.py
# @date: 2015-04-03
# @brief:
# @detail:
#
#################################################################


from oflk import OFTracking
import math
import cv2 as cv


class TrackingRegion:
    ''' 正在跟踪的区域 '''

    def __init__(self, img, bounding_rect):
        self.__first_rect = bounding_rect
        self.__last_rect = bounding_rect
        self.__updated = False
        self.__updated_cnt = 1  # 连续cnt帧没有更新，则认为失败


    def update_same(self, img, bounding_rect):
        ''' 如果面积比较接近，并且距离比较接近，就认为是相同, 并更新 last_rect '''
        if self.__area_like(bounding_rect) and self.__nearby(bounding_rect):
            self.__last_rect = bounding_rect
            self.__updated = True
            self.__updated_cnt = 1
            return True
        else:
            self.__updated_cnt -= 1
            if self.__updated_cnt <= 0:
                self.__updated = False
            return False


    def rect(self):
        return self.__last_rect


    def updated(self):
        return self.__updated


    def __area_like(self, r):
        ''' 如果两个矩形的差小于矩形的 0.1，则认为面积接近 '''
        THRESH = 0.3
        a0 = self.__last_rect[2] * self.__last_rect[3]
        a1 = r[2] * r[3]
        return math.fabs(a0 - a1) < a0 * THRESH


    def __nearby(self, r):
        ''' 如果两个矩形的偏移都小于矩形长宽的 .4，则认为靠近 '''
        THRESH = 0.5
        dx = ((r[0]+r[2]) - (self.__last_rect[0]+self.__last_rect[2])) / 2
        dy = ((r[1]+r[3]) - (self.__last_rect[1]+self.__last_rect[3])) / 2
        return dx < r[2] * THRESH and dy < r[3] * THRESH



class Tracking:
    ''' 保存所有跟踪区，仅仅考虑大小合适，纵横比差不多的 '''
    def __init__(self):
        self.__regions = []


    def update(self, frame, bounding_rects):
        new = []

        THRESH_AREA = 5000

        for r in bounding_rects:
            # 如果面积小于XX, 则忽略
            if r[2]*r[3] < THRESH_AREA:
                continue

            # 如果太宽，则认为无效
            if r[2] > r[3] * 1.5:
                continue

            found = False
            for region in self.__regions:
                if region.update_same(frame, r):
                    found = True
                    break
            if not found:
                region = TrackingRegion(frame, r)
                new.append(region)

        # 删除没有更新的 region
        for r in self.__regions:
            if not r.updated():
                self.__regions.remove(r)

        for r in new:
            self.__regions.append(r)

        return self.__regions # 返回当前区域



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

