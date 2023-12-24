import random

import pygame

from pygame import Vector2

from constants import *
from tools import SpriteSheet


class Property(object):
    def __init__(self, hungerLevel=100, speed=2, detectionRange=100, hungerSpeed=2,
                 foodAmount=60, interactiveRange=30, matingDesireLevel=0,
                 matingDesireSpeed=5, matingDesireThreshold=100, towardFoodSpeed=3):
        self.hungerLevel = hungerLevel
        self.hungerSpeed = hungerSpeed
        self.matingDesireLevel = matingDesireLevel
        self.matingDesireSpeed = matingDesireSpeed
        self.matingDesireThreshold = matingDesireThreshold
        self.speed = speed
        self.towarfFoodSpeed = towardFoodSpeed
        self.detectionRange = detectionRange
        self.interactiveRange = interactiveRange

        self.foodAmount = foodAmount

class SpriteAnimaition(object):
    def __init__(self, filepath, size):
        self.sprites = SpriteSheet(filepath)
        self.images = [self.sprites.imageAt((16*i, 0, 16, 16)) for i in range(4)]

        self.size = size
        self.frameDuration = 200
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

class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, filepath):
        super().__init__()

        self.size = TILE_SIZE
        self.filepath = filepath
        self.spriteAnimation = SpriteAnimaition(filepath, self.size)
        self.rect = self.spriteAnimation.getImage().get_rect(topleft=(x, y))

        self.timeCounter = 0

        self.position = Vector2(self.rect.centerx, self.rect.centery)
        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        self.property = Property()

        self.speed = random.randint(self.property.speed - 1, self.property.speed + 1)
        self.changeDirectionTimer = random.randint(30, 60)

        self.infoLabel = Label(20)

        self.totalEaten = 0

    def move(self):
        self.changeDirectionTimer -= 1
        if self.changeDirectionTimer <= 0:
            self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.changeDirectionTimer = random.randint(10, 30) 
            self.speed = self.property.speed
        
    def reproduce(self, *args, **kwargs):
        pass

    def seekingFood(self, foods):
        for food in foods:
            distance = self.position.distance_to(food.position)
            if distance < self.property.detectionRange:
                self.speed = self.property.towarfFoodSpeed
                self.direction = Vector2((food.position - self.position)).normalize()

            if distance < self.property.interactiveRange:
                self.property.hungerLevel += food.property.foodAmount
                food.kill()
                self.totalEaten += 1

    def detectTerrain(self, terrainTiles):
        for tile in terrainTiles:
            if self.position.x // TILE_SIZE == tile.rect.x // TILE_SIZE \
                and self.position.y // TILE_SIZE == tile.rect.y // TILE_SIZE :
                self.speed = 0.75 * self.property.speed

    def limits(self, x0, y0):
        self.rect.x = max(x0, min(self.rect.x, MAP_WIDTH + x0 - int(self.size)))
        self.rect.y = max(y0, min(self.rect.y, MAP_HEIGHT + y0 - int(self.size)))   

    def propertyUpdate(self):
        if self.timeCounter % 20 == 0:
            self.property.hungerLevel -= self.property.hungerSpeed
            if self.property.matingDesireLevel < 100:
                self.property.matingDesireLevel += self.property.matingDesireSpeed
            else:
                self.property.matingDesireLevel = 100 

        if self.property.hungerLevel < 0:
            self.kill()
        

    def update(self):
        self.spriteAnimation.update()

        self.timeCounter += 1
        self.propertyUpdate()

        self.position += self.direction * self.speed
        self.rect.center = self.position

        msg = "Velocity: {} \nHungerLevel: {} \nMatingDesireLevel: {} \nTotalEaten: {}".format(
            self.speed, self.property.hungerLevel, self.property.matingDesireLevel, self.totalEaten
        )
        self.infoLabel.update(msg)

    def drawInfo(self, screen):
        self.drawDetectionRange(screen)
        self.drawInteractiveRange(screen)
        self.drawProperty(screen)
        self.drawBBox(screen)

    def draw(self, screen):
        screen.blit(self.spriteAnimation.getImage(), self.rect)

    def drawProperty(self, screen):
        self.infoLabel.draw(screen, self.rect.x, self.rect.y - 60)

    def drawDetectionRange(self, screen):
        pygame.draw.circle(
            screen, (0, 255, 0), self.rect.center, 
            self.property.detectionRange, width=2
        )

    def drawInteractiveRange(self, screen):
        pygame.draw.circle(
            screen, (255, 255, 0), self.rect.center,
            self.property.interactiveRange, width=2
        )
   
    def drawBBox(self, screen):
        pygame.draw.rect(
            screen, (255, 0, 0), self.rect, width=2
        )

    def shift(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
        self.position.x = self.rect.centerx 
        self.position.y = self.rect.centery


class Label:
    def __init__(self, fontSize):
        self.font = pygame.font.Font(None, fontSize)
        self.text_surface = pygame.Surface((60, 60), pygame.SRCALPHA)

    def update(self, msg):
        self.text_surface = self.font.render(
            msg, 
            True, (0, 0, 255)
        )

    def draw(self, screen, x, y):
        screen.blit(self.text_surface, (x, y))

class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.property = Property(foodAmount=30)
        self.spriteSheet = SpriteSheet(GRASS_IMAGE_PATH)
        self.image = self.spriteSheet.imageAt((80, 112, 16, 16))
        self.image = pygame.transform.scale(self.image, (int(TILE_SIZE), int(TILE_SIZE)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = Vector2(self.rect.centerx, self.rect.centery)
        self.timeCounter = 0

    def update(self):
        self.timeCounter += 1
        if self.timeCounter % 200 == 0:
            self.kill()
    
    def draw(self, screen): 
        screen.blit(self.image, self.rect)

    def shift(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.position.x = self.rect.centerx 
        self.position.y = self.rect.centery


class Sheep(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, SHEEP_IMAGE_PATH)

        self.property = Property(
            hungerLevel=100, 
            speed=2,
            detectionRange=100,
            foodAmount=60,
            towardFoodSpeed=2.5
        )
        
    def escape(self, predators):
        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance <= self.property.detectionRange:
                self.speed = 1.8 * self.property.speed
                self.direction = Vector2((self.position - predator.position)).normalize()

    def reproduce(self, mates):
        targetMate = None
        for mate in mates:
            distance = self.position.distance_to(mate.position)
            if mate is not self and distance < self.property.detectionRange \
                and mate.property.matingDesireLevel >= 100:
                self.speed = 1
                self.direction = Vector2((mate.position - self.position)).normalize()
                targetMate = mate   
                break

        if targetMate is not None and distance < self.property.interactiveRange:
            self.speed = 0

            newPosition = self.position if random.randint(0, 1) == 0 else mate.position

            newCreature = Sheep(newPosition.x, newPosition.y)
        
            mates.add(newCreature)

            self.property.matingDesireLevel = 0
            mate.property.matingDesireLevel = 0

    

class Wolf(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, WOLF_IMAGE_PATH)

        self.property = Property(
            hungerLevel=1000,
            speed=3,
            detectionRange=170,
            towardFoodSpeed=4
        )

    def reproduce(self, mates):
        targetMate = None
        for mate in mates:
            distance = self.position.distance_to(mate.position)
            if mate is not self and distance < self.property.detectionRange \
                and mate.property.matingDesireLevel >= 100:
                self.speed = 1
                self.direction = Vector2((mate.position - self.position)).normalize()
                targetMate = mate   
                break

        if targetMate is not None and distance < self.property.interactiveRange:
            self.speed = 0

            newPosition = self.position if random.randint(0, 1) == 0 else mate.position

            newCreature = Wolf(newPosition.x, newPosition.y)
        
            mates.add(newCreature)

            self.property.matingDesireLevel = 0
            mate.property.matingDesireLevel = 0
    