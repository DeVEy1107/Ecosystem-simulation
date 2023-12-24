import random

import pygame 

from constants import *
from creatures import *
from tilemap import Tilemap

from tools import debug

class Timer(object):
    def __init__(self, timeInterval):
        self.absTime = 0
        self.time = 0
        self.timeInterval = timeInterval

    def update(self):
        self.absTime += 1
        if self.absTime % self.timeInterval == 0:
            self.time += 1

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
            sheep.move()
            sheep.seekingFood(foods)
            if sheep.property.matingDesireLevel >= sheep.property.matingDesireThreshold:
                sheep.reproduce(self.flock)
            sheep.escape(predators)
            sheep.detectTerrain(terrains.waterTiles)
            sheep.update()
            sheep.limits(*self.offset)

    def draw(self, screen):
        for sheep in self.flock:
            sheep.draw(screen)
            if self.showInfo:
                sheep.drawInfo(screen)
  
class WolfFlock(Flock):
    def __init__(self):
        super().__init__()
        self.showInfo = False

    def add(self, x, y):
        self.flock.add(Wolf(x, y))

    def update(self, foods, terrains):
        for wolf in self.flock:
            wolf.move()
            wolf.seekingFood(foods)
            if wolf.property.matingDesireLevel >= wolf.property.matingDesireThreshold:
                wolf.reproduce(self.flock)
            wolf.detectTerrain(terrains.waterTiles)
            wolf.update()
            wolf.limits(*self.offset)

    def draw(self, screen):
        for wolf in self.flock:
            wolf.draw(screen)
            if self.showInfo:
                wolf.drawInfo(screen)

class GrassFlock(Flock):
    def __init__(self):
        super().__init__()
        

    def randSpawn(self, num):
        for _ in range(num):
            x = random.randint(self.offset[0], MAP_WIDTH-TILE_SIZE+self.offset[0])
            y = random.randint(self.offset[1], MAP_HEIGHT-TILE_SIZE+self.offset[1])
            self.flock.add(Grass(x, y))

    def draw(self, screen):
        for grass in self.flock:
            grass.draw(screen)
        
class World(object):
    def __init__(self):
        self.timer = Timer(TIME_INTERVAL)

        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock()

    def init(self):
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock()

    def update(self):
        self.timer.update()
        self.sheep.update(self.grass.flock, self.wolfs.flock, self.terrains)
        self.wolfs.update(self.sheep.flock, self.terrains)

        if self.timer.time % 10 == 0:
            self.grass.randSpawn(2)
    
    def draw(self, screen):
        self.terrains.draw(screen)
        self.grass.draw(screen)
        self.sheep.draw(screen)
        self.wolfs.draw(screen)

    def shift(self, dx, dy):
        self.terrains.shift(dx, dy)
        self.sheep.shift(dx, dy)
        self.wolfs.shift(dx, dy)
        self.grass.shift(dx, dy)

    def drawGroupsCount(self):
        msg = f"sheeps: {len(self.sheep.flock)} \nWolfs: {len(self.wolfs.flock)} \nFoods: {len(self.grass.flock)}"
        debug(msg)