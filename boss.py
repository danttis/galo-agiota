import pygame
import math
import random
from municao import Municao_boss

class Boss(pygame.sprite.Sprite):
    # DEFININDO O TAMANHO E APARENCIA DO BOSS
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image=pygame.image.load("data/boss.png")
        self.image=pygame.transform.scale(self.image,[100,100])
        self.rect=pygame.Rect(50,50,40,40)

        # APARECE DE UMA POSIÇÃO ALEATORIA NO EIXO Y
        self.rect.y = random.randint(1, 420)
        self.speed = 0

    def update(self, *args):
        # MOVIMENTO DO BOSS NA TELA
        self.speed += 0.01
        self.rect.x = 750 - math.sin(self.speed) * 100
        if self.rect.left > 750:
            self.rect.y = random.randint(1, 420)

    def para(self, *args):
        self.kill()

