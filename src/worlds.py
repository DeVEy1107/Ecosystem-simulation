import random

import pygame 


from constants import *
from creatures import *
from tilemap import Tilemap

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

        self.monkeys = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.wolfs = pygame.sprite.Group()

        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)
       
        self.showInfo = False

    def init(self):
        self.addMonkeys(20)
        self.addWolfs(5)

    def addMonkeys(self, num):
        for _ in range(num):
            self.monkeys.add(
                Monkey(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
            )

    def addWolfs(self, num):
        for _ in range(num):
            self.wolfs.add(
                Wolf(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
            )

    def addFoods(self, num):
        for _ in range(num):
            self.fruits.add(
                Banana(random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT))
            )

    def update(self):
        self.timer.update()

        for monkey in self.monkeys:
            monkey.update()
            monkey.move()
            if not monkey.isMating:
                monkey.seekingFood(self.fruits)
            if monkey.property.matingDesireLevel >= 100:
                monkey.reproduce(self.monkeys)
            monkey.limits(*self.terrains.getOffset())

        for wolf in self.wolfs:
            wolf.update()
            wolf.move()
            if not wolf.isMating:
                wolf.seekingFood(self.monkeys)
            if wolf.property.matingDesireLevel >= 100:
                wolf.reproduce(self.wolfs)
            wolf.limits(*self.terrains.getOffset())

        if self.timer.time % 10 == 0:
            self.addFoods(2)
    
    def draw(self, screen):
        self.terrains.draw(screen)

        self.fruits.draw(screen)

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

        for fruit in self.fruits:
            fruit.shift(dx, dy)

    def getCurrentTime(self):
        return self.timer.time