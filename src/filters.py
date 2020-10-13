#!/usr/bin/env python3
import cv2
import numpy as np

class Filter:
    def __init__(self, gamma=2):
        self.gamma = float(gamma)

    def equalize_filter(self, frame, BGR):
        B, G, R = BGR
        for i in range(3):
            frame = cv2.GaussianBlur(frame, (5,5), 0)
        output_B = cv2.equalizeHist(B)
        output_G = cv2.equalizeHist(G)
        output_R = cv2.equalizeHist(R)
        re = cv2.merge((output_B, output_G, output_R))
        return re

    def clahe_filter(self, frame, BGR):
        B, G, R = BGR
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        output_B = clahe.apply(B)
        output_G = clahe.apply(G)
        output_R = clahe.apply(R)
        return cv2.merge((output_B, output_G, output_R))

    def gamma_filter(self, frame):
        # for i in range(3):
        #     frame = cv2.GaussianBlur(frame, (5,5), 0)
        look_up_table = np.empty((1,256), np.uint8)
        for i in range(256):
            look_up_table[0, i] = np.clip(pow(i/255.0, float(self.gamma)) * 255.0, 0, 255)
        re = cv2.LUT(frame, look_up_table)
        return re

    def split_BGR(self, frame):
        B, G, R = cv2.split(frame)
        output_B = cv2.equalizeHist(B)
        output_G = cv2.equalizeHist(G)
        output_R = cv2.equalizeHist(R)
        return (output_B, output_G, output_R)