import sys
import pygame

class UI(object):
    def __init__(self, screen):
        self.screen = screen

        self.buttonRect = pygame.Rect(50, 50, 100, 50)
    
        self.uiHidden = True

    def toggleVisibility(self):
        self.uiHidden = not self.uiHidden
    
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button1_rect.collidepoint(event.pos):
                        print("Button 1 clicked")
                    
    def draw(self):
        if not self.uiHidden:
            pygame.draw.rect(self.screen, (255, 0, 0), self.buttonRect)