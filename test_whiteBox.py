from main import *
from fundos import *
from municao import Municao_boss
import pygame
from obj_animacao import Dinheiro
from obj_animacao import GaloAnimacao

#CAIXA BRANCA

def test_animacao(): #DIHEIRO NA TELA
	screen = pygame.set_mode(screenDimension)
	objeto = Dinheiro()
	objDinheiro = screen.blit(objeto)
	assert objDinheiro == True

def test_animacao2(): #GALO ANDANDO ATÉ FECHAR A TELA DE ANIMAÇÃO AUTOMATICA
	screen = pygame.set_mode(screenDimension)
	x = 600
	galorun = GaloAnimacao.update(x)
	assert galorun == False

def test_fundo(): #FUNDO GAME OVER
	fundo_gameOver = funeral()
	screen = display.set_mode(fundo_gameOver)
	fundo_Ok = screen.blit(screen, (0, 0))
	assert fundo_Ok == True

def test_fundo2(): #FUNDO MENU
	fundo_meNu = imagem_menu()
	screen = display.set_mode(fundo_meNu)
	fundo_Ok2 = screen.blit(screen, (0, 0))
	assert fundo_Ok2 == True

def test_minimal_pygame3(): #DISPAROS GALO PRINCIPAL
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_SPACE)
    wrap.send(None) # prime the coroutine
    test_press_space = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
	disparo = Municao()
    assert disparo==True