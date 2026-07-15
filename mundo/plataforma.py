import pygame
from config import VERDE, PRETO

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor=None, tipo='chao'):
        super().__init__()
        self.cor = cor or VERDE
        self.tipo = tipo
        self.image = pygame.Surface((largura, altura))
        self.image.fill(self.cor)

        # Textura de tijolo/concreto
        if tipo == 'chao':
            # Linhas horizontais
            for i in range(0, largura, 40):
                pygame.draw.line(self.image, (self.cor[0]-20, self.cor[1]-20, self.cor[2]-20), (i, 0), (i, altura), 2)
            for j in range(0, altura, 20):
                pygame.draw.line(self.image, (self.cor[0]-20, self.cor[1]-20, self.cor[2]-20), (0, j), (largura, j), 2)
            # Borda superior mais clara
            pygame.draw.line(self.image, (min(255, self.cor[0]+30), min(255, self.cor[1]+30), min(255, self.cor[2]+30)), (0, 0), (largura, 0), 3)
            # Borda inferior mais escura
            pygame.draw.line(self.image, (max(0, self.cor[0]-40), max(0, self.cor[1]-40), max(0, self.cor[2]-40)), (0, altura-2), (largura, altura-2), 3)
        elif tipo == 'plataforma':
            pygame.draw.rect(self.image, (self.cor[0]-30, self.cor[1]-30, self.cor[2]-30), (0, 0, largura, 6))
            pygame.draw.rect(self.image, PRETO, (0, 0, largura, altura), 2)
        else:
            pygame.draw.rect(self.image, PRETO, (0, 0, largura, altura), 2)

        self.rect = self.image.get_rect(topleft=(x, y))

class Caixa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((139, 69, 19))
        # Detalhes da caixa
        pygame.draw.rect(self.image, (100, 50, 10), (0, 0, 40, 40), 3)
        pygame.draw.line(self.image, (80, 40, 0), (10, 10), (30, 30), 2)
        pygame.draw.line(self.image, (80, 40, 0), (30, 10), (10, 30), 2)
        pygame.draw.rect(self.image, PRETO, (0, 0, 40, 40), 2)
        self.rect = self.image.get_rect(topleft=(x, y))

class Espinho(pygame.sprite.Sprite):
    """Espinhos no chão dos buracos - insta-kill"""
    def __init__(self, x, y, largura):
        super().__init__()
        self.image = pygame.Surface((largura, 40))
        self.image.fill((40, 40, 40))  # Fundo escuro
        # Desenha os espinhos
        for i in range(0, largura, 20):
            pontos = [(i, 40), (i+10, 0), (i+20, 40)]
            pygame.draw.polygon(self.image, (200, 50, 50), pontos)
            pygame.draw.polygon(self.image, PRETO, pontos, 1)
        self.rect = self.image.get_rect(topleft=(x, y))
