from ações.cabeçarios import *
pygame.init()
pygame.font.init()
pygame.mixer.init()

# CARREGANDO TODAS AS MÚSICAS USADAS NO JOGO

menu = pygame.mixer.Sound("data/background_menu.wav")
animacao = pygame.mixer.Sound("data/animacao.wav")
fase1 = pygame.mixer.Sound("data/background_fase1.wav")
fase2 = pygame.mixer.Sound("data/background_fase2.wav")
fase3 = pygame.mixer.Sound("data/background_fase3.wav")


# SONS DE AÇÕES
tiro = pygame.mixer.Sound("data/tiro.wav")
morreu = pygame.mixer.Sound("data/morreu.wav")
dano = pygame.mixer.Sound("data/dano.wav")
perdeu_vida = pygame.mixer.Sound("data/perdeu_vida.wav")