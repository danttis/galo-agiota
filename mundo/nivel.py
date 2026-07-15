import pygame
from mundo.plataforma import Plataforma, Caixa, Espinho
from config import LARGURA_NIVEL, ALTURA

class Nivel:
    def __init__(self, numero):
        self.numero = numero
        self.plataformas = pygame.sprite.Group()
        self.espinhos = pygame.sprite.Group()
        self.inimigos_spawns = []
        self.checkpoint_x = 200
        self.fim_x = LARGURA_NIVEL - 300
        self.gerar()

    def gerar(self):
        if self.numero == 1:
            self._gerar_fase1()
        elif self.numero == 2:
            self._gerar_fase2()
        elif self.numero == 3:
            self._gerar_fase3()
        elif self.numero == 4:
            self._gerar_fase4()
        elif self.numero == 5:
            self._gerar_fase5()
        else:
            self._gerar_fase3()

    def _gerar_fase1(self):
        # Chao base com BURACOS visiveis (entre 1500-1600 e 2800-3000)
        self.plataformas.add(Plataforma(0, 520, 1500, 80, tipo='chao'))
        self.plataformas.add(Plataforma(1600, 520, 1200, 80, tipo='chao'))
        self.plataformas.add(Plataforma(3000, 520, 1000, 80, tipo='chao'))

        # Espinhos nos buracos
        self.espinhos.add(Espinho(1500, 560, 100))
        self.espinhos.add(Espinho(2800, 560, 200))

        # Plataformas elevadas
        self.plataformas.add(Plataforma(400, 400, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(700, 350, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1000, 420, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1800, 400, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2200, 350, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2500, 420, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3400, 400, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3700, 350, 150, 20, tipo='plataforma'))

        # Caixas
        self.plataformas.add(Caixa(550, 480))
        self.plataformas.add(Caixa(1950, 480))
        self.plataformas.add(Caixa(3550, 480))

        self.inimigos_spawns = [
            (600, 450), (900, 450), (1200, 450), (1500, 450),
            (2000, 450), (2300, 450), (2600, 450), (2900, 450),
            (3200, 450), (3500, 450), (3800, 450)
        ]
        self.checkpoint_x = 1500
        self.fim_x = 3900

    def _gerar_fase2(self):
        # Galinheiro industrial com mais buracos
        self.plataformas.add(Plataforma(0, 520, 1000, 80, tipo='chao'))
        self.plataformas.add(Plataforma(1100, 520, 1000, 80, tipo='chao'))
        self.plataformas.add(Plataforma(2300, 520, 800, 80, tipo='chao'))
        self.plataformas.add(Plataforma(3300, 520, 700, 80, tipo='chao'))

        # Buracos
        self.espinhos.add(Espinho(1000, 560, 100))
        self.espinhos.add(Espinho(2200, 560, 100))
        self.espinhos.add(Espinho(3200, 560, 100))

        # Andares
        self.plataformas.add(Plataforma(300, 400, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(500, 300, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(800, 380, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1300, 350, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1500, 280, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1800, 380, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2500, 400, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2700, 300, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3000, 380, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3500, 350, 120, 20, tipo='plataforma'))

        # Caixas
        self.plataformas.add(Caixa(750, 480))
        self.plataformas.add(Caixa(1600, 480))
        self.plataformas.add(Caixa(2900, 480))

        self.inimigos_spawns = [
            (500, 450), (800, 450), (1400, 450), (1700, 450),
            (2000, 450), (2600, 450), (2800, 450), (3100, 450),
            (3600, 450), (3800, 450)
        ]
        self.checkpoint_x = 1700
        self.fim_x = 3900

    def _gerar_fase3(self):
        # Arena do boss - chao amplo
        self.plataformas.add(Plataforma(0, 520, 4000, 80, tipo='chao'))
        # Plataformas laterais para escapar
        self.plataformas.add(Plataforma(500, 400, 200, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3000, 400, 200, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1500, 350, 200, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2500, 350, 200, 20, tipo='plataforma'))

        self.inimigos_spawns = [
            (800, 450), (1200, 450), (2800, 450), (3200, 450)
        ]
        self.checkpoint_x = 2000
        self.fim_x = 3500

    def _gerar_fase4(self):
        # Favela dos Frangos - muitos buracos e plataformas
        self.plataformas.add(Plataforma(0, 520, 600, 80, tipo='chao'))
        self.plataformas.add(Plataforma(800, 520, 500, 80, tipo='chao'))
        self.plataformas.add(Plataforma(1500, 520, 600, 80, tipo='chao'))
        self.plataformas.add(Plataforma(2400, 520, 400, 80, tipo='chao'))
        self.plataformas.add(Plataforma(3100, 520, 900, 80, tipo='chao'))

        # Buracos enormes
        self.espinhos.add(Espinho(600, 560, 200))
        self.espinhos.add(Espinho(1300, 560, 200))
        self.espinhos.add(Espinho(2100, 560, 300))
        self.espinhos.add(Espinho(2800, 560, 300))

        # Muitas plataformas suspensas
        self.plataformas.add(Plataforma(650, 400, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(900, 350, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1200, 400, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1600, 350, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1900, 300, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2200, 380, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2600, 350, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2900, 400, 100, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3400, 350, 120, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3700, 300, 100, 20, tipo='plataforma'))

        self.plataformas.add(Caixa(500, 480))
        self.plataformas.add(Caixa(1700, 480))
        self.plataformas.add(Caixa(3200, 480))

        self.inimigos_spawns = [
            (300, 450), (1000, 450), (1800, 450), (2500, 450),
            (3300, 450), (3600, 450), (3800, 450)
        ]
        self.checkpoint_x = 2000
        self.fim_x = 3900

    def _gerar_fase5(self):
        # Boss Final - A Cobra vai fumar
        self.plataformas.add(Plataforma(0, 520, 2000, 80, tipo='chao'))
        self.plataformas.add(Plataforma(2200, 520, 1800, 80, tipo='chao'))

        # Buraco central dramatico
        self.espinhos.add(Espinho(2000, 560, 200))

        # Plataformas para esquiva
        self.plataformas.add(Plataforma(800, 400, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1200, 300, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(1600, 350, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(2600, 400, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3000, 300, 150, 20, tipo='plataforma'))
        self.plataformas.add(Plataforma(3400, 350, 150, 20, tipo='plataforma'))

        self.inimigos_spawns = [
            (600, 450), (1000, 450), (1500, 450), (2600, 450), (3200, 450)
        ]
        self.checkpoint_x = 2200
        self.fim_x = 3900
