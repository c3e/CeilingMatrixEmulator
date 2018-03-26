#!/usr/bin/env python3
#
# emulator for led ceiling
#
# (c) 2018 Chaospott Essen


import os
import pygame
import signal
import time
import sys

from MatrixThread import MatrixThread
from SerialThread import SerialThread


#----------------#
# Configguration #
#----------------#
PIXEL_WIDTH = 8
PIXEL_MARGIN = 2

CHUNK_WIDTH = 8
CHUNK_HEIGHT = 8
CHUNK_MARGIN = 2

GRID_WIDTH = 10
GRID_HEIGHT = 5


def sighandler(signum, frame):
    """
    Callback for the signal handler.

    It removes the symlink for the
    pts to /dev/ttyUSB99.
    """
    # remove the symlink
    os.remove('/dev/ttyUSB99')

    # print the status
    print('==> Removed symlink')

    # exit gracefully
    sys.exit(0)


def main():
    """
    Main function and entrypoint of the script.
    """
    # calculate window width and window height from the configuration
    windowWidth = (((PIXEL_WIDTH + PIXEL_MARGIN) * CHUNK_WIDTH) + CHUNK_MARGIN) \
            * GRID_WIDTH
    windowHeight = (((PIXEL_WIDTH + PIXEL_MARGIN) * CHUNK_HEIGHT) + CHUNK_MARGIN) \
            * GRID_HEIGHT

    # register the callback to be called on SIGINT
    signal.signal(signal.SIGINT, sighandler)

    # initialize the ui thread with configured parameters
    matrix_thread = MatrixThread(
            windowWidth,
            windowHeight,
            PIXEL_WIDTH,
            PIXEL_MARGIN,
            CHUNK_WIDTH,
            CHUNK_HEIGHT,
            CHUNK_MARGIN,
            GRID_WIDTH,
            GRID_HEIGHT
    )

    # initialize the serial communicator
    serial_thread = SerialThread(
            matrix_thread,
            CHUNK_WIDTH,
            CHUNK_HEIGHT,
            GRID_WIDTH,
            GRID_HEIGHT
    )

    # run the serial thread to fetch data to draw
    serial_thread.run()

    # run while true with timeout of 60 seconds in order
    # to save cpu time, but not exit the script
    while True:
        time.sleep(60)


# call the main function if this script isn't
# loaded as module
if __name__ == '__main__':
    main()
