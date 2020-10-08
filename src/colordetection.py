#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : colordetection.py
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last Modified : Sun, 31 Jan 2016


from sys import exit as Die
try:
    import sys
    import json
    import numpy as np
    from scipy.spatial import distance
except ImportError as err:
    Die(err)

class ColorDetection:

    def get_color_name(self, hsv, definer_flag, custom_flag):
        """ Get the name of the color based on the hue.

        :returns: string
        """
        (h,s,v) = hsv
        if definer_flag or custom_flag:
            with open("colors.json", "r") as json_file:
                custom_colors = json.load(json_file)
                json_file.close()
            euclidean_dst = {}
            point_a = (h,s,v)
            for key, value in custom_colors.items():
                point_b = (value[0], value[1], value[2])
                dst = distance.euclidean(point_a, point_b)
                euclidean_dst[key] = dst
            color = min(euclidean_dst, key=euclidean_dst.get).lower()
            return color

        else:
            if h < 15 and v < 100:
                return 'red'
            elif h <= 10 and v > 100:
                return 'orange'
            elif h <= 30 and s <= 100:
                return 'white'
            elif h <= 40:
                return 'yellow'
            elif h <= 85:
                return 'green'
            elif h <= 130:
                return 'blue'
            return 'white'

    def name_to_rgb(self, name):
        """
        Get the main RGB color for a name.

        :param name: the color name that is requested
        :returns: tuple
        """
        color = {
            'red'    : (0,0,255),
            'orange' : (0,165,255),
            'blue'   : (255,0,0),
            'green'  : (0,255,0),
            'white'  : (255,255,255),
            'yellow' : (0,255,255)
        }
        return color[name]

    def average_hsv(self, roi):
        """ Average the HSV colors in a region of interest.

        :param roi: the image array
        :returns: tuple
        """
        h   = 0
        s   = 0
        v   = 0
        num = 0
        for y in range(len(roi)):
            if y % 10 == 0:
                for x in range(len(roi[y])):
                    if x % 10 == 0:
                        chunk = roi[y][x]
                        num += 1
                        h += chunk[0]
                        s += chunk[1]
                        v += chunk[2]
        h /= num
        s /= num
        v /= num
        return (int(h), int(s), int(v))

ColorDetector = ColorDetection()
