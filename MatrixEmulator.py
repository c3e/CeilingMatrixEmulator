import pygame
import os
import pty
import threading
import time

pixelWidth = 8
pixelHeight = 8
pixelMargin = 2

panelPixelX = 8
panelPixelY = 8
panelMargin = 5

gridPanelX = 10
gridPanelY = 5

windowWidth = (((pixelWidth + pixelMargin) * panelPixelX) + panelMargin) * gridPanelX
windowHeight = (((pixelHeight + pixelMargin) * panelPixelY) + panelMargin) * gridPanelY

# calculate complete number of pixels
pixelBufferNumber = (panelPixelX * panelPixelY) * (gridPanelX * gridPanelY) * 3

running = True


class pixel:
    def __init__(self):
        self.color = [128, 128, 128]


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
    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.s_name = os.ttyname(self.slave)
        print("Hey use this serial port:", self.s_name)

    def readSerialBuffer(self):
        returnBuffer = os.read(self.master, 1)

        if returnBuffer == '':
            return 0
        else:
            # print ord(returnBuffer)
            return ord(returnBuffer)


virtualSerial = SerialEmulator()
pixelBuffer = [0] * pixelBufferNumber

panelGrid = grid(gridPanelX, gridPanelY, "HL")

newFrame = False


def mapPixelBuffer():
    global pixelBuffer
    global newFrame
    global panelPixelX
    global panelPixelY

    currentX = 0
    currentY = 0

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
    newFrame = True


def handleSerialStuff():
    global virtualSerial
    global pixelBufferNumber
    global pixelBuffer
    global running

    while running:
        if virtualSerial.readSerialBuffer() == 1:
            for currentPixelInBuffer in range(pixelBufferNumber):
                pixelBuffer[currentPixelInBuffer] = virtualSerial.readSerialBuffer()
            mapPixelBuffer()


def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))

    pygame.display.set_caption("Pixellamp - Matrix Emulator")

    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    clock = pygame.time.Clock()

    global gridPanelX
    global gridPanelY
    global newFrame
    global running

    threadSerial = threading.Thread(target=handleSerialStuff, args=[])
    threadSerial.daemon = True
    threadSerial.start()

    while running:
        clock.tick(30)  # fps
        screen.fill((0, 0, 0))  # fill window black
        # counter stuff
        currentX = 0
        currentY = 0

        currentPixel = 0  # just to keep track where we are

        # print "Buffer update done."

        # print(x[i][j])
        # Draw the grid
        if newFrame:
            for currentPanelY in range(panelGrid.panelY):
                for currentPanelX in range(panelGrid.panelX):
                    # panel inside grid
                    for currentPixelY in range(panelGrid.Matrix[0][0].pixelY):
                        for currentPixelX in range(panelGrid.Matrix[0][0].pixelX):
                            # pixel inside panel
                            currentPanelOffsetX = currentPanelX * (panelGrid.Matrix[0][0].pixelX * (pixelWidth + pixelMargin) + panelMargin)
                            currentPanelOffsetY = currentPanelY * (panelGrid.Matrix[0][0].pixelY * (pixelWidth + pixelMargin) + panelMargin)

                            currentX = (pixelMargin + pixelWidth) * currentPixelX + pixelMargin + currentPanelOffsetX
                            currentY = (pixelMargin + pixelHeight) * currentPixelY + pixelMargin + currentPanelOffsetY

                            # draw that dirty little pixel
                            pygame.draw.rect(screen, panelGrid.Matrix[currentPanelY][currentPanelX].Matrix[currentPixelX][currentPixelY].color, [currentX, currentY, pixelWidth, pixelHeight])
                            # pygame.draw.rect(screen, [255, 255, 255], [currentX, currentY, pixelWidth, pixelHeight], 1)
                            currentPixel = currentPixel + 1
            pygame.display.flip()
            newFrame = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()


main()
