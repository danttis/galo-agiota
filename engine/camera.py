from config import LARGURA, ALTURA

class Camera:
    def __init__(self, largura_mundo, altura_mundo):
        self.offset_x = 0
        self.offset_y = 0
        self.largura_mundo = largura_mundo
        self.altura_mundo = altura_mundo

    def seguir(self, alvo):
        # Centraliza a camera no alvo com suavizacao
        alvo_x = alvo.rect.centerx - LARGURA // 2

        self.offset_x += (alvo_x - self.offset_x) * 0.1
        # Fixa Y - jogo eh side-scroller horizontal
        self.offset_y = 0

        # Limita aos bounds do mundo
        self.offset_x = max(0, min(self.offset_x, self.largura_mundo - LARGURA))

    def aplicar(self, sprite):
        return sprite.rect.move(-int(self.offset_x), -int(self.offset_y))

    def aplicar_rect(self, rect):
        return rect.move(-int(self.offset_x), -int(self.offset_y))
