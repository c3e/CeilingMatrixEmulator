import pygame
import os
import pty
# import serial
from random import randint

pixelWidth = 8
pixelHeight = 8
pixelMargin = 2
panelMargin = 5

panelPixelX = 8
panelPixelY = 8

gridPanelX = 10
gridPanelY = 5

# calculate complete number of pixels
pixelBufferNumber = (panelPixelX * panelPixelY) * (gridPanelX * gridPanelY) * 3


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


class SerialEmulator:
    # master, slave = pty.openpty()
    # s_name = os.ttyname(slave)
    # ser = serial.Serial(s_name)
    # To Write to the device
    # ser.write('Your text')
    # To read from the device
    # os.read(master, 1000)

    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.s_name = os.ttyname(self.slave)
        print("Hey use this serial port:", self.s_name)

    def writeSerialTestText(self):
        # To Write to the device
        self.master.write('Your text')

    def readSerialBuffer(self):
        # To read from the device
        returnBuffer = os.read(self.master, 1)

        if returnBuffer == '':
            return 0
        else:
            # print ord(returnBuffer)
            return ord(returnBuffer)


virtualSerial = SerialEmulator()
pixelBuffer = [0] * pixelBufferNumber


def updatePixelBuffer():
    global virtualSerial
    global pixelBufferNumber
    global pixelBuffer

    # int idx = 0;
    # for (size_t i = 0; i < NUM_LINES*NUM_LEDS_PER_LINE; i++) {
    #   pixelbuffer[idx++] = gammaCorrection[serialGlediator()]; // G
    #   pixelbuffer[idx++] = gammaCorrection[serialGlediator()]; // R
    #   pixelbuffer[idx++] = gammaCorrection[serialGlediator()]; // B
    #   pixelbuffer[idx++] = gammaCorrection[whiteStart];        // W
    # }

    while virtualSerial.readSerialBuffer() != 1:
        # lets wait some until sync
        pass

    for currentPixelInBuffer in range(pixelBufferNumber):
        pixelBuffer[currentPixelInBuffer] = virtualSerial.readSerialBuffer()


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

        updatePixelBuffer()
        # print "Buffer update done."

        global pixelBuffer

        global panelPixelX
        global panelPixelY

        valuesPerPanel = panelPixelX * panelPixelY * 3

        currentPanelX = 0
        currentPanelY = 0

        for bufferIndex in range(len(pixelBuffer)):
            if bufferIndex % valuesPerPanel == 0:
                if bufferIndex == 0:
                    pass
                else:
                    currentPanelX = currentPanelX + 1
                    currentX = 0
                    currentY = 0
                # else:
                # pass

            if currentPanelX == panelGrid.panelX:
                currentPanelX = 0
                currentPanelY = currentPanelY + 1

            if bufferIndex % 3 == 0:
                red = pixelBuffer[bufferIndex]
                green = pixelBuffer[bufferIndex + 1]
                blue = pixelBuffer[bufferIndex + 2]
                # print("Matrix[", currentPanelY, "][", currentPanelX, "].Matrix[", currentX, "][", currentY, "] = [", red, ", ", green, ", ", blue, "]", bufferIndex)
                panelGrid.Matrix[currentPanelY][currentPanelX].Matrix[currentX][currentY].color = [red, green, blue]
                currentX = currentX + 1

            if currentX == panelPixelX:
                currentY = currentY + 1
                currentX = 0

            if currentY == panelPixelY:
                currentY = 0

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

                        # RED = randint(0, 255)
                        # GREEN = randint(0, 255)
                        # BLUE = randint(0, 255)

                        # draw that dirty little pixel
                        # pygame.draw.rect(screen, [RED, GREEN, BLUE], [currentX, currentY, pixelWidth, pixelHeight])
                        pygame.draw.rect(screen, panelGrid.Matrix[currentPanelY][currentPanelX].Matrix[currentPixelX][currentPixelY].color, [currentX, currentY, pixelWidth, pixelHeight])
                        # pygame.draw.rect(screen, [255, 255, 255], [currentX, currentY, pixelWidth, pixelHeight], 1)

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
