from random import randint

import numpy as np
import pygame

from perlin_noise import PerlinNoise


class SpriteSheet(object):
    def __init__(self, filePath):
        self.sheet = pygame.image.load(filePath)

    def imageAt(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        return image

class NoiseGenerator(object):
    def __init__(self, seed=0):
        
        self.seed = seed

        self.isRand = True
        self.randomSeedRange = (0, 100000)

    def getNoise2d(self, width: int, height: int):
        a, b = self.randomSeedRange
        self.seed = randint(a, b) if self.isRand else self.seed
        
        noise1 = PerlinNoise(octaves=3)
        noise2 = PerlinNoise(octaves=6)
        noise3 = PerlinNoise(octaves=12)
        noise4 = PerlinNoise(octaves=24)

        pic = []
        for i in range(height):
            row = []
            for j in range(width):
                noise_val = noise1([i/height, j/width])
                noise_val += 0.5 * noise2([i/height, j/width])
                noise_val += 0.25 * noise3([i/height, j/width])
                noise_val += 0.125 * noise4([i/height, j/width])

                row.append(noise_val)
            pic.append(row)

        return self._normalize(np.array(pic))


    def _normalize(self, ndarr: np.ndarray) -> np.ndarray:
        minimumValue = np.min(ndarr)
        fullRange = np.max(ndarr) - np.min(ndarr)
        return (ndarr - minimumValue) / fullRange


def debug(info, x=10, y=10):
    font = pygame.font.Font(None, 30)

    debugSurface = font.render(str(info), True, 'White')
    debugRect = debugSurface.get_rect(topleft=(x, y))
    
    screen = pygame.display.get_surface()
    rectSurface = pygame.Surface(debugRect.size)
    rectSurface.set_alpha(64)
    rectSurface.fill((0, 0, 0))
    pygame.draw.rect(rectSurface, (0, 0, 0), debugRect)

    screen.blit(rectSurface, debugRect)
    screen.blit(debugSurface, debugRect)