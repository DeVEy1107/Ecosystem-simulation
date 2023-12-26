import sys

import pygame

from constants import *
from worlds import World


class Game(object):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE)
        pygame.display.set_caption(GAME_NAME)

        self.clock = pygame.time.Clock()

        self.isRunning = True
        self.isPaused = False

        self.world = World()

        self.showWorldInfo = False

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    self.world.wolfs.displayInfo()
                    self.world.sheep.displayInfo()
                if event.key == pygame.K_p:
                    self.isPaused = not self.isPaused
                if event.key == pygame.K_r:
                    self.world.init()
                if event.key == pygame.K_TAB:
                    self.showWorldInfo = not self.showWorldInfo
                if event.key == pygame.K_z:
                    if self.world.timer.timeInterval > 1:
                        self.world.timer.timeInterval /= 2 
                if event.key == pygame.K_x:
                    if self.world.timer.timeInterval < 32:
                        self.world.timer.timeInterval *= 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseKeys = pygame.mouse.get_pressed()
                if mouseKeys[0]:
                    self.world.wolfs.add(*pygame.mouse.get_pos())
                elif mouseKeys[2]:
                    self.world.sheep.add(*pygame.mouse.get_pos())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.world.shift(0, WINDOW_MOVING_SPEED)
        if keys[pygame.K_DOWN]:
            self.world.shift(0, -WINDOW_MOVING_SPEED)
        if keys[pygame.K_LEFT]:
            self.world.shift(WINDOW_MOVING_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            self.world.shift(-WINDOW_MOVING_SPEED, 0)

    def update(self):
        self.world.update()
              
    def draw(self, screen):
        screen.fill(BACKGROUND)     
        self.world.draw(screen)

    def run(self):
        while self.isRunning:
            self.processEvents()
            if not self.isPaused:
                self.update()
            
            self.draw(self.screen)
            if self.showWorldInfo:
                self.world.drawWorldInfo()
            self.clock.tick(FPS)

            pygame.display.flip()

        pygame.quit()  


if __name__ == "__main__":
    game = Game()
    game.run()