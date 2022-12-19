import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)