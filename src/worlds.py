from constants import *
from misc import Timer
from flocks import GrassFlock, SheepFlock, WolfFlock
from tilemap import Tilemap
from tools import debug

class World(object):
    def __init__(self):
        self.timer = Timer(TIME_INTERVAL)
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

    def init(self):
        self.timer = Timer(TIME_INTERVAL)
        self.terrains = Tilemap(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)
        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

    def update(self):
        self.updateTimeInterval()
        self.sheep.update(self.grass.flock, self.wolfs.flock, self.terrains)
        self.wolfs.update(self.sheep.flock, self.terrains)

        if self.timer.time % GRASS_GROWING_TIME == 0:
            self.grass.randSpawn(1)
    
        self.timer.update()

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

    def updateTimeInterval(self):
        self.sheep.setTimeInterval(self.timer.timeInterval)
        self.wolfs.setTimeInterval(self.timer.timeInterval)
        self.grass.setTimeInterval(self.timer.timeInterval)

    def setTimeInterval(self, timeInterval):
        self.timer.timeInterval = timeInterval

    def drawFlocksCount(self):
        msg = f"sheeps: {len(self.sheep.flock)} \nWolfs: {len(self.wolfs.flock)} \nFoods: {len(self.grass.flock)}"
        msg = msg + f" \nTime interval: {self.timer.timeInterval} \n World time: {self.timer.time}"
        debug(msg)