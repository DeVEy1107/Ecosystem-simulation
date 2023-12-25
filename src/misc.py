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
    def __init__(self, sprite):
        self.sprite = sprite
        self.font = pygame.font.Font(None, 30)
        self.font2 = pygame.font.Font(None, 30)
        self.textSurface = pygame.Surface((60, 60), pygame.SRCALPHA)
        # self.detailTextEmbeddedSurface = pygame.Surface((180, 200), pygame.SRCALPHA)
        self.detailTextSurface = pygame.Surface((60, 60), pygame.SRCALPHA)
        # self.detailTextEmbeddedSurface.fill((169, 169, 169))

    def update(self):
        msg = "HungerLevel: {:.1f}/100 \nMatingDesireLevel: {:.1f}/100 \nVelocity: {:.1f}".format(
            self.sprite.property.hungerLevel, self.sprite.property.matingDesireLevel,
            self.sprite.speed
        )
        self.textSurface = self.font.render(msg, True, (0, 0, 255))
        
        msg = f"HungerSpeed: {self.sprite.property.hungerSpeed:.3f}\n" + \
              f"MatingDesireSpeed: {self.sprite.property.matingDesireSpeed:.3f}\n" + \
              f"Speed: {self.sprite.property.speed:.3f}\n" + \
              f"DetectionRange: {self.sprite.property.detectionRange:.1f}\n" + \
              f"InteractiveRange: {self.sprite.property.interactiveRange:.1f}\n" + \
              f"TowarfFoodSpeed: {self.sprite.property.towarfFoodSpeed:.3f}\n"
        self.detailTextSurface = self.font2.render(msg, True, (255, 255, 255), (169, 169, 169))

    def draw(self, screen):
        self.drawInteractiveRange(screen)
        self.drawDetectionRange(screen)
        
    def drawInfo(self, screen): 
        if self.isMouseOver():
            self.drawBBox(screen)
            screen.blit(self.textSurface, (self.sprite.rect.x, self.sprite.rect.y - 70))
            x, _ = screen.get_size()
            screen.blit(self.detailTextSurface, (x - 280, 20))


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
    
    def isMouseOver(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        return self.sprite.rect.collidepoint(mouseX, mouseY)