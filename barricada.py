import pygame
import math


class Barricada(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load("data/barricada.png")
        self.rect = pygame.Rect(0, 0, 750, 500)
