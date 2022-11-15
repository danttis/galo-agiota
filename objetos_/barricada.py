import pygame
import math
from plot.imagens import *


class Barricada(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = barricada_img
        self.rect = pygame.Rect(0, 0, 750, 500)
