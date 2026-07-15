import pygame
import random
from pygame.locals import *

from config import LARGURA, ALTURA, FPS, TITULO, BRANCO, PRETO, VERMELHO, VERDE, AMARELO, AZUL
from plot.imagens import carregar as carregar_imagens
from plot.sons import carregar as carregar_sons
from engine.camera import Camera
from engine.particulas import criar_explosao, criar_sangue, criar_penas, Explosao, Particula
from engine.texto import texto_com_borda
from mundo.nivel import Nivel
from mundo.plataforma import Plataforma
from entidades.jogador import Jogador
from entidades.inimigo import Inimigo
from entidades.boss import Boss, BossVisitante
from entidades.projetil import Projetil, Suborno
from ui.hud import HUD
from historia.intro import Intro


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    clock = pygame.time.Clock()

    imgs = carregar_imagens()
    sons = carregar_sons()

    try:
        fonte_menu = pygame.font.SysFont("Ubuntu Sans", 28, bold=True)
        fonte_grande = pygame.font.SysFont("Ubuntu Sans", 42, bold=True)
    except:
        fonte_menu = pygame.font.SysFont("monospace", 28, bold=True)
        fonte_grande = pygame.font.SysFont("monospace", 42, bold=True)

    def toggle_som():
        som_mutado = False
        for s in sons.values():
            if s:
                if s.get_volume() > 0:
                    s.set_volume(0)
                    som_mutado = True
                else:
                    s.set_volume(1)
        return som_mutado

    def reset_grupos():
        todos = pygame.sprite.Group()
        plataformas = pygame.sprite.Group()
        espinhos = pygame.sprite.Group()
        inimigos = pygame.sprite.Group()
        tiros_jogador = pygame.sprite.Group()
        tiros_inimigo = pygame.sprite.Group()
        subornos = pygame.sprite.Group()
        particulas = pygame.sprite.Group()
        return todos, plataformas, espinhos, inimigos, tiros_jogador, tiros_inimigo, subornos, particulas

    def estado_menu():
        if sons.get('menu'):
            sons['menu'].play(-1)
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if sons.get('menu'):
                            sons['menu'].stop()
                        return 'intro'
                    if event.key == pygame.K_q:
                        return 'sair'
                    if event.key == pygame.K_m:
                        toggle_som()

            if 'menu_fundo' in imgs:
                fundo = pygame.transform.scale(imgs['menu_fundo'], (LARGURA, ALTURA))
                screen.blit(fundo, (0, 0))
            else:
                screen.fill((30, 30, 60))

            if 'logo' in imgs:
                logo = pygame.transform.scale(imgs['logo'], (350, 120))
                screen.blit(logo, (LARGURA//2 - 175, 60))

            titulo = texto_com_borda(fonte_grande, "GALO AGIOTA", AMARELO)
            screen.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 200))

            start = texto_com_borda(fonte_menu, "START GAME - PRESSIONE [S]", BRANCO)
            screen.blit(start, (LARGURA//2 - start.get_width()//2, 340))

            quitg = texto_com_borda(fonte_menu, "QUIT GAME - PRESSIONE [Q]", (200, 200, 200))
            screen.blit(quitg, (LARGURA//2 - quitg.get_width()//2, 390))

            pygame.display.flip()

    def estado_intro():
        intro = Intro(screen, imgs)
        while intro.ativa:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                intro.evento(event)
            intro.update()
            intro.desenhar()
            pygame.display.flip()
        return 'preparar'

    def estado_preparar():
        """Tela de espera antes do jogo comecar. Aguarda tecla/espaco."""
        esperando = True
        while esperando:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        esperando = False
                    if event.key == pygame.K_ESCAPE:
                        return 'sair'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False

            screen.fill(PRETO)
            t1 = texto_com_borda(fonte_grande, "GALO AGIOTA", AMARELO)
            screen.blit(t1, (LARGURA//2 - t1.get_width()//2, 150))

            t2 = texto_com_borda(fonte_menu, "FASE 1 - A FAVELA DOS FRANGOS", BRANCO)
            screen.blit(t2, (LARGURA//2 - t2.get_width()//2, 250))

            pisca = (pygame.time.get_ticks() // 400) % 2 == 0
            if pisca:
                t3 = texto_com_borda(fonte_menu, "PRESSIONE [ESPACO] OU CLIQUE PARA COMECAR", VERDE)
                screen.blit(t3, (LARGURA//2 - t3.get_width()//2, 380))

            pygame.display.flip()
        return 'jogar'

    def estado_jogar():
        fase_atual = 1
        venceu = False
        perdeu = False

        while not venceu and not perdeu:
            resultado = jogar_fase(fase_atual)
            if resultado == 'proxima':
                fase_atual += 1
                if fase_atual > 5:
                    venceu = True
            elif resultado == 'morreu':
                perdeu = True
            elif resultado == 'sair':
                return 'sair'

        if venceu:
            return estado_vitoria()
        else:
            return estado_gameover()

    def jogar_fase(numero_fase):
        todos, plataformas, espinhos, inimigos, tiros_jogador, tiros_inimigo, subornos, particulas = reset_grupos()

        nivel = Nivel(numero_fase)
        for plat in nivel.plataformas:
            plataformas.add(plat)
            todos.add(plat)
        for esp in nivel.espinhos:
            espinhos.add(esp)
            todos.add(esp)

        jogador = Jogador(100, 400, imgs['galo'])
        todos.add(jogador)

        # Boss real so nas fases 3 e 5
        boss = None
        if numero_fase == 3 or numero_fase == 5:
            boss = Boss(nivel.fim_x, 400, imgs['boss'])
            todos.add(boss)
            inimigos.add(boss)

        for pos in nivel.inimigos_spawns:
            cap = Inimigo(pos[0], pos[1], imgs['capanga'])
            inimigos.add(cap)
            todos.add(cap)

        camera = Camera(4000, ALTURA)
        hud = HUD()
        hud.mostrar_mensagem(f"FASE {numero_fase} - COMECO!")

        # Timer do boss visitante - so aparece UMA vez por fase, pela DIREITA
        boss_visitante = None
        boss_visitante_timer = random.randint(300, 600)  # 5-10 segundos ate aparecer
        boss_visitante_ja_apareceu = False

        chave_musica = f'fase{min(numero_fase, 3)}'
        if sons.get(chave_musica):
            sons[chave_musica].play(-1)

        running = True
        spawn_timer = 0
        while running:
            clock.tick(FPS)
            tempo_atual = pygame.time.get_ticks()
            teclas = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if sons.get(chave_musica):
                        sons[chave_musica].stop()
                    return 'sair'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if sons.get(chave_musica):
                            sons[chave_musica].stop()
                        return 'sair'
                    if event.key == pygame.K_j:
                        if sons.get(chave_musica):
                            sons[chave_musica].stop()
                        return 'proxima'
                    if event.key == pygame.K_m:
                        toggle_som()

            # Boss visitante logica (aparece UMA vez em fases 1, 2, 4), pela DIREITA
            if numero_fase in [1, 2, 4] and not boss_visitante_ja_apareceu:
                boss_visitante_timer -= 1
                if boss_visitante_timer <= 0:
                    # Encontra trecho de chao seguro à direita do jogador para spawnar
                    chao_seguro = None
                    for plat in nivel.plataformas:
                        if getattr(plat, 'tipo', None) == 'chao' and plat.rect.right > jogador.rect.x + 300:
                            if chao_seguro is None or plat.rect.left < chao_seguro.rect.left:
                                chao_seguro = plat
                    if chao_seguro is None:
                        # Fallback: ultimo chao da fase
                        for plat in nivel.plataformas:
                            if getattr(plat, 'tipo', None) == 'chao':
                                if chao_seguro is None or plat.rect.right > chao_seguro.rect.right:
                                    chao_seguro = plat
                    if chao_seguro:
                        bx = min(chao_seguro.rect.right - 80, chao_seguro.rect.left + max(0, chao_seguro.rect.width - 80))
                        by = chao_seguro.rect.top - 64  # sprite 64x64 fica em pe no chao
                    else:
                        bx = jogador.rect.x + 700
                        by = 456
                    boss_visitante = BossVisitante(bx, by, imgs['boss'])
                    inimigos.add(boss_visitante)
                    todos.add(boss_visitante)
                    boss_visitante_ja_apareceu = True

            # Update jogador
            jogador.update(teclas, plataformas, tiros_jogador, subornos, tempo_atual)
            todos.add(*tiros_jogador)
            todos.add(*subornos)

            # Update inimigos
            for ini in list(inimigos):
                if not ini.alive():
                    continue
                if isinstance(ini, Boss):
                    ini.update(jogador, plataformas, tiros_inimigo, inimigos, particulas, imgs['capanga'])
                elif isinstance(ini, BossVisitante):
                    ini.update(jogador, plataformas, tiros_inimigo, inimigos, particulas, imgs['capanga'])
                else:
                    ini.update(jogador, plataformas, tiros_inimigo, particulas, inimigos)
            todos.add(*tiros_inimigo)

            # Update projeteis
            for t in tiros_jogador:
                t.update()
            for t in tiros_inimigo:
                t.update()

            # Update subornos
            for s in list(subornos):
                s.update()
                # Colisao suborno -> inimigo: suborna!
                if s.alive() and s.parado:
                    atingidos = pygame.sprite.spritecollide(s, inimigos, False)
                    for ini in atingidos:
                        if not ini.alive() or ini.morto or isinstance(ini, (Boss, BossVisitante)):
                            continue
                        if getattr(ini, 'subornado', False):
                            continue
                        ini.subornar()
                        jogador.score += 50
                        s.kill()
                        if sons.get('dano'):
                            sons['dano'].play()
                        break

            # Update particulas
            for p in list(particulas):
                p.update()
            todos.add(*particulas)

            # Camera segue jogador
            camera.seguir(jogador)

            # Colisoes: tiro jogador -> inimigos
            for tiro in list(tiros_jogador):
                if not tiro.alive():
                    continue
                atingidos = pygame.sprite.spritecollide(tiro, inimigos, False)
                for ini in atingidos:
                    if not ini.alive():
                        continue
                    if isinstance(ini, BossVisitante):
                        ini.tomar_dano(tiro.dano, particulas)
                        tiro.kill()
                        break
                    elif isinstance(ini, Boss):
                        ini.tomar_dano(tiro.dano, particulas)
                        jogador.score += 50
                        if ini.morto:
                            jogador.dinheiro += 5000
                    else:
                        ini.tomar_dano(tiro.dano, particulas)
                        if ini.morto:
                            jogador.score += 20
                            jogador.dinheiro += 100
                    tiro.kill()
                    break

            # Colisoes: tiro jogador <-> tiro inimigo (anulam-se no ar)
            for tiro_j in list(tiros_jogador):
                if not tiro_j.alive():
                    continue
                for tiro_i in list(tiros_inimigo):
                    if not tiro_i.alive():
                        continue
                    if tiro_j.rect.colliderect(tiro_i.rect):
                        criar_explosao(particulas, tiro_j.rect.centerx, tiro_j.rect.centery, 4)
                        tiro_j.kill()
                        tiro_i.kill()
                        break

            # Colisoes: tiro inimigo -> jogador
            for tiro in list(tiros_inimigo):
                if not tiro.alive():
                    continue
                if tiro.rect.colliderect(jogador.rect):
                    if jogador.tomar_dano(tempo_atual):
                        if sons.get('perdeu_vida'):
                            sons['perdeu_vida'].play()
                        criar_sangue(particulas, jogador.rect.centerx, jogador.rect.centery, 5)
                    tiro.kill()

            # Colisoes: inimigo subornado -> inimigo normal (corpo a corpo)
            for ini in list(inimigos):
                if not ini.alive() or ini.morto or not getattr(ini, 'subornado', False):
                    continue
                for alvo in list(inimigos):
                    if alvo is ini or not alvo.alive() or alvo.morto or getattr(alvo, 'subornado', False):
                        continue
                    if isinstance(alvo, (Boss, BossVisitante)):
                        continue
                    if ini.rect.colliderect(alvo.rect):
                        alvo.tomar_dano(2, particulas)
                        if alvo.morto:
                            jogador.score += 20
                            jogador.dinheiro += 100
                        ini.vel_x *= -1
                        break

            # Colisoes: jogador -> inimigos (corpo a corpo)
            for ini in list(inimigos):
                if not ini.alive() or ini.morto:
                    continue
                # Inimigo subornado nao machuca o jogador
                if getattr(ini, 'subornado', False):
                    continue
                if not jogador.rect.colliderect(ini.rect):
                    continue

                # Pulo estilo Mario: caindo em cima do inimigo
                # Margem de 12 pixels para detectar a cabeca do inimigo
                pisando = jogador.vel_y > 0 and jogador.rect.bottom <= ini.rect.top + 12
                if pisando and not isinstance(ini, (Boss, BossVisitante)):
                    # Bounce no jogador
                    jogador.vel_y = -10
                    # Dano no inimigo
                    ini.tomar_dano(2, particulas)
                    if ini.morto:
                        jogador.score += 20
                        jogador.dinheiro += 100
                        if sons.get('dano'):
                            sons['dano'].play()
                    continue

                # Colisao lateral/normal: jogador toma dano
                if jogador.tomar_dano(tempo_atual):
                    if sons.get('perdeu_vida'):
                        sons['perdeu_vida'].play()
                    criar_sangue(particulas, jogador.rect.centerx, jogador.rect.centery, 5)

            # Colisoes: jogador -> espinhos (insta-kill)
            for esp in espinhos:
                if jogador.rect.colliderect(esp.rect):
                    jogador.vidas = 0
                    jogador.morrer()
                    criar_explosao(particulas, jogador.rect.centerx, jogador.rect.centery, 20)
                    if sons.get('morreu'):
                        sons['morreu'].play()
                    break

            # Respawn se morreu
            if jogador.morto:
                if sons.get('morreu'):
                    sons['morreu'].play()
                if sons.get(chave_musica):
                    sons[chave_musica].stop()
                return 'morreu'

            # Verifica vitoria de fase
            if numero_fase in [3, 5] and boss and boss.morto:
                if sons.get(chave_musica):
                    sons[chave_musica].stop()
                return 'proxima'
            elif numero_fase not in [3, 5] and jogador.rect.right >= nivel.fim_x:
                if sons.get(chave_musica):
                    sons[chave_musica].stop()
                return 'proxima'

            # Spawna inimigos extras
            ativos = [i for i in inimigos if i.alive() and not i.morto and not isinstance(i, (Boss, BossVisitante))]
            if len(ativos) < 3 and numero_fase not in [3, 5]:
                spawn_timer += 1
                if spawn_timer > 120:
                    spawn_timer = 0
                    amostra = random.sample(nivel.inimigos_spawns, min(2, len(nivel.inimigos_spawns)))
                    for pos in amostra:
                        cap = Inimigo(pos[0] + random.randint(-100, 100), pos[1], imgs['capanga'])
                        inimigos.add(cap)
                        todos.add(cap)

            if jogador.municao <= 0 and teclas[pygame.K_r]:
                jogador.municao = 30

            # DESENHO
            # Fundo parallax (escalado para cobrir a tela)
            chave_fundo = f'fase{min(numero_fase, 3)}'
            if chave_fundo in imgs:
                fundo = pygame.transform.scale(imgs[chave_fundo], (LARGURA, ALTURA))
                bg_x = -(int(camera.offset_x) % fundo.get_width())
                screen.blit(fundo, (bg_x, 0))
                if bg_x + fundo.get_width() < LARGURA:
                    screen.blit(fundo, (bg_x + fundo.get_width(), 0))
            else:
                screen.fill((60, 50, 90))

            # Desenha sprites com offset da camera
            for sprite in list(todos):
                if hasattr(sprite, 'image') and sprite.image and sprite.alive():
                    pos = camera.aplicar(sprite)
                    # Verifica visibilidade considerando largura/altura do sprite
                    if pos.right > -200 and pos.x < LARGURA + 200 and pos.bottom > -200 and pos.y < ALTURA + 200:
                        screen.blit(sprite.image, pos)

            hud.desenhar(screen, jogador, numero_fase, boss)

            # Efeito de transicao se perto do fim
            if numero_fase not in [3, 5] and jogador.rect.right > nivel.fim_x - 200:
                s = pygame.Surface((LARGURA, ALTURA))
                s.set_alpha(100)
                s.fill(PRETO)
                screen.blit(s, (0, 0))
                txt = texto_com_borda(fonte_menu, "PORTA DO CHEFE!", AMARELO)
                screen.blit(txt, (LARGURA//2 - txt.get_width()//2, ALTURA//2))

            pygame.display.flip()

        if sons.get(chave_musica):
            sons[chave_musica].stop()
        return 'sair'

    def estado_vitoria():
        if sons.get('menu'):
            sons['menu'].play(-1)
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        if sons.get('menu'):
                            sons['menu'].stop()
                        return 'jogar'
                    if event.key == pygame.K_s:
                        return 'sair'

            if 'venceu' in imgs:
                v = pygame.transform.scale(imgs['venceu'], (LARGURA, ALTURA))
                screen.blit(v, (0, 0))
            else:
                screen.fill((20, 80, 20))

            t1 = texto_com_borda(fonte_grande, "PARABENS!", AMARELO)
            screen.blit(t1, (LARGURA//2 - t1.get_width()//2, 100))

            t2 = texto_com_borda(fonte_menu, "A DIVIDA FOI COBRADA COM SUCESSO!", BRANCO)
            screen.blit(t2, (LARGURA//2 - t2.get_width()//2, 200))

            t3 = texto_com_borda(fonte_menu, "[C] JOGAR NOVAMENTE", BRANCO)
            screen.blit(t3, (LARGURA//2 - t3.get_width()//2, 350))

            t4 = texto_com_borda(fonte_menu, "[S] SAIR", (200, 200, 200))
            screen.blit(t4, (LARGURA//2 - t4.get_width()//2, 400))

            pygame.display.flip()

    def estado_gameover():
        if sons.get('menu'):
            sons['menu'].play(-1)
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'sair'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        if sons.get('menu'):
                            sons['menu'].stop()
                        return 'jogar'
                    if event.key == pygame.K_s:
                        return 'sair'

            if 'funeral' in imgs:
                f = pygame.transform.scale(imgs['funeral'], (LARGURA, ALTURA))
                screen.blit(f, (0, 0))
            else:
                screen.fill((20, 20, 20))

            t1 = texto_com_borda(fonte_grande, "GAME OVER", VERMELHO)
            screen.blit(t1, (LARGURA//2 - t1.get_width()//2, 100))

            t2 = texto_com_borda(fonte_menu, "O GALO DEVEDOR ESCAPOU...", BRANCO)
            screen.blit(t2, (LARGURA//2 - t2.get_width()//2, 200))

            t3 = texto_com_borda(fonte_menu, "[C] TENTAR NOVAMENTE", BRANCO)
            screen.blit(t3, (LARGURA//2 - t3.get_width()//2, 350))

            t4 = texto_com_borda(fonte_menu, "[S] DESISTIR", (200, 200, 200))
            screen.blit(t4, (LARGURA//2 - t4.get_width()//2, 400))

            pygame.display.flip()

    estado = 'menu'
    while True:
        if estado == 'menu':
            estado = estado_menu()
        elif estado == 'intro':
            estado = estado_intro()
        elif estado == 'preparar':
            estado = estado_preparar()
        elif estado == 'jogar':
            estado = estado_jogar()
        elif estado == 'sair':
            break

    pygame.quit()


if __name__ == "__main__":
    main()
