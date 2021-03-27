import pygame
import math
class Persona(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image=pygame.image.load("data/galo.png")
        self.image=pygame.transform.scale(self.image,[100,100])
        self.rect=pygame.Rect(124,263,10,10)

        #O que vai dar "Movimento" ao personagem, a física em sí
        self.speed = 0
        self.acceleration = 0.1
    def update(self, *args, **kwargs):
        # LOGICA DO PERSONAGEM

        #Pega qual tecla ta sendo clicada
        keyMOVI=pygame.key.get_pressed()
        # Movimentação pra cima e pra baixo
        if keyMOVI[pygame.K_DOWN]:
            self.speed +=self.acceleration
        elif keyMOVI[pygame.K_UP]:
            self.speed -=self.acceleration
        else:
            self.speed *=0.93

        self.rect.y+=self.speed

        #NÃO PERMITIR QUE ELE PASSE DA PARTE DE CIMA OU BAIXO
        if self.rect.top<0:
            self.rect.top=0
            self.speed = 0
        elif self.rect.bottom>400:
            self.rect.bottom = 400
            self.speed = 0

