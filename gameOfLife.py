import sys
import pygame
import random
import copy


class GameOfLife:
    def __init__(self):
        self.name = "Game of Life"

        # Config
        self.mapSize = 64
        self.win_width = self.mapSize * 10
        self.win_height = self.mapSize * 10

        # Determines how many cells are initially
        self.probability = 0.5

        # Graphics
        self.blue = (0, 128, 255)
        self.black = (0, 0, 0)

        pygame.init()
        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode(
            (self.win_width, self.win_height))

        self.clock = pygame.time.Clock()

        # Control main loop
        self.running = True

        # Game state
        self.alive = set()
        self.map = [[]]

        self.createMap()

    # Generate the matrix with random values (1 or 0) and
    # Creating the "alive" set with cells that are alive
    def createMap(self):
        self.map = [[0 for i in range(self.mapSize)]
                    for j in range(self.mapSize)]
        for x in range(self.mapSize):
            for y in range(self.mapSize):
                value = 1 if random.random() < self.probability else 0
                self.map[x][y] = value
                if value == 1:
                    self.alive.add((x, y))

    # Drawing rectangles on the screen based on the
    # cells that are alive
    def drawMap(self):
        for c in self.alive:
            (x, y) = c
            color = self.blue
            pygame.draw.rect(self.screen, color,
                             pygame.Rect(y * 10, x * 10, 5, 5))

    # Helper method to print the map inside the terminal
    def printMap(self):
        for x in range(self.mapSize):
            for y in range(self.mapSize):
                if self.map[x][y] == 1:
                    sys.stdout.write("# ")
                else:
                    sys.stdout.write(". ")
            print("")

    # Returns adjacent positions given position (8 directions)
    def getAdjacent(self, pos):
        res = []
        (x, y) = pos
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                if x + i >= self.mapSize or y + j >= self.mapSize or x + i < 0 or y + j < 0:
                    continue
                res.append((x + i, y + j))
        return res

    def isCellAlive(self, cell):
        (x, y) = cell
        return self.map[x][y] == 1

    # Computes the next state based on the given Scenarios
    def runIteration(self):
        dead = set()
        # Scenarios 0, 3, 5 are contained within the rest (no action is required)
        # Scenario 1, 2 - Underpopulation, Overcrowding
        for c in self.alive:
            aliveAdj = list(
                filter(lambda x: self.isCellAlive(x), self.getAdjacent(c)))
            if len(aliveAdj) < 2 or len(aliveAdj) > 3:
                dead.add(c)
        alive = set()

        # Scenario 4 - Creation of Life
        for x in range(self.mapSize):
            for y in range(self.mapSize):
                if (x, y) in self.alive:
                    continue
                aliveAdj = list(
                    filter(lambda c: self.isCellAlive(c), self.getAdjacent((x, y))))

                if len(aliveAdj) == 3:
                    alive.add((x, y))

        # Creating the next state of the game
        self.alive = self.alive.difference(dead)
        self.alive = self.alive.union(alive)
        self.updateMap()

    # Updating the map with the new state
    def updateMap(self):
        self.map = [[0 for i in range(self.mapSize)]
                    for j in range(self.mapSize)]

        for c in self.alive:
            self.map[c[0]][c[1]] = 1

    # Starts the game
    def start(self):
        # main loop
        # Delay variables
        current_tick = 0
        next_tick = 0

        while self.running:
            current_tick = pygame.time.get_ticks()
            if current_tick > next_tick:
                next_tick += 200  # interval
                self.screen.fill(self.black)
                self.drawMap()
                self.runIteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # This will update the contents of the entire display
            pygame.display.flip()
            # This method should be called once per frame. It will
            # compute how many milliseconds have passed since the previous call.
            self.clock.tick(60)


game = GameOfLife()
# Print the map for Debug
# game.printMap()
game.start()
