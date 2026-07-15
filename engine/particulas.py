import pygame
import random

class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, velocidade, vida, tamanho, gravidade=0.2):
        super().__init__()
        self.image = pygame.Surface((tamanho, tamanho))
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.uniform(-velocidade, velocidade)
        self.vel_y = random.uniform(-velocidade, 0)
        self.vida = vida
        self.vida_max = vida
        self.gravidade = gravidade

    def update(self):
        self.vel_y += self.gravidade
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.vida / self.vida_max))
            self.image.set_alpha(alpha)

class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y, raio=30):
        super().__init__()
        self.x = x
        self.y = y
        self.raio = 0
        self.raio_max = raio
        self.vida = 15
        self.image = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.raio += self.raio_max / 15
        self.vida -= 1
        if self.vida <= 0:
            self.kill()
            return
        self.image = pygame.Surface((int(self.raio_max*2), int(self.raio_max*2)), pygame.SRCALPHA)
        alpha = int(255 * (self.vida / 15))
        pygame.draw.circle(self.image, (255, 200, 50, alpha), (int(self.raio_max), int(self.raio_max)), int(self.raio))
        pygame.draw.circle(self.image, (255, 50, 0, alpha), (int(self.raio_max), int(self.raio_max)), int(self.raio * 0.7))
        self.rect = self.image.get_rect(center=(self.x, self.y))

def criar_explosao(grupo, x, y, quantidade=10):
    grupo.add(Explosao(x, y))
    for _ in range(quantidade):
        cor = random.choice([(255, 200, 50), (255, 100, 0), (200, 50, 0)])
        grupo.add(Particula(x, y, cor, 4, random.randint(20, 40), random.randint(3, 6), gravidade=0.1))

def criar_sangue(grupo, x, y, quantidade=8):
    for _ in range(quantidade):
        cor = random.choice([(180, 30, 30), (200, 50, 50), (150, 20, 20)])
        grupo.add(Particula(x, y, cor, 3, random.randint(15, 30), random.randint(3, 5), gravidade=0.3))

def criar_penas(grupo, x, y, quantidade=6):
    for _ in range(quantidade):
        cor = random.choice([(255, 255, 255), (240, 240, 240), (200, 200, 200)])
        grupo.add(Particula(x, y, cor, 2, random.randint(20, 35), random.randint(4, 7), gravidade=0.15))
