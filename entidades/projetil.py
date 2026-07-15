import pygame
from engine.fisica import aplicar_gravidade, resolver_colisao_plataforma

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, velocidade=10, cor=(255, 255, 0), imagem=None):
        super().__init__()
        if imagem:
            self.image = imagem
            if direcao < 0:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.Surface((12, 6))
            self.image.fill(cor)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = velocidade if direcao > 0 else -velocidade
        self.dano = 1

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0 or self.rect.left > 4000:
            self.kill()

class Faca(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, velocidade=7):
        super().__init__()
        # Desenha uma faca simples
        base = pygame.Surface((20, 8), pygame.SRCALPHA)
        # Lamina
        pygame.draw.polygon(base, (200, 200, 210), [(0, 4), (14, 0), (14, 8)])
        # Cabo
        pygame.draw.rect(base, (100, 60, 30), (14, 2, 6, 4))
        # Borda
        pygame.draw.polygon(base, (150, 150, 160), [(0, 4), (14, 0), (14, 8)], 1)
        if direcao < 0:
            base = pygame.transform.flip(base, True, False)
        self.image_original = base
        self.image = base.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = velocidade if direcao > 0 else -velocidade
        self.vel_y = -4
        self.gravidade = 0.25
        self.angulo = 0
        self.dano = 2
        self.direcao = direcao

    def update(self):
        self.vel_y += self.gravidade
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.angulo += 8 * self.direcao
        centro = self.rect.center
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.rect = self.image.get_rect(center=centro)
        if self.rect.right < 0 or self.rect.left > 4000 or self.rect.top > 700:
            self.kill()


class Granada(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((50, 200, 50))
        pygame.draw.circle(self.image, (0, 100, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 5 if direcao > 0 else -5
        self.vel_y = -10
        self.gravidade = 0.4
        self.tempo = 60

    def update(self):
        self.vel_y += self.gravidade
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.tempo -= 1
        if self.tempo <= 0:
            self.kill()
        if self.rect.top > 600:
            self.kill()


class Suborno(pygame.sprite.Sprite):
    """Dinheiro que o Galo Agiota joga para subornar capangas."""
    CUSTO = 500

    def __init__(self, x, y, direcao, plataformas_group):
        super().__init__()
        self.image = pygame.Surface((28, 14), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (34, 139, 34), (0, 0, 28, 14), border_radius=2)
        pygame.draw.rect(self.image, (255, 215, 0), (0, 0, 28, 14), 2)
        try:
            f = pygame.font.SysFont("monospace", 10, bold=True)
            t = f.render("$", True, (255, 215, 0))
            self.image.blit(t, (10, 2))
        except:
            pass
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 6 if direcao > 0 else -6
        self.vel_y = -7
        self.gravidade = 0.35
        self.parado = False
        self.tempo_vida = 200
        self.plataformas = plataformas_group

    def update(self):
        if not self.parado:
            self.rect.x += int(self.vel_x)
            aplicar_gravidade(self)
            no_chao = resolver_colisao_plataforma(self, self.plataformas)
            if no_chao:
                self.parado = True
                self.vel_x = 0
                self.vel_y = 0
            if self.rect.top > 700:
                self.kill()
        else:
            self.tempo_vida -= 1
            alpha = 255 if (self.tempo_vida // 6) % 2 == 0 else 80
            self.image.set_alpha(alpha)
            if self.tempo_vida <= 0:
                self.kill()
