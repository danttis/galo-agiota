import pygame
import random
from config import GRAVIDADE, ALTURA
from engine.fisica import aplicar_gravidade, resolver_colisao_plataforma
from entidades.projetil import Projetil, Faca
from engine.particulas import criar_sangue, criar_penas

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, tipo='patrulha'):
        super().__init__()
        # A imagem original do capanga olha para a ESQUERDA
        img_original = pygame.transform.scale(imagem, (64, 64))
        self.imagem_esquerda = img_original
        self.imagem_direita = pygame.transform.flip(img_original, True, False)
        self.rect = self.imagem_esquerda.get_rect(topleft=(x, y))
        self.vel_x = random.choice([-1.5, 1.5])
        self.image = self.imagem_direita if self.vel_x > 0 else self.imagem_esquerda
        self.vel_y = 0
        self.no_chao = False
        self.tipo = tipo
        self.vida = 2
        self.morto = False
        self.subornado = False
        self.tempo_anim_morte = 0
        self.tempo_tiro = random.randint(30, 90)
        self.raio_visao = 300
        self.raio_ataque = 250

    def update(self, jogador, plataformas, tiros_group, particulas_group, inimigos_group=None):
        if self.morto:
            self.tempo_anim_morte -= 1
            self.vel_y += GRAVIDADE
            self.rect.y += int(self.vel_y)
            if self.tempo_anim_morte <= 0:
                self.kill()
            return

        # IA de subornado: persegue outros inimigos
        if self.subornado and inimigos_group:
            alvo = None
            menor_dist = float('inf')
            for ini in inimigos_group:
                if ini is self or ini.morto or getattr(ini, 'subornado', False):
                    continue
                # Nao ataca boss visitante nem boss real
                from entidades.boss import Boss, BossVisitante
                if isinstance(ini, (Boss, BossVisitante)):
                    continue
                dx = ini.rect.centerx - self.rect.centerx
                dy = ini.rect.centery - self.rect.centery
                d = (dx*dx + dy*dy) ** 0.5
                if d < menor_dist:
                    menor_dist = d
                    alvo = ini

            if alvo:
                if alvo.rect.centerx > self.rect.centerx + 10:
                    self.vel_x = 3
                    self.image = self.imagem_direita
                elif alvo.rect.centerx < self.rect.centerx - 10:
                    self.vel_x = -3
                    self.image = self.imagem_esquerda
                else:
                    self.vel_x = 0
            else:
                # Sem inimigos, fica perto do jogador como guarda-costas
                dx = jogador.rect.centerx - self.rect.centerx
                if dx > 80:
                    self.vel_x = 2
                    self.image = self.imagem_direita
                elif dx < -80:
                    self.vel_x = -2
                    self.image = self.imagem_esquerda
                else:
                    self.vel_x = 0
        else:
            # IA basica (inimigo normal)
            dist_x = jogador.rect.centerx - self.rect.centerx
            dist_y = jogador.rect.centery - self.rect.centery
            dist = (dist_x ** 2 + dist_y ** 2) ** 0.5

            if dist < self.raio_visao:
                if dist_x > 20:
                    self.vel_x = 1.5
                    self.image = self.imagem_direita
                elif dist_x < -20:
                    self.vel_x = -1.5
                    self.image = self.imagem_esquerda
                else:
                    self.vel_x = 0

                # Atira se estiver no raio de ataque
                if dist < self.raio_ataque:
                    self.tempo_tiro -= 1
                    if self.tempo_tiro <= 0:
                        self.atirar(jogador, tiros_group)
                        self.tempo_tiro = random.randint(60, 120)
            else:
                # Patrulha
                self.rect.x += int(self.vel_x)
                if random.random() < 0.01:
                    self.vel_x *= -1
                    self.image = self.imagem_direita if self.vel_x > 0 else self.imagem_esquerda

        # Gravidade e colisao
        self.rect.x += int(self.vel_x)
        aplicar_gravidade(self)
        self.no_chao = resolver_colisao_plataforma(self, plataformas)

        # Limita ao mundo
        if self.rect.left < 0 or self.rect.right > 4000:
            self.vel_x *= -1

        # Garante que a sprite sempre corresponde a direcao do movimento
        if self.vel_x > 0.1:
            self.image = self.imagem_direita
        elif self.vel_x < -0.1:
            self.image = self.imagem_esquerda

    def atirar(self, jogador, tiros_group):
        dir_x = 1 if jogador.rect.centerx > self.rect.centerx else -1
        self.image = self.imagem_direita if dir_x > 0 else self.imagem_esquerda
        faca = Faca(self.rect.centerx, self.rect.centery, dir_x, velocidade=6)
        tiros_group.add(faca)

    def subornar(self):
        """Capanga muda de lado: vira aliado verde."""
        if self.subornado or self.morto:
            return
        self.subornado = True
        self.vida = 4  # mais resistente como aliado
        # Overlay verde nas sprites
        overlay = pygame.Surface(self.imagem_esquerda.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 255, 100, 90))
        self.imagem_esquerda.blit(overlay, (0, 0))
        self.imagem_direita.blit(overlay, (0, 0))
        self.image = self.imagem_direita if self.vel_x >= 0 else self.imagem_esquerda

    def tomar_dano(self, dano, particulas_group):
        self.vida -= dano
        if self.vida <= 0:
            self.morrer(particulas_group)
        else:
            # Knockback
            self.vel_x = -self.vel_x * 2
            self.vel_y = -3

    def morrer(self, particulas_group):
        self.morto = True
        self.tempo_anim_morte = 30
        self.vel_y = -6
        self.vel_x = self.vel_x * 0.5
        criar_sangue(particulas_group, self.rect.centerx, self.rect.centery, 10)
        criar_penas(particulas_group, self.rect.centerx, self.rect.centery, 8)
