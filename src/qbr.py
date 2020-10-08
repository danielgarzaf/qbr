#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : qbr.py
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last Modified : Sun, 31 Jan 2016


from sys import exit as Die
try:
    import sys
    import kociemba
    import argparse

    from combiner import combine
    from video import webcam
    from normalizer import normalize
except ImportError as err:
    Die(err)


class Qbr:

    def __init__(self, normalize, language, definer, custom_colors, scaler, delay):
        self.humanize = normalize
        self.language = (language[0]) if isinstance(language, list) else language
        self.definer = definer
        self.custom_colors = custom_colors
        self.scaler = int(scaler)
        self.delay = int(delay)

    def run(self):
        state = webcam.scan(self.definer, self.custom_colors, self.scaler, self.delay)
        if not state:
            print('\033[0;33m[QBR SCAN ERROR] Oops, you did not scan in all 6 sides.')
            print('Please try again.\033[0m')
            Die(1)

        unsolvedState = combine.sides(state)
        try:
            algorithm     = kociemba.solve(unsolvedState)
            length        = len(algorithm.split(' '))
        except Exception as err:
            print('\033[0;33m[QBR SOLVE ERROR] Ops, you did not scan in all 6 sides correctly.')
            print('Please try again.\033[0m')
            Die(1)

        print('-- SOLUTION --')
        print('Starting position:\n    front: green\n    top: white\n')
        print(algorithm, '({0} moves)'.format(length), '\n')

        if self.humanize:
            manual = normalize.algorithm(algorithm, self.language)
            for index, text in enumerate(manual):
                print('{}. {}'.format(index+1, text))
        Die(0)

if __name__ == '__main__':
    # define argument parser.
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--normalize', default=False, action='store_true',
            help='Shows the solution normalized. For example "R2" would be: \
                    "Turn the right side 180 degrees".')
    parser.add_argument('-l', '--language', nargs=1, default='en',
            help='You can pass in a single \
                    argument which will be the language for the normalization output. \
                    Default is "en".')
    parser.add_argument('-d', '--define', action='store_true', default=False,
            help='Run the color definer. Uses custom colors after scan.')
    parser.add_argument('-c', '--custom', action='store_true', default=False,
            help="Use custom colors.")
    parser.add_argument('-s', '--scaler', default = 0, 
            help="Values from 0 to 255 that determine how much the image \
                darkens. Defaults at 0")
    parser.add_argument('-D', '--delay', default=0,
            help='Determines how many seconds of delay there is between \
                each frame. Defaults at 0')
    args = parser.parse_args()

    # run Qbr with its arguments.
    Qbr(
        args.normalize,
        args.language,
        args.define,
        args.custom,
        args.scaler,
        args.delay
    ).run()
