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
except ImportError as err:
    Die(err)

class ColorDetection:

    def get_color_name(self, hsv, colorFlag):
        """ Get the name of the color based on the hue.

        :returns: string
        """
        (h,s,v) = hsv

        if colorFlag:
            print("custom colors loaded")
            custom_colors = {}
            with open("colors.json", "r") as json_file:
                custom_colors = json.load(json_file)
                json_file.close()
            red_hsv = custom_colors["RED"]
            orange_hsv = custom_colors["ORANGE"]
            white_hsv = custom_colors["WHITE"]
            yellow_hsv = custom_colors["YELLOW"]
            green_hsv = custom_colors["GREEN"]
            blue_hsv = custom_colors["BLUE"]
            if h - 10 < red_hsv[0] and red_hsv[0] < h + 10:
                return 'red'
            elif h - 10 < orange_hsv[0] and orange_hsv[0] < h + 10:
                return 'orange'
            elif h - 10 < white_hsv[0] and white_hsv[0] < h + 10:
                return 'white'
            elif h - 10 < yellow_hsv[0] and yellow_hsv[0] < h + 10:
                return 'yellow'
            elif h - 10 < green_hsv[0] and green_hsv[0] < h + 10:
                return 'green'
            elif h - 10 < blue_hsv[0] and blue_hsv[0] < h + 10:
                return 'blue'
            else:
                return 'white'
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
