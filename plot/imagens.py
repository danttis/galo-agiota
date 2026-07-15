import pygame

# Carrega todas as imagens existentes e novas

def carregar():
    imgs = {}
    try:
        imgs['menu_fundo'] = pygame.image.load("data/fundoM.png.png")
    except:
        imgs['menu_fundo'] = pygame.Surface((800, 600))
        imgs['menu_fundo'].fill((50, 50, 80))

    try:
        imgs['logo'] = pygame.image.load("data/logoJogo.png")
    except:
        imgs['logo'] = pygame.Surface((200, 100))
        imgs['logo'].fill((255, 0, 0))

    try:
        imgs['galo'] = pygame.image.load("data/galo.png")
    except:
        imgs['galo'] = pygame.Surface((64, 64))
        imgs['galo'].fill((255, 0, 0))

    try:
        imgs['capanga'] = pygame.image.load("data/capanga.png")
    except:
        imgs['capanga'] = pygame.Surface((64, 64))
        imgs['capanga'].fill((0, 255, 0))

    try:
        imgs['boss'] = pygame.image.load("data/boss.png")
    except:
        imgs['boss'] = pygame.Surface((100, 100))
        imgs['boss'].fill((255, 0, 255))

    try:
        imgs['bala'] = pygame.image.load("data/bala.png")
    except:
        imgs['bala'] = pygame.Surface((10, 4))
        imgs['bala'].fill((255, 255, 0))

    try:
        imgs['bala_boss'] = pygame.image.load("data/bala_boss.png")
    except:
        imgs['bala_boss'] = pygame.Surface((10, 4))
        imgs['bala_boss'].fill((255, 0, 0))

    try:
        imgs['vida'] = pygame.image.load("data/vida.png")
    except:
        imgs['vida'] = pygame.Surface((24, 24))
        imgs['vida'].fill((255, 0, 0))

    try:
        imgs['bolsa'] = pygame.image.load("data/bolsaD.png")
    except:
        imgs['bolsa'] = pygame.Surface((24, 24))
        imgs['bolsa'].fill((255, 215, 0))

    # Fundos de fase
    try:
        imgs['fase1'] = pygame.image.load("data/fundo_fase_1.png")
    except:
        imgs['fase1'] = pygame.Surface((800, 600))
        imgs['fase1'].fill((100, 150, 200))

    try:
        imgs['fase2'] = pygame.image.load("data/fundo_fase_2.png")
    except:
        imgs['fase2'] = pygame.Surface((800, 600))
        imgs['fase2'].fill((150, 100, 80))

    try:
        imgs['fase3'] = pygame.image.load("data/fundo_fase_3.png")
    except:
        imgs['fase3'] = pygame.Surface((800, 600))
        imgs['fase3'].fill((80, 50, 50))

    try:
        imgs['venceu'] = pygame.image.load("data/venceu.png")
    except:
        imgs['venceu'] = pygame.Surface((800, 600))
        imgs['venceu'].fill((0, 100, 0))

    try:
        imgs['funeral'] = pygame.image.load("data/funeral.png")
    except:
        imgs['funeral'] = pygame.Surface((800, 600))
        imgs['funeral'].fill((20, 20, 20))

    try:
        imgs['galo_inicio'] = pygame.image.load("data/galo_inicio.png")
    except:
        imgs['galo_inicio'] = imgs['galo']

    try:
        imgs['boss_inicio'] = pygame.image.load("data/boss_inicio.png")
    except:
        imgs['boss_inicio'] = imgs['boss']

    return imgs
