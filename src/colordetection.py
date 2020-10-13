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

    def get_color_name(self, hsv):
        """ Get the name of the color based on the hue.

        :returns: string
        """
        colors_hsv = {}
        with open('colors.json', 'r') as json_file:
            colors_hsv = json.load(json_file)
        (h,s,v) = hsv
        colors = list(colors_hsv.keys())

        for color in colors:
            hsv_bounds = colors_hsv[color]
            # print(hsv_bounds)
            # avg_colors_hsv = self.bounds_to_avg(hsv_bounds)
            lowH = hsv_bounds[0][0]
            highH = hsv_bounds[0][1]
            lowS = hsv_bounds[1][0]
            highS = hsv_bounds[1][1]
            lowV = hsv_bounds[2][0]
            highV = hsv_bounds[2][1]
            # if color == 'red' or color == 'orange':
            #     if (h < lowH or h > highH) and s in range(lowS, highS) and v in range(lowV, highV):
            #         return color
            if h in range(lowH, highH) and s in range(lowS, highS) and v in range(lowV, highV):
                return color
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
    
    def median_hsv(self, roi):
        """ Average the HSV colors in a region of interest.

        :param roi: the image array
        :returns: tuple
        """
        h   = []
        s   = []
        v   = []
        num = 0
        for y in range(len(roi)):
            if y % 10 == 0:
                for x in range(len(roi[y])):
                    if x % 10 == 0:
                        chunk = roi[y][x]
                        num += 1
                        h.append(chunk[0])
                        s.append(chunk[1])
                        v.append(chunk[2])
        
        return (int(np.median(h)), int(np.median(s)), int(np.median(v)))

    def bounds_to_avg(self, hsv_bounds):
        lowH = hsv_bounds[0][0]
        highH = hsv_bounds[0][1]
        lowS = hsv_bounds[1][0]
        highS = hsv_bounds[1][1]
        lowV = hsv_bounds[2][0]
        highV = hsv_bounds[2][1]
        avg_colors_hsv = self.colors_hsv
        for color in avg_colors_hsv:
            avg_colors_hsv[color] = [int((highH-lowH)/2), int((highS-lowS)/2), int((highV-lowV)/2)]
        return avg_colors_hsv

ColorDetector = ColorDetection()