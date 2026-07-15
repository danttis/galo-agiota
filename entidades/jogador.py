import pygame
import time
from config import GRAVIDADE, VEL_PULO, VEL_MAX, VEL_CORRIDA, ATRITO, ACELERACAO, VIDAS_INICIAIS, MUNICAO_INICIAL, INVENCIVEL_TEMPO
from engine.fisica import aplicar_gravidade, resolver_colisao_plataforma
from entidades.projetil import Projetil, Suborno

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        self.imagem_original = pygame.transform.scale(imagem, (64, 64))
        self.imagem_esquerda = pygame.transform.flip(self.imagem_original, True, False)
        self.image = self.imagem_original
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.direcao = 1  # 1 direita, -1 esquerda
        self.no_chao = False
        self.vidas = VIDAS_INICIAIS
        self.municao = MUNICAO_INICIAL
        self.score = 0
        self.dinheiro = 1000
        self.invencivel = False
        self.tempo_invencivel = 0
        self.atirando = False
        self.tempo_tiro = 0
        self.morto = False

    def update(self, teclas, plataformas, tiros_group, subornos_group, tempo_atual):
        if self.morto:
            return

        # Invencibilidade
        if self.invencivel and tempo_atual - self.tempo_invencivel > INVENCIVEL_TEMPO:
            self.invencivel = False
            self.image.set_alpha(255)

        if self.invencivel:
            alpha = 255 if (pygame.time.get_ticks() // 100) % 2 == 0 else 100
            self.image.set_alpha(alpha)

        # Movimento horizontal
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.vel_x -= ACELERACAO
            self.direcao = -1
            self.image = self.imagem_esquerda
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.vel_x += ACELERACAO
            self.direcao = 1
            self.image = self.imagem_original
        else:
            self.vel_x *= ATRITO

        self.vel_x = max(-VEL_MAX, min(VEL_MAX, self.vel_x))
        self.rect.x += int(self.vel_x)

        # Colisao horizontal
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right
                self.vel_x = 0

        # Pulo
        if (teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_SPACE]) and self.no_chao:
            self.vel_y = VEL_PULO
            self.no_chao = False

        # Gravidade
        aplicar_gravidade(self)
        self.no_chao = resolver_colisao_plataforma(self, plataformas)

        # Tiro
        self.tempo_tiro -= 1
        if teclas[pygame.K_x] and self.tempo_tiro <= 0 and self.municao > 0:
            self.atirar(tiros_group)
            self.tempo_tiro = 12

        # Suborno
        if teclas[pygame.K_z] and self.tempo_tiro <= 0 and self.dinheiro >= Suborno.CUSTO:
            self.lancar_suborno(subornos_group, plataformas)
            self.tempo_tiro = 20
            self.dinheiro -= Suborno.CUSTO

        # Limita ao chao
        if self.rect.top > 700:
            self.morrer()

    def atirar(self, tiros_group):
        self.atirando = True
        offset_x = 30 if self.direcao == 1 else -30
        tiro = Projetil(self.rect.centerx + offset_x, self.rect.centery, self.direcao, velocidade=12, imagem=None)
        # Usa cor amarela para tiro do jogador (mesmo tamanho da bala do boss para alinhar)
        tiro.image = pygame.Surface((14, 6))
        tiro.image.fill((255, 255, 0))
        tiro.dano = 1
        tiros_group.add(tiro)
        self.municao -= 1

    def lancar_suborno(self, subornos_group, plataformas):
        offset_x = 20 if self.direcao == 1 else -20
        suborno = Suborno(self.rect.centerx + offset_x, self.rect.centery, self.direcao, plataformas)
        subornos_group.add(suborno)

    def tomar_dano(self, tempo_atual):
        if self.invencivel or self.morto:
            return False
        self.vidas -= 1
        self.invencivel = True
        self.tempo_invencivel = tempo_atual
        self.vel_y = -5
        self.vel_x = -self.direcao * 4
        if self.vidas <= 0:
            self.morrer()
        return True

    def morrer(self):
        self.morto = True
        self.vel_y = -8

    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.morto = False
        self.invencivel = True
        self.tempo_invencivel = pygame.time.get_ticks()
        self.vidas = VIDAS_INICIAIS
        self.municao = MUNICAO_INICIAL
