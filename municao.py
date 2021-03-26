import pygame
import math
import random
class Municao(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load("data/bala.png")
        self.image = pygame.transform.scale(self.image, [15, 6])
        self.rect=pygame.Rect(124,263,-165,-75)

        #Velocidade na qual sai da nave e atravessa a tela
        self.speed = 4

    def update(self, *args):
        self.rect.x += self.speed
        #Quando passa da tela ele é excluido
        if self.rect.left>750:
            self.kill()