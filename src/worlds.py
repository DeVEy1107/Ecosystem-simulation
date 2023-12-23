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

class World(object):
    def __init__(self):
        self.timer = Timer(TIME_INTERVAL)

    def init(self):
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)
        
        self.monkeys = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.wolfs = pygame.sprite.Group()

        self.showInfo = False
        self.offset = self.terrains.offset
        self.addMonkeys(20)


    def addMonkeys(self, num):
        for _ in range(num):
            self.monkeys.add(
                Monkey(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
            )

    def addWolf(self, x, y):
        self.wolfs.add(Wolf(x, y))

    def addWolfs(self, num):
        for _ in range(num):
            self.wolfs.add(
                Wolf(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
            )

    def addFoods(self, num):
        for _ in range(num):
            self.foods.add(
                Food(
                    random.randint(self.offset[0], MAP_WIDTH-self.offset[0]), 
                    random.randint(self.offset[1], MAP_HEIGHT-self.offset[1])
                )
            )

    def update(self):
        self.timer.update()
        for monkey in self.monkeys:
            monkey.escape(self.wolfs)
            if not monkey.isMating:
                monkey.seekingFood(self.foods)
            if monkey.property.matingDesireLevel >= 100:
                monkey.reproduce(self.monkeys)
            monkey.move()
            monkey.update()
            monkey.limits(*self.offset)

        for wolf in self.wolfs:
            if not wolf.isMating:
                wolf.seekingFood(self.monkeys)
            if wolf.property.matingDesireLevel >= 100:
                wolf.reproduce(self.wolfs)
            wolf.move()
            wolf.update()
            wolf.limits(*self.offset)

        if self.timer.time % 10 == 0:
            self.addFoods(1)
    
    def draw(self, screen):
        self.terrains.draw(screen)

        self.foods.draw(screen)

        for monkey in self.monkeys:
            monkey.showInfo = self.showInfo
            monkey.draw(screen)
            
        for wolf in self.wolfs:
            wolf.showInfo = self.showInfo
            wolf.draw(screen)


    def shift(self, dx, dy):
        self.terrains.shift(dx, dy)
        for monkey in self.monkeys:
            monkey.shift(dx, dy)
        
        for wolf in self.wolfs:
            wolf.shift(dx, dy)

        for food in self.foods:
            food.shift(dx, dy)

        self.offset = self.terrains.offset

    def getCurrentTime(self):
        return self.timer.time

    def drawGroupsCount(self):
        msg = f"Monkeys: {len(self.monkeys)} \nWolfs: {len(self.wolfs)} \nFoods: {len(self.foods)}"
        debug(msg)