import pygame

from tools import NoiseGenerator
from misc import SpriteSheet
from constants import *

tileTypes = {
    "water": (0, 0, 16, 16),
    "grass1": (16, 0, 16, 16),
    "grass2": (32, 0, 16, 16),
    "sand1": (48, 0, 16, 16),
    "sand2": (64, 0, 16, 16)
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.tileSize = TILE_SIZE
        self.image = pygame.transform.scale(image, (self.tileSize, self.tileSize))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Tileset(object):
    def __init__(self):
        self.tileSheet = SpriteSheet(TILE_IMAGE_PATH)

        self.tileImages = {}
        
        for tileType, tileRect in tileTypes.items():
            self.tileImages[tileType] = self.tileSheet.imageAt(tileRect).convert_alpha()

    def getTileImage(self, tileType):
        return self.tileImages[tileType]

class Tilemap(object):
    def __init__(self, width, height):
        self.width, self.height = width, height

        self.tileset = Tileset()
        
        self.grassCoords = [] 

        self.landTiles = pygame.sprite.Group()
        self.waterTiles = pygame.sprite.Group()

        self.noise = NoiseGenerator()

        self.generateWorldMap(width, height)

        self.offset = [0, 0]

    def generateWorldMap(self, width, height):
        noise2d = self.noise.getNoise2d(width, height)

        for y in range(height):
            for x in range(width):
                if noise2d[y][x] < 0.3:
                    self.waterTiles.add(
                        Tile(
                            int(TILE_SIZE*x), int(TILE_SIZE*y), 
                            self.tileset.getTileImage("water")
                        )
                    )
                elif noise2d[y][x] >= 0.3 and noise2d[y][x] < 0.35:
                    self.landTiles.add(
                        Tile(
                            int(TILE_SIZE*x), int(TILE_SIZE*y), 
                            self.tileset.getTileImage("sand1")
                        )
                    )
                elif noise2d[y][x] > 0.35:
                    self.grassCoords.append((x, y))
                    self.landTiles.add(
                        Tile(
                            int(TILE_SIZE*x), int(TILE_SIZE*y), 
                            self.tileset.getTileImage("grass1")
                        )
                    )

    def draw(self, screen):
        self.landTiles.draw(screen)
        self.waterTiles.draw(screen)


    def shift(self, dx, dy):
        for tile in self.landTiles:
            tile.rect.x += dx
            tile.rect.y += dy

        for tile in self.waterTiles:
            tile.rect.x += dx
            tile.rect.y += dy

        self.offset[0] += dx
        self.offset[1] += dy


                