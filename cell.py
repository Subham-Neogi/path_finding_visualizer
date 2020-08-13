class Cell:
    def __init__(self, pygame, screen, w, h, row, cols, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1
        self.pygame = pygame
        self.screen = screen
        self.width = w
        self.height = h
        self.row = row
        self.cols = cols

    def show(self, color, st):
        if self.closed == False :
            self.pygame.draw.rect(self.screen, color, (self.i * self.width, self.j * self.height, self.width, self.height), st)
            self.pygame.display.update()

    def path(self, color, st):
        self.pygame.draw.rect(self.screen, color, (self.i * self.width, self.j * self.height, self.width, self.height), st)
        self.pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < self.cols-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < self.row-1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])
        # if i < self.cols-1 and j < self.row-1 and grid[self.i + 1][j + 1].obs == False:
        #     self.neighbors.append(grid[self.i + 1][j + 1])
        # if i < self.cols-1 and j > 0 and grid[self.i + 1][j - 1].obs == False:
        #     self.neighbors.append(grid[self.i + 1][j - 1])
        # if i > 0 and j < self.row-1 and grid[self.i - 1][j + 1].obs == False:
        #     self.neighbors.append(grid[self.i - 1][j + 1])
        # if i > 0 and j > 0 and grid[self.i - 1][j - 1].obs == False:
        #     self.neighbors.append(grid[self.i - 1][j - 1])
