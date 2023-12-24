from constants import *
from flocks import GrassFlock, SheepFlock, WolfFlock
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
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

    def init(self):
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

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