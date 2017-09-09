import pygame
import os
import pty
import serial
from random import randint

pixelWidth = 8
pixelHeight = 8
pixelMargin = 2
panelMargin = 5

panelPixelX = 8
panelPixelY = 8

gridPanelX = 10
gridPanelY = 5


class pixel:
    def __init__(self):
        self.color = [255, 255, 255]


class panel:
    def __init__(self, pixelX, pixelY, pixelOrder):
        self.pixelX = pixelX
        self.pixelY = pixelY
        self.pixelOrder = pixelOrder
        self.Matrix = [[pixel() for x in range(self.pixelX)] for y in range(self.pixelY)]


class grid:
    def __init__(self, panelX, panelY, panelOrder):
        self.panelX = panelX
        self.panelY = panelY
        self.panelOrder = panelOrder

        global panelPixelX
        self.panelPixelX = panelPixelX
        global panelPixelY
        self.panelPixelY = panelPixelY

        self.Matrix = [[panel(self.panelPixelX, self.panelPixelY, self.panelOrder) for x in range(self.panelX)] for y in range(self.panelY)]


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

serialMaster, serialSlave = pty.openpty()
s_name = os.ttyname(serialSlave)
serialDevice = serial.Serial(s_name)


def writeSerialTestText():
    global serialDevice
    # To Write to the device
    serialDevice.write('Your text')


def readSerialBuffer():
    global serialMaster
    # To read from the device
    returnBuffer = os.read(serialMaster, 1)
    if returnBuffer == '':
        return 0
    else:
        return int(returnBuffer)


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 500))

    pygame.display.set_caption("Pixellamp - Matrix Emulator")

    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    clock = pygame.time.Clock()

    global gridPanelX
    global gridPanelY

    panelGrid = grid(gridPanelX, gridPanelY, "HL")
    print panelGrid
    running = 1

    while running:
        clock.tick(30)  # fps
        screen.fill((0, 0, 0))  # fill window black
        # counter stuff
        currentX = 0
        currentY = 0

        currentPanelCountX = 0
        currentPanelCountY = 0

        currentPixel = 0  # just to keep track where we are

        # print str(readSerialBuffer())

        # print(x[i][j])
        # Draw the grid
        for currentPanelY in range(panelGrid.panelY):
            for currentPanelX in range(panelGrid.panelX):
                # panel inside grid
                # for currentPixelY in range(panelGrid.Matrix[currentPanelX][currentPanelY].pixelY):
                for currentPixelY in range(panelGrid.Matrix[0][0].pixelY):
                    for currentPixelX in range(panelGrid.Matrix[0][0].pixelX):
                        # pixel inside panel
                        # color = WHITE
                        # color = panelGrid.Matrix[currentPanelX, currentPanelY]

                        currentPanelOffsetX = currentPanelX * (panelGrid.Matrix[0][0].pixelX * (pixelWidth + pixelMargin) + panelMargin)
                        currentPanelOffsetY = currentPanelY * (panelGrid.Matrix[0][0].pixelY * (pixelWidth + pixelMargin) + panelMargin)

                        currentX = (pixelMargin + pixelWidth) * currentPixelX + pixelMargin + currentPanelOffsetX
                        currentY = (pixelMargin + pixelHeight) * currentPixelY + pixelMargin + currentPanelOffsetY

                        RED = randint(0, 255)
                        GREEN = randint(0, 255)
                        BLUE = randint(0, 255)

                        # draw that dirty little pixel
                        pygame.draw.rect(screen, [RED, GREEN, BLUE], [currentX, currentY, pixelWidth, pixelHeight])
                        pygame.draw.rect(screen, [255, 255, 255], [currentX, currentY, pixelWidth, pixelHeight], 1)

                        # print 'Pa: ' + str(currentPanelX) + ' ' + str(currentPanelY)
                        # print 'Pi: ' + str(currentPixelX) + ' ' + str(currentPixelY)
                        # print 'PC: ' + str(currentPixel)

                        currentPixel = currentPixel + 1
                        # print '-----------'

                currentPanelCountX = currentPanelCountX + (pixelMargin * 2)
            currentPanelCountY = currentPanelCountX + (pixelMargin * 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        pygame.display.flip()


main()
