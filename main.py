import pygame
from pygame.locals import *
from obstaculos import Obstaculos
def inicia():
    base=pygame.Rect(45,10,400,400)
    botao = pygame.Rect(90, 300, 125, 50)
    botao2 = pygame.Rect(265, 300, 125, 50)
    pygame.draw.rect(screen, branco, base)
    pygame.draw.rect(screen, azul, botao)
    pygame.draw.rect(screen, azul, botao2)
    pygame.draw.circle(screen, azul, (90, 325), 25)
    pygame.draw.circle(screen, azul, (210, 325), 25)
    pygame.draw.circle(screen, azul, (265, 325), 25)
    pygame.draw.circle(screen, azul, (395, 325), 25)

    fonte_padrao = pygame.font.get_default_font()
    textobotao=pygame.font.SysFont(fonte_padrao, 45)
    text=textobotao.render("INICIAR", 1, 1)
    screen.blit(text,(95,310))
    text2 = textobotao.render("SAIR", 1, 1)
    screen.blit(text2, (290, 310))
    principal = textobotao.render("RINHA DE GALO", 1, 1)
    screen.blit(principal, (125, 50))
    """imagem=pygame.image.load("./data/algumaimagem.png")
    redim = pygame.transform.smoothscale(imagem, (100,150))
    screen.blit(redim, (200, 100))"""


pygame.init()
pygame.font.init()
screenDimension=(500,500)
screen=pygame.display.set_mode(screenDimension, 0, 32)
azul=(108,194,236)
branco=(255,255,255)
ret=pygame.Rect(10,10,10,10)

# OBJETOS
objectGroup = pygame.sprite.Group()

obs1 = Obstaculos(objectGroup)
obs2 = Obstaculos(objectGroup)
obs3 = Obstaculos(objectGroup)

clock = pygame.time.Clock()

# MÚSICA DO MENU

while True:
    clock.tick(60)

    pygame.display.flip()
    screen.fill(0)
    inicia()
    ##Eventos do game
    for event in pygame.event.get():
        ##Quando aperta o X ele exita o pygame
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit(0)
        ##Movimentação do personagem

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

    objectGroup.update()
    objectGroup.draw(screen)

    pygame.display.update()







