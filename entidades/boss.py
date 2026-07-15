import pygame
import random
from config import GRAVIDADE, ALTURA
from engine.fisica import aplicar_gravidade, resolver_colisao_plataforma
from entidades.projetil import Projetil
from engine.particulas import criar_explosao, criar_sangue

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem):
        super().__init__()
        # A imagem original do boss olha para a ESQUERDA
        img_original = pygame.transform.scale(imagem, (64, 64))
        self.imagem_esquerda = img_original
        self.imagem_direita = pygame.transform.flip(img_original, True, False)
        self.image = self.imagem_esquerda
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.vida_max = 30
        self.vida = self.vida_max
        self.fase = 1
        self.morto = False
        self.tempo_tiro = 0
        self.tempo_pulo = 0
        self.tempo_invoca = 0
        self.direcao = -1
        self.alvo_x = x
        self.estado = 'idle'
        self.tempo_estado = 0

    def update(self, jogador, plataformas, tiros_group, inimigos_group, particulas_group, capanga_img):
        if self.morto:
            self.vel_y += GRAVIDADE
            self.rect.y += int(self.vel_y)
            if self.rect.top > 700:
                self.kill()
            return

        if self.vida <= self.vida_max * 0.3:
            self.fase = 3
        elif self.vida <= self.vida_max * 0.6:
            self.fase = 2

        self.tempo_tiro -= 1
        self.tempo_pulo -= 1
        self.tempo_invoca -= 1
        self.tempo_estado -= 1

        dist_x = jogador.rect.centerx - self.rect.centerx
        dist = abs(dist_x)

        if self.tempo_estado <= 0:
            self.estado = random.choice(['perseguir', 'atirar', 'pular', 'invocar'])
            self.tempo_estado = random.randint(60, 120)

        if self.estado == 'perseguir':
            if dist_x > 50:
                self.vel_x = 2 + self.fase
                self.image = self.imagem_direita
            elif dist_x < -50:
                self.vel_x = -(2 + self.fase)
                self.image = self.imagem_esquerda
            else:
                self.vel_x = 0
        elif self.estado == 'atirar':
            self.vel_x *= 0.9
            if self.tempo_tiro <= 0:
                self._atirar_multiplo(jogador, tiros_group)
                self.tempo_tiro = max(20, 60 - self.fase * 15)
        elif self.estado == 'pular' and self.no_chao and self.tempo_pulo <= 0:
            self.vel_y = -16
            self.no_chao = False
            self.tempo_pulo = 120
            if dist_x > 0:
                self.vel_x = 5
                self.image = self.imagem_direita
            else:
                self.vel_x = -5
                self.image = self.imagem_esquerda
        elif self.estado == 'invocar' and self.tempo_invoca <= 0:
            self._invocar_capangas(inimigos_group, capanga_img)
            self.tempo_invoca = 180
            self.estado = 'perseguir'

        self.rect.x += int(self.vel_x)
        aplicar_gravidade(self)
        self.no_chao = resolver_colisao_plataforma(self, plataformas)

    def _atirar_multiplo(self, jogador, tiros_group):
        direcao = 1 if jogador.rect.centerx > self.rect.centerx else -1
        self.image = self.imagem_direita if direcao > 0 else self.imagem_esquerda
        num_tiros = random.randint(1, 3)
        for i in range(num_tiros):
            offset_y = (i - 1) * 12
            tiro = Projetil(self.rect.centerx, self.rect.centery + offset_y, direcao, velocidade=8, cor=(255, 0, 0))
            tiro.image = pygame.Surface((14, 6))
            tiro.image.fill((255, 80, 80))
            tiro.dano = 1
            tiros_group.add(tiro)

    def _invocar_capangas(self, inimigos_group, capanga_img):
        from entidades.inimigo import Inimigo
        for _ in range(2):
            x = self.rect.centerx + random.choice([-200, 200])
            cap = Inimigo(x, 400, capanga_img)
            inimigos_group.add(cap)

    def tomar_dano(self, dano, particulas_group):
        self.vida -= dano
        criar_sangue(particulas_group, self.rect.centerx, self.rect.centery, 5)
        if self.vida <= 0:
            self.morrer(particulas_group)

    def morrer(self, particulas_group):
        self.morto = True
        self.vel_y = -10
        criar_explosao(particulas_group, self.rect.centerx, self.rect.centery, quantidade=30)
        criar_sangue(particulas_group, self.rect.centerx, self.rect.centery, 20)


