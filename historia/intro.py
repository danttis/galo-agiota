import pygame
from config import BRANCO, PRETO, LARGURA, ALTURA
from engine.texto import texto_com_borda

class Intro:
    def __init__(self, tela, imagens):
        self.tela = tela
        self.imagens = imagens
        self.ativa = True
        self.pulada = False
        try:
            self.fonte_titulo = pygame.font.SysFont("Ubuntu Sans", 36, bold=True)
            self.fonte_texto = pygame.font.SysFont("Ubuntu Sans", 18, bold=True)
        except:
            self.fonte_titulo = pygame.font.SysFont("monospace", 36, bold=True)
            self.fonte_texto = pygame.font.SysFont("monospace", 18, bold=True)

        self.historia = [
            "A FAVELA DOS FRANGOS...",
            "",
            "O GALO AGIOTA era o mais respeitado",
            "cobrador de dividas do bairro.",
            "",
            "Mas um dia, o temivel GALO DEVEDOR",
            "que deve a METADE da cidade",
            "fugiu com seu exercito de capangas.",
            "",
            "Armado ate o bico, o Galo Agiota",
            "precisa atravessar territorio inimigo,",
            "cobrar cada centavo e fazer justica",
            "com as proprias esporas.",
            "",
            "NINGUEM foge do Galo Agiota."
        ]
        self.linha_atual = 0
        self.caractere_atual = 0
        self.tempo_anim = 0
        self.tempo_pisca = 0
        self.cor_titulo = (255, 215, 0)

    def update(self):
        self.tempo_anim += 1
        if self.tempo_anim % 3 == 0 and not self.pulada:
            self.caractere_atual += 1
            linha = self.historia[self.linha_atual]
            if self.caractere_atual > len(linha):
                self.caractere_atual = len(linha)
                if self.linha_atual < len(self.historia) - 1:
                    self.linha_atual += 1
                    self.caractere_atual = 0
                else:
                    # Espera um pouco e termina
                    if self.tempo_anim > len(self.historia) * 3 + 180:
                        self.ativa = False

    def desenhar(self):
        self.tela.fill(PRETO)

        # Titulo
        titulo = texto_com_borda(self.fonte_titulo, "GALO AGIOTA", self.cor_titulo)
        self.tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 30))

        # Sprites dramaticos
        galo_img = self.imagens.get('galo_inicio')
        if galo_img:
            galo_img = pygame.transform.scale(galo_img, (120, 120))
            self.tela.blit(galo_img, (100, ALTURA - 200))

        boss_img = self.imagens.get('boss_inicio')
        if boss_img:
            boss_img = pygame.transform.scale(boss_img, (140, 140))
            self.tela.blit(boss_img, (LARGURA - 260, ALTURA - 220))

        # Texto com efeito typewriter
        y = 120
        for i in range(self.linha_atual + 1):
            if i < len(self.historia):
                linha = self.historia[i]
                if i == self.linha_atual:
                    linha = linha[:self.caractere_atual]
                cor = self.cor_titulo if i == 0 else BRANCO
                texto = texto_com_borda(self.fonte_texto, linha, cor)
                self.tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
                y += 28

        # Pisca "Pressione E"
        self.tempo_pisca += 1
        if (self.tempo_pisca // 30) % 2 == 0:
            pular = texto_com_borda(self.fonte_texto, "PRESSIONE [E] PARA PULAR", (200, 200, 200))
            self.tela.blit(pular, (LARGURA//2 - pular.get_width()//2, ALTURA - 50))

    def evento(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.pulada = True
            self.ativa = False
