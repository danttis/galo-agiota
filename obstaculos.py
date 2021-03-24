import pygame
import math
import random

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load("data/galo-preto-em-um-branco-2375372.jpg")
        self.image = pygame.transform.scale(self.image, [100, 100])
        self.rect = pygame.Rect(50, 50, 40, 40)

        self.rect.x = 500 + random.randint(1, 250)
        self.rect.y = random.randint(1, 420)

        self.speed = 5

    def update(self, *args):
        self.rect.x -= self.speed