class BossVisitante(pygame.sprite.Sprite):
    """O Galo Devedor aparece pelo lado direito no CHAO, da 1-3 tiros sequenciais e foge."""
    def __init__(self, x, y, imagem):
        super().__init__()
        img_original = pygame.transform.scale(imagem, (64, 64))
        self.imagem_esquerda = img_original
        self.imagem_direita = pygame.transform.flip(img_original, True, False)
        self.image = self.imagem_esquerda
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.morto = False
        self.estado = 'entrando'
        self.tiros_restantes = random.randint(1, 3)
        self.tempo_tiro = 0
        self.tempo_espera = 90  # ~1.5 segundos entre tiros
        self.tempo_sem_chao = 0

    def update(self, jogador, plataformas, tiros_group, inimigos_group, particulas_group, capanga_img):
        if self.morto:
            self.kill()
            return

        # Aplica gravidade e colisao primeiro (respeita as regras do jogo)
        self.rect.x += int(self.vel_x)
        aplicar_gravidade(self)
        self.no_chao = resolver_colisao_plataforma(self, plataformas)

        # Protecao: se caiu em buraco, foge apos um tempo
        if not self.no_chao:
            self.tempo_sem_chao += 1
            if self.tempo_sem_chao > 60 and self.rect.top > ALTURA:
                self.kill()
                return
        else:
            self.tempo_sem_chao = 0

        if self.estado == 'entrando':
            self.vel_x = -6
            self.image = self.imagem_esquerda
            # Para perto do jogador, mantendo distancia de seguranca
            alvo = jogador.rect.x + random.randint(250, 450)
            if self.rect.x <= alvo:
                self.estado = 'atirando'
                self.vel_x = 0
                self.tempo_tiro = 40
            return

        if self.estado == 'saindo':
            self.vel_x = 8
            self.image = self.imagem_direita
            if self.rect.left > 4500:
                self.kill()
            return

        # Estado 'atirando' — fica PARADO no chao, olha pro jogador e atira
        dist_x = jogador.rect.centerx - self.rect.centerx
        if dist_x > 0:
            self.image = self.imagem_direita
        else:
            self.image = self.imagem_esquerda
        self.vel_x = 0

        self.tempo_tiro -= 1
        if self.tempo_tiro <= 0:
            if self.tiros_restantes > 0:
                self._atirar_uma_vez(jogador, tiros_group)
                self.tiros_restantes -= 1
                self.tempo_tiro = self.tempo_espera
            else:
                self.estado = 'saindo'
                criar_explosao(particulas_group, self.rect.centerx, self.rect.centery, 5)

    def _atirar_uma_vez(self, jogador, tiros_group):
        direcao = 1 if jogador.rect.centerx > self.rect.centerx else -1
        self.image = self.imagem_direita if direcao > 0 else self.imagem_esquerda
        # Mesma altura do jogador (centery) para as balas colidirem no ar
        tiro = Projetil(self.rect.centerx, self.rect.centery, direcao, velocidade=10, cor=(255, 0, 0))
        tiro.image = pygame.Surface((14, 6))
        tiro.image.fill((255, 50, 50))
        tiros_group.add(tiro)

    def tomar_dano(self, dano, particulas_group):
        criar_sangue(particulas_group, self.rect.centerx, self.rect.centery, 3)
        self.vel_x = -2

    def morrer(self, particulas_group):
        pass
