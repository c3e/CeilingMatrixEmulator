#!/usr/bin/env python3
#
# emulator for led ceiling
#
# (c) 2018 Chaospott Essen


import colors
import pygame

from threading import Thread


class MatrixThread(Thread):
    """
    Define a class derivated from Thread, that
    holds the UI.
    """

    def __init__(
            self, 
            windowWidth,
            windowHeight,
            pixel_width,
            pixel_margin,
            chunk_width, 
            chunk_height,
            chunk_margin,
            grid_width,
            grid_height
            ):
        """
        Override the default constructor of the MatrixThread class.
        """
        # call the constructor of the parent class
        Thread.__init__(self)

        # initialize pygame
        pygame.init()

        # set the window's title
        pygame.display.set_caption("Pixellamp - Matrix Emulator")

        # display the mouse cursor
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)

        # get the screen from pygame
        self.__screen = pygame.display.set_mode((windowWidth, windowHeight))

        # set constructor parameters to class parameters
        self.__window_width = windowWidth
        self.__window_height = windowHeight
        self.__pixel_width = pixel_width
        self.__pixel_margin = pixel_margin
        self.__chunk_width = chunk_width
        self.__chunk_height = chunk_height
        self.__chunk_margin = chunk_margin
        self.__grid_width = grid_width
        self.__grid_height = grid_height

        # initialize the screen with black color pixels
        self.__screen.fill(colors.BLACK)

    def draw_pixmap(self, pixmap):
        """
        Draws the given pixmap into simulated pixels
        of the rendered window.

        :param pixmap: Array of chunks with pixels als RGB tupel.
        """
        # initialize the counter
        counter = 0

        # iterate through vertical chunks
        for chunk_y in range(self.__grid_height):
            # iterate through horizontal chunks
            for chunk_x in range(self.__grid_width):
                # calculate the general chunk-index from vertical and horizontal
                # chunk-index
                chunk = chunk_x + (self.__grid_width * chunk_y)
                
                # calculate the draw offset in window pixels for the
                # selected chunk
                chunk_x_offset = chunk_x * self.__chunk_width \
                        * (self.__pixel_width + self.__pixel_margin) \
                        + (chunk_x * self.__chunk_margin)
                chunk_y_offset = chunk_y * self.__chunk_height \
                        * (self.__pixel_width + self.__pixel_margin) \
                        + (chunk_y * self.__chunk_margin)

                # iterate through vertical simulated pixels
                for y in range(self.__chunk_height):
                    # iterate through horizontal simulated pixels
                    for x in range(self.__chunk_width):
                        # calculate the horizontal and vertical window pixel
                        # offset for every simulated pixel
                        pixel_x = x * (self.__pixel_width + self.__pixel_margin)
                        pixel_y = y * (self.__pixel_width + self.__pixel_margin)
                        
                        # calculate the offset of the color in our given
                        # pixmap
                        pixel_color_offset = x + (self.__chunk_width * y)

                        # get the color array [r, g, b] from the given pixmap
                        pixel_color = pixmap[chunk][pixel_color_offset]

                        # if there is an incomplete RGB value...
                        while len(pixel_color) != 3:
                            # ...set the missing channels to black
                            pixel_color.append(0)

                        # draw the simulated pixel to screen
                        pygame.draw.rect(
                                self.__screen,
                                pixel_color,
                                [
                                    chunk_x_offset + pixel_x,
                                    chunk_y_offset + pixel_y,
                                    self.__pixel_width,
                                    self.__pixel_width
                                ])
        # flip the display
        pygame.display.flip()
