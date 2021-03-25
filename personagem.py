import pygame
import math
class Persona(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image=pygame.image.load("data/galotest.png")
        self.image=pygame.transform.scale(self.image,[100,100])
        self.rect=pygame.Rect(124,263,10,10)

    def update(self, *args, **kwargs):
        # LOGICA DO PERSONAGEM

        #Pega qual tecla ta sendo clicada
        keyMOVI=pygame.key.get_pressed()
        # Movimentação pra cima e pra baixo
        if keyMOVI[pygame.K_DOWN]:
            self.rect.y +=5
        elif keyMOVI[pygame.K_UP]:
            self.rect.y -=5
        #Tecla para disparar
        if keyMOVI[pygame.K_SPACE]:
            self.rect.x += 5
