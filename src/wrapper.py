#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename        : wrapper.py
# Original Author : Daniel G
# Created         : Mon, 19 Oct 2020
# Last Modified   : Tue, 20 Oct 2020

import numpy as np


class Wrapper:
    def __init__(self):
        self.values = {
            "U": "0",
            "B": "1",
            "R": "2",
            "F": "3",
            "L": "4",
            "D": "5",
        }

    def wrap_results(self, scramble):
        scramble_nums = ""
        for idx, letter in enumerate(scramble):
            scramble_nums += self.values[letter]
        scramble = scramble_nums

        # parse each face values
        scramble_parsed = self.parse_nums(scramble)

        # populate matrix
        n = len(scramble_parsed[0])
        rows = n // 3
        cols = n // rows
        scramble_matrix = np.zeros((len(scramble_parsed), rows, cols))
        for index, nums in enumerate(scramble_parsed):
            for i in range(rows):
                for j in range(cols):
                    scramble_matrix[index][i][j] = nums[i * cols + j]

        # rotate matrixes accordingly
        for i in range(len(scramble_matrix)):
            block = scramble_matrix[i]
            block[:] = np.rot90(block, 1).copy()
            if scramble_matrix[i][1][1] == 5:
                block[:] = np.rot90(block, 1).copy()
                block[:] = np.rot90(block, 1).copy()
            elif scramble_matrix[i][1][1] == 0:
                pass
            else:
                block[:] = np.rot90(block, 1).copy()

        # prepare the result in string, then split it
        # and swap face values accordingly to be in the order
        # the manual demands:
        # (["White", "Blue", "Red", "Green", "Orange", "Yellow"])
        res = ""
        for i in range(len(scramble_matrix)):
            for j in range(len(scramble_matrix[i])):
                for k in range(len(scramble_matrix[i][j])):
                    res += str(int(scramble_matrix[i][j][k]))
        res = self.parse_nums(res)
        res = [
            res[0],
            res[-1],
            res[1],
            res[2],
            res[-2],
            res[-3],
        ]

        # remove the center color of each face value
        for i, nums in enumerate(res):
            res[i] = nums[:4] + nums[5:]

        # arrange values accordingly to fit format in manual
        output = ""
        for nums in res:
            output += nums[:3] + nums[4] + nums[-1] + nums[-2] + nums[-3] + nums[3]

        return output

    # parse each face values
    def parse_nums(self, nums):
        scramble_parsed = []
        for i, num in enumerate(nums):
            if i % 9 == 0 and i != 0:
                scramble_parsed.append(nums[i - 9 : i])
            elif i == len(nums) - 1:
                scramble_parsed.append(nums[i - 8 : i + 1])
        return scramble_parsed

