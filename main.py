from acoes.cabecalho import * #CHAMANDO PACOTES NECESSÁRIOS

pygame.init()

#VARIÁVEIS CONTADORAS
vidas = 3
vida_boss = 10
balas = 40
fase = 1
cont = 0
#PAINEL CONTADOR
contador = fonteGame.render("Mortes: ", True, (255, 255, 255), (0, 0, 0))
pos_contador = contador.get_rect()
pos_contador.center = (300, 50)
#ANIMAÇÃO DOS GALOS
galo = GaloAnimacao()
galoInicio.add(galo)
dim = Dinheiro()
dinheiro.add(dim)
dim2 = Dinheiro()
dinheiro2.add(dim2)

#FUNCOES
# LIMITANDO FPS
timer = 0
clock = pygame.time.Clock()
fase4 = False

#limpagem da tela
barreira_limp = Barricada(objectGroup,barreira)
def limpa():
    pygame.sprite.spritecollide(barreira_limp, obstaculosGroup, True)
    pygame.sprite.spritecollide(barreira_limp, tiro_bossGroup, True)
    pygame.sprite.spritecollide(barreira_limp, tiroGroup, True)


if __name__ == "__main__":
    #VÁRIAVEIS DE CONTROLE DO GAME
    gameLooping=False
    perdeu=False
    #############################

    #INICIO DA ANIMAÇÃO

    ############################################
    animacaoIni=True
    while animacaoIni:
        # INICIA A MUSICA DA ANIMAÇÃO
        animacao.play()
        contani=0
        gerarobg=True

        while gerarobg:
            """"AQUI FAZ A IMPLEMENTAÇÃO DA
            ANIMAÇÃO"""
            clock.tick(20)
            # ATRIBUI ELEMENTOS NA TELA DA ANIMAÇÃO
            screen.fill((128, 128, 128))
            screen.blit(nomeJogo, (70,90))
            #O TEXT ABAIXO É OPCIONAL
            screen.blit(text, (250, 450))
            #DINHEIRO
            dinheiro.draw(screen)
            dinheiro.update()
            pygame.display.flip()
            dinheiro2.draw(screen)
            dinheiro2.update()
            pygame.display.flip()
            #ANIMAÇÃO DO GALO
            galoInicio.draw(screen)
            galoInicio.update()
            pygame.display.flip()
            pygame.display.update()

            contani += 1
            if contani == 120:
                gerarobg = False
            #LISTA DE TECLAS
            for event in pygame.event.get():
                #SE APERTAR NO X DA ABA O PROGRAMA QUITA
                if event.type == pygame.QUIT:
                    exit(1)
                    menu.stop()
                if event.type== KEYDOWN:
                    #SE APERTAR E O PROGRAMA SAI DA ANIMAÇÃO E VAI PRO MENU
                    if event.key==K_e:
                        gerarobg = False
        animacaoIni=False
        # PARA A MUSICA DA ANIMACAO
        animacao.stop()
    #FIM DA ANIMAÇÃO      ######################################################


    #INICIO DO MENU AQUI ##################################################
    #INICIA A TOCAR A MÚSICA DO MENU
    menu.play()
    # ENTRA NO LAÇO PORQUE O GAMELOOPING NÃO É TRUE
    while not gameLooping:
        #INICIA A MUSICA NO MENU
        #CARREGA O FUNDO DO MENU
        fundos_menu()
        #CARREGA O LOGO DO MENU
        imagem_menu()
        #OPÇÕES DO MENU
        screen.blit(textom1, [245, 317])
        screen.blit(textom2, [245, 376])

        #ATUALIZA A TELA
        pygame.display.update()
        #PEGA A LISTA DE TECLAS E VERIFICA QUAL É A CLICADA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)
                menu.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit(0)
                    menu.stop()
                if event.key == pygame.K_s:
                    #VAI RETORNAR TRUE PRA ENTRAR NO OUTRO LAÇO DE REPETIÇÃO
                    gameLooping=True
                    menu.stop()

    #FIM DO MENU #################################################################
    # INICIA A TOCAR A MÚSICA DO JOGO
    if fase == 1:
        fase1.play()

    while gameLooping:

        #LIMITADOR DE FPS
        clock.tick(120)

        pygame.display.flip()
        screen.fill(azul)
        fundo_fase1()
        screen.blit(instrucoes, pos_instrucoes)
        screen.blit(objetivo, pos_objetivos)

        ##EVENTOS DO JOGO

        for event in pygame.event.get():
            ##SE APERTAR NO X DA ABA O PROGRAMA QUITA
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit(0)
            #QUANDO APERTA ESPAÇO ATIRA
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and not perdeu:
                    #SOM QUANDO ATIRA
                    tiro.play()
                    #DIMINUI 1 BALA A CADA CLIQUE
                    balas -= 1
                    #CHAMA A BALA, QUE SAIRA DO PERSONAGEM E VAI ANDANDO PELO EIXO X
                    newTiro=Municao(objectGroup,tiroGroup)
                    newTiro.rect.center=personagem.rect.center
                #FAZ PULAR DE FASE
                if event.key == pygame.K_j and fase<4:
                    fase+=1
                    cont+=20
                    # TROCA A MUSICA
                    if fase == 2:
                        fase1.stop()
                        fase2.play()
                    elif fase == 3:
                        fase2.stop()
                        fase3.play()
                    # LIMPA A TELA
                    limpa()
                    balas = 40
       # (IMPORTANTE) FIM DA LISTA DE TECLAS ####################3###################
        #LÓGICA DO JOGO EM SI

        if not perdeu:
            #Gera Os galo schaves #########################

            #ATUALIZA OS OBJETOS DA TELA
            objectGroup.update()

            # DEFININDO APARIÇÃO DOS OBSTACULOS
            timer += 1
            if timer > 30*fase:
                timer = 0
                if random.random() < 0.3*fase:
                    #GERA UM NOVO OBSTACULO(OS GALOS NORMAIS)
                    newObstaculos = Obstaculos(objectGroup,obstaculosGroup)
                    #GERA O TIRO DO BOSS (O GALO DE JUJU)
                    newTiro_boss = Municao_boss(objectGroup, tiro_bossGroup)
                    newTiro_boss.rect.center = boss.rect.center

            # Analisa se tem impacto
            colliTiro = pygame.sprite.groupcollide(tiro_bossGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)
            collisions = pygame.sprite.spritecollide(personagem, obstaculosGroup, True, pygame.sprite.collide_mask)
            colliTiro = pygame.sprite.groupcollide(tiroGroup, obstaculosGroup, True, True, pygame.sprite.collide_mask)
            collitiro_boss = pygame.sprite.spritecollide(personagem, tiro_bossGroup, True, pygame.sprite.collide_mask)
            collitiro_Boss = pygame.sprite.spritecollide(boss, tiroGroup, True, pygame.sprite.collide_mask)
            collitiro_ = pygame.sprite.groupcollide(tiroGroup, tiro_bossGroup, True, True, pygame.sprite.collide_mask)

            # SE HOUVER COLIZÃO DA SUA BALA COM O BOSS O BOSS PERDE VIDA, SE ELE PERDER AS SUAS 10 VIDAS VC GANHA O GAME
            if collitiro_Boss and fase == 3:
                vida_boss -= 1
                perdeu_vida.play()
                # SE VC MATAR O BOSS TELA DE VITÓRIA
                if vida_boss <= 0:
                    morreu.play()
                    # MUDA PARA TELA DE VITORIA
                    fase = 4

            #Conta as mortes
            if  colliTiro :
                cont += 1
                dano.play()

            # CONTADOR DE FASES

            if cont == 20:
                fase = 2
                balas = 40

            if cont == 40:
                fase = 3
                balas = 20

            if cont == 60:
                fase = 4

            if fase == 2:
                screen.blit(objetivo, pos_objetivos)

                fundo_fase2()

            elif fase == 3:
                fundo_fase3()
                screen.blit(objetivo3, pos_objetivos3)

            #contador
            contador = fonteGame.render("Mortes: %i | Balas: %i | Vidas: %i | Fase: %i | BOSS: %i" % (cont, balas, vidas, fase, vida_boss), True, (255, 255, 255), (0, 0, 0))

            #QUANDO O JOGADOR CHEGA AQUI O JOGO ACABA, DAR OS PARABÉNS E VERIFICA SE QUER CONTINUAR OU SAIR
            if fase == 4:
                #VARIAVEL DE CONTROLE
                fase4=True
                # PARANDO DE REPRODUZIR A MUSICA
                fase1.stop()
                fase2.stop()
                fase3.stop()

             #FIM DO TRATAMENTO DAS FASES DO GAME

            #Contador de vidas e balas
            #SE HOUVER COLIZÃO COM ALGUM GALO OU O TIRO DO GALO BOSS PERDE VIDA

            if not collisions and not collitiro_boss:
                pass
            else:
                vidas -= 1
                perdeu_vida.play()
                if vidas <= 0:
                    morreu.play()
                    perdeu = True

             #SE AS BALAS ACABARAM VC PERDE
            if balas <= 0:
                    perdeu = True

            #TRATAMENTO DE FASES(2) CASO VOCÊ PERCA
            if perdeu == True:
                # PARANDO DE REPRODUZIR A MUSICA
                if fase == 1:
                    fase1.stop()
                elif fase == 2:
                    fase2.stop()
                else:
                    fase3.stop()


            #GAMEOVER
            while perdeu or fase4:
                #CARREGA IMAGENS E ETC...
                if perdeu:
                    funeral()
                    screen.blit(voce_morreu, pos_global)
                if fase4:
                    fundo_fase4()
                    screen.blit(voce_venceu, pos_global)
                pygame.display.update()
                ############################
                #INICIO DA LISTA DE TECLAS
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameLooping = False
                        perdeu = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            pygame.quit()
                            exit(0)
                        if event.key == pygame.K_c:
                            fase = 1
                            timer = 0
                            cont = 0
                            vidas = 3
                            vida_boss = 10
                            balas = 40
                            perdeu = False
                            fase4 = False
                            gameLooping = True
                            if fase == 1:
                                fase1.play()
                            limpa()
                #FIM DA LISTA DE TECLAS ##########
        #Contador
        screen.blit(contador,pos_contador)
        objectGroup.draw(screen)

        pygame.display.update()
