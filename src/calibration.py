#!/usr/bin/env python3

import numpy as np
import cv2
import json
import os


class Calibrator(Webcam):
    def __init__(self):
        self.check_colors_file()
        self.colors_hsv = {}
        with open("colors.json", "r") as json_file:
            self.colors_hsv = json.load(json_file)
        self.colors = list(self.colors_hsv.keys())
        self.colors_idx = 0
        self.color = self.colors[self.colors_idx]

    def calbrate(self):
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
            k = cv2.waitKey(0) & 0xFF
            self.draw_main_stickers(frame)

            # extract hsv bounds from trackbars
            lowH = cv2.getTrackbarPos('lowH', 'default')
            highH = cv2.getTrackbarPos('highH','default')
            lowS = cv2.getTrackbarPos('lowS', 'default')
            highS = cv2.getTrackbarPos('highS','default')
            lowV = cv2.getTrackbarPos('lowV', 'default')
            highV = cv2.getTrackbarPos('highV','default')
            low_hsv = np.array([lowH, lowS, lowV])
            high_hsv = np.array([highH, highS, highV])

            # apply mask
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, low_hsv, high_hsv)
            frame = cv2.bitwise_and(frame, frame, mask=mask)

            text = 'Calibrating {}'.format(self.faces[self.face_idx].upper(), 
                                        self.color_idx + 1, len(self.colors))
            cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 
                1, cv2.LINE_AA)

            # press spacebar: move on to next color config
            if k == 32:
                self.color = self.colors[self.color_idx]
                self.colors_hsv[self.color] = ((lowH, highH), (lowS, highS), (lowV, highV))
                self.color_idx += 1

                if self.color_idx < len(self.colors):
                    self.color = self.colors[color_idx]
                    self.set_trackbar_positions()
            
            # press esc OR last color calibrated: finish calibration process
            if k == 27 or self.color_idx == len(self.color):
                cv2.destroyAllWindows()
                self.color_idx = 0
                break
            
            # press backspace: go back to previous hsv config.
            if k == 8:
                self.color_idx -= 1
                if self.color_idx < 0:
                    cv2.destroyAllWindows()
                    self.color_idx = 0
                    break
                self.color = self.colors[self.color_idx]
                self.set_trackbar_positions()
    
            cv2.imshow('default', frame)
        
        with open('colors.json', 'w') as json_file:
            json.dump(colors_hsv, json_file)

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
        cv2.setTrackbarPos('lowH', 'img', self.colors_hsv[self.color][0][0])
        cv2.setTrackbarPos('highH', 'img', self.colors_hsv[self.color][0][1])
        cv2.setTrackbarPos('lowS', 'img', self.colors_hsv[self.color][1][0])
        cv2.setTrackbarPos('highS', 'img', self.colors_hsv[self.color][1][1])
        cv2.setTrackbarPos('lowV', 'img', self.colors_hsv[self.color][2][0])
        cv2.setTrackbarPos('highV', 'img', self.colors_hsv[self.color][2][1])


    def callback(self, x):
        pass
