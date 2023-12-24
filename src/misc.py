import pygame

from constants import *

class Timer(object):
    def __init__(self, timeInterval):
        self.absTime = 0
        self.time = 0
        self.timeInterval = timeInterval

    def update(self):
        self.absTime += 1
        if self.tick():
            self.time += 1
    
    def setTimeInterval(self, timeInterval):
        self.timeInterval = timeInterval

    def tick(self):
        return bool(self.absTime % self.timeInterval == 0)

class SpriteSheet(object):
    def __init__(self, filePath):
        self.sheet = pygame.image.load(filePath)

    def imageAt(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        return image

class SpriteAnimaition(object):
    def __init__(self, filepath, size):
        self.sprites = SpriteSheet(filepath)
        self.images = [self.sprites.imageAt((16*i, 0, 16, 16)) for i in range(4)]

        self.size = size
        self.frameDuration = ANIMATION_FRAME_DURATION 
        self.imageIndex = 0
        self.image = pygame.transform.scale(
            self.images[self.imageIndex], (int(self.size), int(self.size))
        )
        self.lastUpdateTime = pygame.time.get_ticks()

    def getImage(self):
        return self.image
    
    def update(self):
        now = pygame.time.get_ticks() 
        passedTime = now - self.lastUpdateTime

        if passedTime > self.frameDuration:
            self.lastUpdateTime = now
            self.imageIndex = (self.imageIndex + 1) % len(self.images)
            self.image = pygame.transform.scale(
                self.images[self.imageIndex], (int(self.size), int(self.size))
            )

class SpriteInfoLabel(object):
    def __init__(self, sprite, fontSize=20):
        self.sprite = sprite
        self.font = pygame.font.Font(None, fontSize)
        self.textSurface = pygame.Surface((60, 60), pygame.SRCALPHA)

    def update(self):
        msg = "Velocity: {} \nHungerLevel: {} \nMatingDesireLevel: {} \nTotalEaten: {}".format(
            self.sprite.speed, self.sprite.property.hungerLevel, 
            self.sprite.property.matingDesireLevel, self.sprite.totalEaten
        )
        self.textSurface = self.font.render(msg, True, (0, 0, 255))

    def draw(self, screen):
        self.drawBBox(screen)
        self.drawInteractiveRange(screen)
        self.drawDetectionRange(screen)
        screen.blit(self.textSurface, (self.sprite.rect.x, self.sprite.rect.y - 60))

    def drawDetectionRange(self, screen):
        pygame.draw.circle(
            screen, (0, 255, 0), self.sprite.rect.center, 
            self.sprite.property.detectionRange, width=2
        )

    def drawInteractiveRange(self, screen):
        pygame.draw.circle(
            screen, (255, 255, 0), self.sprite.rect.center,
            self.sprite.property.interactiveRange, width=2
        )
   
    def drawBBox(self, screen):
        pygame.draw.rect(
            screen, (255, 0, 0), self.sprite.rect, width=2
        )