import random
import pygame

from constants import *
from creatures import Grass, Sheep, Wolf

class Flock(object):
    '''
        用來管理及儲存生物群體的類別
    '''
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

    def __len__(self):
        return len(self.flock)

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
            sheep.infoLabel.drawInfo(screen)
  
    def randAdds(self, num):
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
            wolf.infoLabel.drawInfo(screen)

    def randAdds(self, num):
        for _ in range(num):
            x = random.randint(0, MAP_WIDTH - TILE_SIZE)
            y = random.randint(0, MAP_HEIGHT - TILE_SIZE)
            self.flock.add(Wolf(x, y))

class GrassFlock(Flock):
    def __init__(self, grassCoords):
        super().__init__()
        self.grassCoords = grassCoords
        self.growingTime = GRASS_GROWING_TIME
        self.newNum = GRASS_GROWING_NUM

    def add(self, x, y):
        self.flock.add(Grass(x, y))

    def update(self, timerTime):
        if timerTime.time % self.growingTime == 0:
            self.randAdds(self.newNum)

    def randAdds(self, num):
        while num:
            x, y = random.choice(self.grassCoords)
            newX = x * TILE_SIZE + self.offset[0]
            newY = y * TILE_SIZE + self.offset[1]
            self.add(newX, newY)
            num -= 1

    def draw(self, screen):
        for grass in self.flock:
            grass.draw(screen)