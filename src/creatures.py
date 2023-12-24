import random

import pygame

from pygame import Vector2

from constants import *
from misc import Timer, SpriteSheet, SpriteAnimaition, SpriteInfoLabel

class Property(object):
    def __init__(self, 
                 hungerLevel=HUNGER_LEVEL, 
                 hungerSpeed=HUNGER_SPEED,
                 matingDesireLevel=MATING_DESIRE_LEVEL,
                 matingDesireSpeed=MATING_DESIRE_SPEED, 
                 matingDesireThreshold=MATING_DESIRE_THRESHOLD, 
                 speed=SPEED, 
                 detectionRange=DETECTION_RANGE, 
                 interactiveRange=INTERACTIVE_RANGE, 
                 towardFoodSpeed=TOWARD_FOOD_SPEED,
                 foodAmount=FOOD_AMOUNT):
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

class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, filepath):
        super().__init__()

        self.size = TILE_SIZE
        self.filepath = filepath
        self.spriteAnimation = SpriteAnimaition(filepath, self.size)
        self.rect = self.spriteAnimation.getImage().get_rect(topleft=(x, y))

        self.timeCounter = 0
        self.timer = Timer(TIME_INTERVAL)

        self.position = Vector2(self.rect.centerx, self.rect.centery)
        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        self.property = Property()

        self.speed = random.randint(self.property.speed - 1, self.property.speed + 1)
        self.changeDirectionTimer = random.randint(30, 60)

        self.infoLabel = SpriteInfoLabel(self)

        self.totalEaten = 0

    def avoidZeroVector(self, position1, position2):
        distance = position1.distance_to(position2)
        if distance == 0:
            return Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        else:
            return Vector2((position1 - position2)).normalize()

    def move(self):
        self.changeDirectionTimer -= 1
        if self.changeDirectionTimer <= 0:
            self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.changeDirectionTimer = random.randint(10, 30) 
            self.speed = self.property.speed
        
    def reproduce(self, mates):
        targetMate = None
        for mate in mates:
            distance = self.position.distance_to(mate.position)
            if mate is not self and distance < self.property.detectionRange \
                and mate.property.matingDesireLevel >= 100:
                self.speed = 1
                self.direction = self.avoidZeroVector(mate.position, self.position)
                targetMate = mate   
                break

        if targetMate is not None and distance < self.property.interactiveRange:
            self.speed = 0

            newPosition = self.rect if random.randint(0, 1) == 0 else mate.rect

            newCreature = self.__class__(newPosition.centerx, newPosition.centery)
        
            mates.add(newCreature)

            self.property.matingDesireLevel = 0
            mate.property.matingDesireLevel = 0

    def seekingFood(self, foods):
        for food in foods:
            distance = self.position.distance_to(food.position)
            if distance < self.property.detectionRange:
                self.speed = self.property.towarfFoodSpeed
                self.direction = self.avoidZeroVector(food.position, self.position)

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
        if self.timer.time % CREATURE_PROPERTY_UPDATE_TIME == 0:
            self.property.hungerLevel -= self.property.hungerSpeed
            if self.property.matingDesireLevel < 100:
                self.property.matingDesireLevel += self.property.matingDesireSpeed
            else:
                self.property.matingDesireLevel = 100 

        if self.property.hungerLevel < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.spriteAnimation.getImage(), self.rect)

    def shift(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.position.x = self.rect.centerx 
        self.position.y = self.rect.centery


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.property = Property(foodAmount=30)
        self.spriteSheet = SpriteSheet(GRASS_IMAGE_PATH)
        self.image = self.spriteSheet.imageAt((80, 112, 16, 16))
        self.image = pygame.transform.scale(self.image, (int(TILE_SIZE), int(TILE_SIZE)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = Vector2(self.rect.centerx, self.rect.centery)
        self.timer = Timer(TIME_INTERVAL)

    def update(self):
        if self.timer.time % 30 == 0:
            self.kill()
        self.timer.update()

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
            matingDesireThreshold=500,
            detectionRange=100,
            foodAmount=60,
            towardFoodSpeed=2.5
        )
        
    def escape(self, predators):
        for predator in predators:
            distance = self.position.distance_to(predator.position)
            if distance <= self.property.detectionRange:
                self.speed = 1.8 * self.property.speed
                self.direction = self.avoidZeroVector(self.position, predator.position)

    def update(self, foods, mates, predators, terrains):
        self.spriteAnimation.update()

        if self.timer.tick():
            self.move()
            self.seekingFood(foods)
            if self.property.matingDesireLevel >= self.property.matingDesireThreshold:
                self.reproduce(mates)
            self.escape(predators)
            self.detectTerrain(terrains.waterTiles)

            self.position += self.direction * self.speed
            self.rect.center = self.position

            self.propertyUpdate()

        self.timer.update()
        self.infoLabel.update()
        

class Wolf(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, WOLF_IMAGE_PATH)

        self.property = Property(
            hungerLevel=1000,
            speed=3,
            detectionRange=170,
            towardFoodSpeed=4
        )
    
    def update(self, foods, mates, terrains):
        self.spriteAnimation.update()

        if self.timer.tick():
            self.move()
            self.seekingFood(foods)
            if self.property.matingDesireLevel >= self.property.matingDesireThreshold:
                self.reproduce(mates)
            self.detectTerrain(terrains.waterTiles)

            self.position += self.direction * self.speed
            self.rect.center = self.position

            self.propertyUpdate()

        self.timer.update()
        self.infoLabel.update()