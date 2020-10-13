#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : video.py
# Author        : Kim K
# Created       : Fri, 29 Jan 2016
# Last Modified : Sun, 31 Jan 2016


from sys import exit as Die
try:
    import os
    import sys
    import cv2
    import json
    import numpy as np
    from colordetection import ColorDetector
    from filters import Filter
    from time import sleep

except ImportError as err:
    Die(err)


class Webcam:
    def __init__(self):
        self.cam              = cv2.VideoCapture(0)
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')
        self.filter = Filter()

    def get_sticker_coordinates(self, name):
        """
        Every array has 2 values: x and y.
        Grouped per 3 since on the cam will be
        3 rows of 3 stickers.

        :param name: the requested color type
        :returns: list
        """
        stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ],
        }
        return stickers[name]

    def draw_main_stickers(self, frame):
        """Draws the 9 stickers in the frame."""
        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)

    def draw_current_stickers(self, frame, state):
        """Draws the 9 current stickers in the frame."""
        for index,(x,y) in enumerate(self.current_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def draw_preview_stickers(self, frame, state):
        """Draws the 9 preview stickers in the frame."""
        for index,(x,y) in enumerate(self.preview_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def color_to_notation(self, color):
        """
        Return the notation from a specific color.
        We want a user to have green in front, white on top,
        which is the usual.

        :param color: the requested color
        """
        notation = {
            'green'  : 'F',
            'white'  : 'U',
            'blue'   : 'B',
            'red'    : 'R',
            'orange' : 'L',
            'yellow' : 'D'
        }
        return notation[color]

    def scan(self):
        """
        Open up the webcam and scans the 9 regions in the center
        and show a preview in the left upper corner.

        After hitting the space bar to confirm, the block below the
        current stickers shows the current state that you have.
        This is show every user can see what the computer toke as input.

        :returns: dictionary
        """

        sides   = {}
        preview = ['white','white','white',
                   'white','white','white',
                   'white','white','white']
        state   = [0,0,0,
                   0,0,0,
                   0,0,0]

        while True:
            _, frame = self.cam.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            key = cv2.waitKey(10) & 0xff
            B,G,R = cv2.split(frame)
            # frame = self.filter.equalize_filter(frame, (B,G,R))
            # frame = self.filter.gamma_filter(frame)
        
            # init certain stickers.
            self.draw_main_stickers(frame)
            self.draw_preview_stickers(frame, preview)

            for index,(x,y) in enumerate(self.stickers):
                roi          = hsv[y:y+32, x:x+32]
                avg_hsv      = ColorDetector.median_hsv(roi)
                color_name   = ColorDetector.get_color_name(avg_hsv)
                state[index] = color_name

                # update when space bar is pressed.
                if key == 32:
                    preview = list(state)
                    self.draw_preview_stickers(frame, state)
                    face = self.color_to_notation(state[4])
                    notation = [self.color_to_notation(color) for color in state]
                    sides[face] = notation

            # show the new stickers
            self.draw_current_stickers(frame, state)

            # append amount of scanned sides
            text = 'scanned sides: {}/6'.format(len(sides))
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

            # quit on escape.
            if key == 27:
                break
            
            # start calibration if 'c' is pressed
            if key == 99:
                Calibrator().calibrate()
                self.cam = cv2.VideoCapture(0)
                _, frame = self.cam.read()

            cv2.imshow("default", frame)

        self.cam.release()
        cv2.destroyAllWindows()
        return sides if len(sides) == 6 else False


class Calibrator(Webcam):
    def __init__(self):
        super().__init__()
        self.check_colors_file()
        self.colors_hsv = {}
        with open("colors.json", "r") as json_file:
            self.colors_hsv = json.load(json_file)
        self.colors = list(self.colors_hsv.keys())
        self.color_idx = 0
        self.color = self.colors[self.color_idx]

    def calibrate(self):
        # create trackbars for hsv bounds
        color = self.colors[self.color_idx]
        cv2.createTrackbar('lowH', 'default', self.colors_hsv[self.color][0][0], 
            180, self.callback)
        cv2.createTrackbar('highH', 'default', self.colors_hsv[self.color][0][1], 
            180, self.callback)
        cv2.createTrackbar('lowS', 'default', self.colors_hsv[self.color][1][0], 
            255, self.callback)
        cv2.createTrackbar('highS', 'default', self.colors_hsv[self.color][1][1], 
            255, self.callback)
        cv2.createTrackbar('lowV', 'default', self.colors_hsv[self.color][2][0],
            255, self.callback)
        cv2.createTrackbar('highV', 'default', self.colors_hsv[self.color][2][1], 
            255, self.callback)


        while True:
            # read frame, key press, and draw stickers
            _, frame = self.cam.read()
            k = cv2.waitKey(1) & 0xFF

            # extract hsv bounds from trackbars
            hl = cv2.getTrackbarPos('lowH', 'default')
            hu = cv2.getTrackbarPos('highH','default')
            sl = cv2.getTrackbarPos('lowS', 'default')
            su = cv2.getTrackbarPos('highS','default')
            vl = cv2.getTrackbarPos('lowV', 'default')
            vu = cv2.getTrackbarPos('highV','default')
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # press spacebar: move on to next color config
            if k == 32:
                self.color = self.colors[self.color_idx]
                self.colors_hsv[self.color] = ((hl, hu), (sl, su), (vl, vu))
                self.color_idx += 1

                if self.color_idx < len(self.colors):
                    self.color = self.colors[self.color_idx]
                    self.set_trackbar_positions()
            
            # press backspace: go back to previous hsv config.
            if k == 8:
                self.color_idx -= 1
                if self.color_idx < 0:
                    cv2.destroyAllWindows()
                    break
                self.color = self.colors[self.color_idx]
                self.set_trackbar_positions()
                
            # press esc OR last color calibrated: finish calibration process
            if k == 27 or self.color_idx == len(self.colors):
                cv2.destroyAllWindows()
                break

            # # mask the frame depending on the color
            # if self.colors[self.color_idx] == 'red' or self.colors[self.color_idx] == 'orange':
            #     lower_hsv = np.array([0,sl,vl])
            #     upper_hsv = np.array([hl,su,vu])
            #     mask1 = cv2.inRange(hsv, lower_hsv, upper_hsv)
            #     lower_hsv = np.array([hu,sl,vl])
            #     upper_hsv = np.array([179, su, vu])
            #     mask2 = cv2.inRange(hsv, lower_hsv, upper_hsv)
            #     mask = cv2.bitwise_or(mask1, mask2)
            #     frame = cv2.bitwise_and(frame, frame, mask=mask)
            #     lower_hsv = np.array([hl,sl,vl])
            #     upper_hsv = np.array([])
            lower_hsv = np.array([hl,sl,vl])
            upper_hsv = np.array([hu,su,vu])
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            frame = cv2.bitwise_and(frame, frame, mask=mask)
            
            # draw text and stickers into frame
            text = 'Calibrating {} ({}/{})'.format(self.colors[self.color_idx].upper(), 
                                        self.color_idx + 1, len(self.colors))
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 
                1, cv2.LINE_AA)
            self.draw_main_stickers(frame)

            cv2.imshow('default', frame)
        
        with open('colors.json', 'w') as json_file:
            json.dump(self.colors_hsv, json_file)
        
        # self.cam.release()

    def check_colors_file(self):
        if not os.path.isfile('./colors.json'):
            raise FileNotFoundError("The file \"colors.json\" wasn't found.\n \
                Create a file named \"colors.json\" and copy and paste this into it:\n \
                {\n \
                \"green\": [[0,179],[0,254],[0,254]],\n \
                \"red\": [[0,179],[0,254],[0,254]],\n \
                \"blue\": [[0,179],[0,254],[0,254]],\n \
                \"orange\": [[0,179],[0,254],[0,254]],\n \
                \"white\": [[0,179],[0,254],[0,254]],\n \
                \"yellow\": [[0,179],[0,254],[0,254]]\n \
                }")
    
    def set_trackbar_positions(self):
        cv2.setTrackbarPos('lowH', 'default', self.colors_hsv[self.color][0][0])
        cv2.setTrackbarPos('highH', 'default', self.colors_hsv[self.color][0][1])
        cv2.setTrackbarPos('lowS', 'default', self.colors_hsv[self.color][1][0])
        cv2.setTrackbarPos('highS', 'default', self.colors_hsv[self.color][1][1])
        cv2.setTrackbarPos('lowV', 'default', self.colors_hsv[self.color][2][0])
        cv2.setTrackbarPos('highV', 'default', self.colors_hsv[self.color][2][1])


    def callback(self, x):
        pass

