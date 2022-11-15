#TESTE DE CAIXA PRETA ------------------------------------
import pygame
import main

def pygame_wrapper(coro):
    yield from coro


#TESTA A TECLA QUE SAI DO JOGO (INTRO)
def test_minimal_pygame():
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_s)
    wrap.send(None) # prime the coroutine
    test_press_s = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_s})
    assert test_press_s==pygame.quit() and exit(0)

#TESTA A TECLA S QUE SAI (MENU)
def test_minimal_pygame2():
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_q)
    wrap.send(None) # prime the coroutine
    test_press_q = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_q})
    assert test_press_q==pygame.quit() and exit(0)



#TESTA A TECLA QUE ATIRA
def test_minimal_pygame3():
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_SPACE)
    wrap.send(None) # prime the coroutine
    test_press_space = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    assert test_press_space==balas<20


#TESTA A TECLA QUE PULA DE FASE
def test_minimal_pygame4():
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_j)
    wrap.send(None) # prime the coroutine
    test_press_j = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_j})
    assert test_press_j==fase>1

#TESTA O CLIQUE NO C NA TELA DE VITÓRIA E PERDA
def test_minimal_pygame5():
    wrap = pygame_wrapper(pygame.KEYDOWN==pygame.K_c)
    wrap.send(None) # prime the coroutine
    test_press_c = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_c})
    assert test_press_c==(fase==1)




#TESTE DE CAIXA PRETA ------------------------------------