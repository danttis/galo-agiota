import pygame

def texto_com_borda(fonte, texto, cor, cor_borda=(0, 0, 0), antialias=True):
    """Renderiza texto com contorno preto (8 direcoes) para legibilidade."""
    base = fonte.render(texto, antialias, cor)
    borda = fonte.render(texto, antialias, cor_borda)
    w, h = base.get_size()
    surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
    for dx, dy in [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]:
        surf.blit(borda, (dx, dy))
    surf.blit(base, (1, 1))
    return surf
