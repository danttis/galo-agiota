import pygame
from config import BRANCO, VERMELHO, VERDE, AMARELO, PRETO, LARGURA
from engine.texto import texto_com_borda

class HUD:
    def __init__(self, fonte_path=None):
        try:
            self.fonte = pygame.font.SysFont("Ubuntu Sans", 18, bold=True)
            self.fonte_grande = pygame.font.SysFont("Ubuntu Sans", 24, bold=True)
        except:
            self.fonte = pygame.font.SysFont("monospace", 18, bold=True)
            self.fonte_grande = pygame.font.SysFont("monospace", 24, bold=True)
        self.mensagem = ""
        self.tempo_mensagem = 0

    def mostrar_mensagem(self, texto, duracao=120):
        self.mensagem = texto
        self.tempo_mensagem = duracao

    def desenhar(self, tela, jogador, fase, boss=None):
        # Barra de vida
        cor_vida = VERDE if jogador.vidas > 1 else VERMELHO
        pygame.draw.rect(tela, PRETO, (10, 10, 154, 24))
        pygame.draw.rect(tela, cor_vida, (12, 12, 150 * (jogador.vidas / 3), 20))
        texto_vida = texto_com_borda(self.fonte, f"VIDA: {jogador.vidas}", BRANCO)
        tela.blit(texto_vida, (12, 12))

        # Municao
        cor_municao = AMARELO if jogador.municao > 10 else VERMELHO
        texto_municao = texto_com_borda(self.fonte, f"MUNICAO: {jogador.municao}", cor_municao)
        tela.blit(texto_municao, (10, 40))

        # Suborno
        tem_dinheiro = jogador.dinheiro >= 500
        cor_suborno = VERDE if tem_dinheiro else VERMELHO
        texto_suborno = texto_com_borda(self.fonte, f"SUBORNO: $500 [Z]", cor_suborno)
        tela.blit(texto_suborno, (10, 62))

        # Score / Dinheiro
        texto_score = texto_com_borda(self.fonte, f"SCORE: {jogador.score}", BRANCO)
        tela.blit(texto_score, (LARGURA - 200, 10))

        texto_dinheiro = texto_com_borda(self.fonte, f"COBRADO: ${jogador.dinheiro}", AMARELO)
        tela.blit(texto_dinheiro, (LARGURA - 200, 32))

        # Fase
        texto_fase = texto_com_borda(self.fonte, f"FASE: {fase}", BRANCO)
        tela.blit(texto_fase, (LARGURA // 2 - 40, 10))

        # Barra do Boss
        if boss and not boss.morto:
            pygame.draw.rect(tela, PRETO, (LARGURA//2 - 152, ALTURA - 40, 304, 24))
            pygame.draw.rect(tela, VERMELHO, (LARGURA//2 - 150, ALTURA - 38, 300 * (boss.vida / boss.vida_max), 20))
            texto_boss = texto_com_borda(self.fonte, "GALO DEVEDOR", BRANCO)
            tela.blit(texto_boss, (LARGURA//2 - 60, ALTURA - 38))

        # Mensagem flutuante
        if self.tempo_mensagem > 0:
            self.tempo_mensagem -= 1
            surf = texto_com_borda(self.fonte_grande, self.mensagem, AMARELO)
            rect = surf.get_rect(center=(LARGURA//2, ALTURA//2))
            tela.blit(surf, rect)

        # Controles
        texto_ctrl = texto_com_borda(self.fonte, "[A/D] Mover  [W/SPACE] Pular  [X] Atirar  [Z] Suborno", (200, 200, 200))
        tela.blit(texto_ctrl, (10, ALTURA - 25))

# Para compatibilidade com referencia a ALTURA no hud
from config import ALTURA
