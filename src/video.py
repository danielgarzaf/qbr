#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : video.py
# Author        : Kim K
# Created       : Fri, 29 Jan 2016
# Last Modified : Sun, 31 Jan 2016


from sys import exit as Die
try:
    import sys
    import cv2
    import json
    import numpy as np
    from time import sleep
    from colordetection import ColorDetector
except ImportError as err:
    Die(err)


class Webcam:

    def __init__(self):
        self.cam              = cv2.VideoCapture(0)
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')
        self.center_sticker = self.get_sticker_coordinates('center')

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
            'center' : [300,220]
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

    def draw_center_sticker(self, frame):
        (x, y) = self.center_sticker
        cv2.rectangle(frame, (x,y), (x+32, y+32), (255,255,255), 2)


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

    def scan(self, definer_flag=False, custom_flag=False, scaler=60, delay=0):
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

        # run definer and store colors in a json file
        if definer_flag:
            faces_avg_hsv = self.define_colors()
            faces_avg_hsv = self.order_custom_colors(faces_avg_hsv)
            with open("colors.json", "w") as json_file:
                json.dump(faces_avg_hsv, json_file)
                json_file.close()

        while True:
            _, frame = self.cam.read()
            intensity_matrix = np.ones(frame.shape, np.uint8) * scaler
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            key = cv2.waitKey(10) & 0xff
        
           # init certain stickers.
            self.draw_main_stickers(frame)
            self.draw_preview_stickers(frame, preview)

            for index,(x,y) in enumerate(self.stickers):
                roi          = hsv[y:y+32, x:x+32]
                avg_hsv      = ColorDetector.average_hsv(roi)
                color_name   = ColorDetector.get_color_name(avg_hsv, definer_flag, custom_flag)
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

            # show result
            frame = cv2.subtract(frame, intensity_matrix)
            cv2.imshow("default", frame)
            sleep(delay)

        self.cam.release()
        cv2.destroyAllWindows()
        return sides if len(sides) == 6 else False

    def define_colors(self):
        """
        Scan the center of each face to determine the HSV range of each color.
        Returns the average hsv scanned for each color.
        """

        preview = ['white','white','white',
                   'white','white','white',
                   'white','white','white']
        faces = ["GREEN", "RED", "BLUE",
                 "ORANGE", "YELLOW", "WHITE"]
        face_index = 0
        current_sticker = self.center_sticker
        print("Current Stickers:", current_sticker)
        faces_avg_hsv = {}

        while True:
            _, frame = self.cam.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            key = cv2.waitKey(10) & 0xff

            # init certain stickers.
            self.draw_center_sticker(frame)

            x,y = current_sticker
            roi = hsv[y:y+32, x:x+32]
            avg_hsv = ColorDetector.average_hsv(roi)
            text = "Scan {} face".format(faces[face_index])
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

            # update when space bar is pressed.
            if key == 32:
                face = faces[face_index]
                faces_avg_hsv[face] = avg_hsv
                face_index += 1

            # quit on escape.
            if key == 27:
                break

            # quit when all faces have been scanned
            elif face_index == 6:
                face_index = 0
                break

            # show result
            cv2.imshow("default", frame)

        return faces_avg_hsv

    def order_custom_colors(self, custom_colors):
        """
        Orders the dictionary containing the custom
        colors scanned in ascending order based on the
        `h` value.
        """
        return {k:v for k,v in sorted(list(custom_colors.items()), key=lambda item: item[1][0])}


webcam = Webcam()
