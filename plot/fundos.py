from ações.cabeçarios import *

#funções que plota(exibe) os fundos no game,

screenDimension=(750,500)
pygame.display.set_caption("Galo Agiota 1.0")
screen=pygame.display.set_mode(screenDimension, 0, 32)
pygame.display.set_icon(screen)


def fundos_menu():
    Menu_fundo
    Menu_fundo.get_rect()
    screen.blit(Menu_fundo,(0, 0))

def imagem_menu():
    imagemMenu
    imagemMenu.get_rect()
    screen.blit(imagemMenu, (135, 50))


def fundo_fase1():
    fase_1
    fase_1.get_rect()
    screen.blit(fase_1,(0, 0))

def fundo_fase2():
    fase_2
    fase_2.get_rect()
    screen.blit(fase_2,(0, 0))

def fundo_fase3():
    fase_3
    fase_3.get_rect()
    screen.blit(fase_3,(0, 0))

def fundo_fase4():
    fase_4
    fase_4.get_rect()
    screen.blit(fase_4,(0, 0))

def funeral():
    funeral_img
    funeral_img.get_rect()
    screen.blit(funeral_img, (0, 0))

