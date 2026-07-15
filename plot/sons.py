import pygame

pygame.mixer.init()

def carregar():
    sons = {}
    arquivos = {
        'menu': 'data/background_menu.wav',
        'fase1': 'data/background_fase1.wav',
        'fase2': 'data/background_fase2.wav',
        'fase3': 'data/background_fase3.wav',
        'tiro': 'data/tiro.wav',
        'morreu': 'data/morreu.wav',
        'dano': 'data/dano.wav',
        'perdeu_vida': 'data/perdeu_vida.wav',
    }
    for nome, path in arquivos.items():
        try:
            sons[nome] = pygame.mixer.Sound(path)
        except:
            sons[nome] = None
    return sons
