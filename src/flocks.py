import random
import pygame

from constants import *
from creatures import Grass, Sheep, Wolf

class Flock(object):
    def __init__(self):
        self.flock = pygame.sprite.Group()
        self.offset = [0, 0]
        self.showInfo = False

    def shift(self, dx, dy):
        for sprite in self.flock:
            sprite.shift(dx, dy)
        self.offset[0] += dx
        self.offset[1] += dy

    def displayInfo(self):
        self.showInfo = not self.showInfo

    def setTimeInterval(self, timeInterval):
        for sprite in self.flock:
            sprite.timer.setTimeInterval(timeInterval)

    def update(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        pass

    def add(self, *args, **kwargs):
        pass

class SheepFlock(Flock):
    def __init__(self):
        super().__init__()
        self.showInfo = False

    def add(self, x, y):
        self.flock.add(Sheep(x, y))

    def update(self, foods, predators, terrains):
        for sheep in self.flock:
            sheep.update(foods, self.flock, predators, terrains)
            sheep.limits(*self.offset)

    def draw(self, screen):
        for sheep in self.flock:
            sheep.draw(screen)
            if self.showInfo:
                sheep.infoLabel.draw(screen)
  
    def randSpawn(self, num):
        for _ in range(num):
            x = random.randint(0, MAP_WIDTH - TILE_SIZE)
            y = random.randint(0, MAP_HEIGHT - TILE_SIZE)
            self.flock.add(Sheep(x, y))

class WolfFlock(Flock):
    def __init__(self):
        super().__init__()
        self.showInfo = False

    def add(self, x, y):
        self.flock.add(Wolf(x, y))

    def update(self, foods, terrains):
        for wolf in self.flock:
            wolf.update(foods, self.flock, terrains)
            wolf.limits(*self.offset)

    def draw(self, screen):
        for wolf in self.flock:
            wolf.draw(screen)
            if self.showInfo:
                wolf.infoLabel.draw(screen)

    def randSpawn(self, num):
        for _ in range(num):
            x = random.randint(0, MAP_WIDTH - TILE_SIZE)
            y = random.randint(0, MAP_HEIGHT - TILE_SIZE)
            self.flock.add(Wolf(x, y))

class GrassFlock(Flock):
    def __init__(self, grassCoords):
        super().__init__()
        self.grassCoords = grassCoords
        self.timeCounter = 0

    def update(self):
        pass

    def randSpawn(self, num):
        while num:
            x, y = random.choice(self.grassCoords)
            spwanX = x * TILE_SIZE + self.offset[0]
            spwanY = y * TILE_SIZE + self.offset[1]
            self.flock.add(Grass(spwanX, spwanY))
            num -= 1

    def draw(self, screen):
        for grass in self.flock:
            grass.draw(screen)