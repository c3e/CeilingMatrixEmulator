import pygame

pixelWidth = 8
pixelHeight = 8
pixelMargin = 2

panelPixelX = 8
panelPixelY = 8

gridPanelX = 3
gridPanelY = 3


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((255, 255))

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
        currentPixel = 0  # just to keep track where we are

        # print(x[i][j])
        # Draw the grid
        for currentPanelX in range(len(panelGrid.Matrix)):
            for currentPanelY in range(len(panelGrid.Matrix)):
                # panel inside grid
                for currentPixelX in range(len(panelGrid.Matrix)):
                    for currentPixelY in range(len(panelGrid.Matrix)):
                        # pixel inside panel
                        # color = panelGrid.Matrix[currentPanelX, currentPanelY]
                        color = WHITE
                        currentX = (pixelMargin + pixelWidth) * currentPixelX + pixelMargin
                        currentY = (pixelMargin + pixelHeight) * currentPixelY + pixelMargin
                        currentPixel = currentPixel + 1
                        # draw that dirty little pixel
                        pygame.draw.rect(screen, color, [currentX, currentY, pixelWidth, pixelHeight], 1)

            currentY = currentY + pixelMargin + 2
        currentX = currentX + pixelMargin + 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        pygame.display.flip()


main()
