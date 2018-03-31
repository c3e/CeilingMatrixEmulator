#!/usr/bin/env python3
#
# emulator for led ceiling
#
# (c) 2018 Chaospott Essen


import os
import pty

from threading import Thread, Event


class SerialThread(Thread):
    """
    Define a class derivated from Thread, that
    handles serial communication.

    """

    def __init__(
            self,
            matrix,
            chunk_width,
            chunk_height,
            grid_width,
            grid_height
            ):
        """
        Override the default constructor of the SerialThread class.
        """
        # call the constructor of the parent class
        Thread.__init__(self)

        # set a stop event for the main loop
        self.stop_event = Event()

        # create and open a serial device
        self.__master, self.__slave = pty.openpty()

        # get the ttyname
        self.__slave_name = os.ttyname(self.__slave)

        # set constructor parameters to class parameters
        self.__matrix = matrix
        self.__chunk_width = chunk_width
        self.__chunk_height = chunk_height
        self.__grid_width = grid_width
        self.__grid_height = grid_height

    def get_serial_port(self):
        """
        Getter for the serial port name.
        """
        return self.__slave_name

    def run(self):
        """
        Mainloop of the thread.
        """
        # print the created port
        print("==> serial port: {}".format(self.__slave_name))

        # create /dev/ttyUSB99 from /dev/pts/X
        try:
            os.symlink(self.__slave_name, '/dev/ttyUSB99')
        except Exception as e:
            # of the symlink exists, remove and recreate it
            os.remove('/dev/ttyUSB99')
            os.symlink(self.__slave_name, '/dev/ttyUSB99')

        # print stats about the symlink
        print('==> Created symlink {} -> /dev/ttyUSB99'.format(self.__slave_name))

        # start the mainloop
        while not self.stop_event.is_set():
            # read one byte from the master file descriptor
            serial_buffer = os.read(self.__master, 1)

            # if we got a 1, the buffer will be send through the serial
            # port and we can receive it
            if ord(serial_buffer) == 1:
                # initialize the pixel map
                pixmap = []

                # initialize the chunk counter
                chunk_counter = -1

                # iterate through the chunks
                for i in range(self.__grid_width * self.__grid_height):
                    # read all color values of the chunk's pixels
                    serial_buffer = os.read(
                            self.__master,
                            self.__chunk_width * self.__chunk_height * 3
                    )

                    # initialize the colorvalue counter
                    counter = 0

                    # initialize the simulated pixel counter
                    pixel_counter = -1

                    # iterate through every byte of the received data
                    # as integer in Python 3 and Hex-String in Python 2
                    for value in serial_buffer:
                        # if we completed a chunk...
                        if counter % (self.__chunk_height * self.__chunk_width * 3) == 0:
                            # ..., increase the chunk index...
                            chunk_counter += 1

                            # ...and append an empty array for the pixels
                            pixmap.append([])

                        # if we saved r,g and b values for one simulated
                        # pixel...
                        if counter % 3 == 0:
                            # ..., increase the counter...
                            pixel_counter += 1

                            # ..., and append an empty array for the next
                            # pixel's r,g and b value
                            pixmap[chunk_counter].append([])

                        # check if we use Python 3, which produces ints
                        if type(value) == int:
                            # append the color value as int
                            pixmap[chunk_counter][pixel_counter].append(value)
                        else:
                            # else we use Python 2 and need to convert
                            # the color value to int from a string like '\xff'
                            pixmap[chunk_counter][pixel_counter].append(ord(value))

                        # increase the colorvalue counter
                        counter += 1

                # after saving the complete chunks into the pixmap,
                # draw it in the ui thread
                self.__matrix.draw_pixmap(pixmap)
