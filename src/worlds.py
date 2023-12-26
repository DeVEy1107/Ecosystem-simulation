from constants import *
from misc import Timer
from flocks import GrassFlock, SheepFlock, WolfFlock
from tilemap import Terrains
from tools import debug

class World(object):
    def __init__(self):
        self.timer = Timer(TIME_INTERVAL)
        self.terrains = Terrains(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)

        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

    def init(self):
        self.timer = Timer(TIME_INTERVAL)
        self.terrains = Terrains(MAP_WIDTH // TILE_SIZE, MAP_HEIGHT // TILE_SIZE)
        self.sheep = SheepFlock()
        self.wolfs = WolfFlock()
        self.grass = GrassFlock(self.terrains.grassCoords)

    def update(self):
        self.updateTimeInterval()
        self.sheep.update(self.grass.flock, self.wolfs.flock, self.terrains)
        self.wolfs.update(self.sheep.flock, self.terrains)
        self.grass.update(self.timer)
    
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

    def drawWorldInfo(self):
        '''
            顯示世界時間, 更新時間間隔, 生物數量
        '''
        msg = "===============\n" + \
              f"World time: {self.timer.time}\n" + \
              f"Time interval: {self.timer.timeInterval:.0f}\n" + \
               "===============\n" + \
              f"Sheep: {len(self.sheep)}\n" + \
              f"Wolfs: {len(self.wolfs)}\n" + \
              f"Grass: {len(self.grass)}\n"
              
        debug(msg)