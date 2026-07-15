from config import GRAVIDADE

def aplicar_gravidade(sprite):
    if hasattr(sprite, 'vel_y'):
        sprite.vel_y += GRAVIDADE
        sprite.rect.y += int(sprite.vel_y)

def resolver_colisao_plataforma(sprite, plataformas):
    """Resolve colisao do sprite com plataformas usando posicao anterior.
    Retorna True se estiver no chao."""
    no_chao = False

    # Posicao anterior (antes do movimento deste frame)
    vel_y = getattr(sprite, 'vel_y', 0)
    vel_x = getattr(sprite, 'vel_x', 0)
    old_top = sprite.rect.top - int(vel_y)
    old_bottom = sprite.rect.bottom - int(vel_y)
    old_left = sprite.rect.left - int(vel_x)
    old_right = sprite.rect.right - int(vel_x)

    for plat in plataformas:
        if not sprite.rect.colliderect(plat.rect):
            continue

        # Veio por CIMA (estava abaixo da plataforma, subiu e bateu a cabeca)
        # Margem de tolerancia para velocidades altas
        if old_bottom <= plat.rect.top + max(0, -int(vel_y)):
            sprite.rect.bottom = plat.rect.top
            if vel_y > 0:
                sprite.vel_y = 0
            no_chao = True

        # Veio por BAIXO (estava acima da plataforma, caiu em cima)
        # Margem de tolerancia para velocidades altas
        elif old_top >= plat.rect.bottom - max(0, int(vel_y)):
            sprite.rect.top = plat.rect.bottom
            if vel_y < 0:
                sprite.vel_y = 0

        # Colisao LATERAL
        else:
            if old_right <= plat.rect.left:
                sprite.rect.right = plat.rect.left
            elif old_left >= plat.rect.right:
                sprite.rect.left = plat.rect.right
            if vel_x != 0:
                sprite.vel_x = 0

    return no_chao
