import pygame
from pygame.locals import *
from obstaculos import Obstaculos
import random


##inica o pygame e suas dependências
pygame.init()
pygame.font.init()
##Define e cria a tela do game
screenDimension=(750,500)
screen=pygame.display.set_mode(screenDimension, 0, 32)
##Define variáveis com valores de cor ou coordenada
azul=(108,194,236)
branco=(255,255,255)
ret=pygame.Rect(10,10,10,10)

# OBJETOS
objectGroup = pygame.sprite.Group()

timer = 0
clock = pygame.time.Clock()

# MÚSICA DO MENU

while True:
    clock.tick(60)

    pygame.display.flip()
    screen.fill(0)
    ##Eventos do game
    for event in pygame.event.get():
        ##Quando aperta o X ele exita o pygame
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit(0)
        ##Movimentação do personagem
        ##Allan Vai organizar direito em classes, e modificar o necessário

        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                ret.move_ip(-20,0)
            if event.key == pygame.K_DOWN:
                ret.move_ip(0, 20)
            if event.key == pygame.K_RIGHT:
                ret.move_ip(20,0)
            if event.key == pygame.K_UP:
                ret.move_ip(0,-20)

    player = pygame.Rect(50, 50, 100, 100)
    pygame.draw.rect(screen, azul, ret)


    ##Obstaculos que vem na tela, os galos
    objectGroup.update()

    timer += 1
    if timer > 30:
        timer = 0
        if random.random() < 0.3:
            newObstaculos = Obstaculos(objectGroup)

    objectGroup.draw(screen)

    pygame.display.update()







