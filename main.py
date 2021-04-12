import pygame, sys, os
from pygame.locals import *
from obstaculos import Obstaculos
from personagem import Persona
from municao import *
from boss import Boss
from obj_animacao import GaloAnimacao
from obj_animacao import Dinheiro
from barricada import Barricada
import random

##inica o pygame e suas dependências

pygame.init()
pygame.font.init()
pygame.mixer.init()

##Definições da janela do game

screenDimension=(750,500)
pygame.display.set_caption("Galo Agiota 1.0")
screen=pygame.display.set_mode(screenDimension, 0, 32)
pygame.display.set_icon(screen)

##Define variáveis com valores de cor ou coordenada

azul=(108,194,236)
branco=(255,255,255)
fonteGame=pygame.font.SysFont("data/Vermin_Vibes_1989.ttf",15)

# CARREGANDO TODAS AS MÚSICAS

menu = pygame.mixer.Sound("data/background_menu.wav")
animacao = pygame.mixer.Sound("data/animacao.wav")
fase1 = pygame.mixer.Sound("data/background_fase1.wav")
fase2 = pygame.mixer.Sound("data/background_fase2.wav")
fase3 = pygame.mixer.Sound("data/background_fase3.wav")


# SONS DE AÇÕES
tiro = pygame.mixer.Sound("data/tiro.wav")
morreu = pygame.mixer.Sound("data/morreu.wav")
dano = pygame.mixer.Sound("data/dano.wav")
perdeu_vida = pygame.mixer.Sound("data/perdeu_vida.wav")

# CHAMANDO OBJETO
objectGroup = pygame.sprite.Group()
obstaculosGroup=pygame.sprite.Group()
tiroGroup=pygame.sprite.Group()
tiro_bossGroup = pygame.sprite.Group()
barreira = pygame.sprite.Group()
#INSTANCIA DO OBJETO
personagem =Persona(objectGroup)
boss = Boss(objectGroup)
#CONTADOR DE MORTES E FASES
fase = 1
cont = 0
contador = fonteGame.render("Mortes: ", True, (255, 255, 255), (0, 0, 0))
pos_contador = contador.get_rect()
pos_contador.center = (300, 50)

# OBJETIVO DAS FASES
objetivo = fonteGame.render("Derrote 20 GALOS CAPANGAS para passar de fase",True, (255,255,255), (0, 0, 0))
pos_objetivos = objetivo.get_rect()
pos_objetivos = (5, 100)

# OBJETIVO DA FASE 3
objetivo3 = fonteGame.render("Derrote o GALO DEVEDOR",True, (255,255,255), (0, 0, 0))
pos_objetivos3 = objetivo.get_rect()
pos_objetivos3 = (5, 100)

#TEXTOS
instrucoes = fonteGame.render("USE AS TECLAS DIRECIONAIS DO SEU TECLADO PARA MOVER O GALO PARA CIMA OU PARA BAIXO, E USE A TECLA SPACE BAR PARA ATIRAR", True, (255, 255, 255), (0, 0, 0))
pos_instruções = instrucoes.get_rect()
pos_instruções = (18, 480)
voce_morreu = fonteGame.render("VOCÊ MORREU PRESSIONE 'C' PARA CONTINUAR OU 'S' PARA SAIR", True, (255, 255, 255), (0, 0, 0))
pos_global = voce_morreu.get_rect()
pos_global = (200, 100)
voce_venceu = fonteGame.render("VOCÊ VENCEU! SE DESEJAR JOGAR DE NOVO PRESSIONE [C] PARA SAIR [E]", True, (255, 255, 255), (0, 0, 0))

#Contador de vidas e balas
vidas = 3
vida_boss = 10
balas = 40

#FUNDOS
#Fundo menu;
Menu_fundo = pygame.image.load("data/fundoM.png.png")
imagemMenu = pygame.image.load("data/logoMenu.png")
#Fase 1
fase_1 = pygame.image.load("data/fundo_fase_1.png")
pos_fase_1 = fase_1.get_rect()
pos_fase_1.center = (375, 250)
#Fase 2
fase_2 = pygame.image.load("data/fundo_fase_2.png")

#Fase 3
fase_3 = pygame.image.load("data/fundo_fase_3.png")

#Fase 4
fase_4 = pygame.image.load("data/venceu.png")

#Game over
funeral = pygame.image.load("data/funeral.png")

#Animação dados
galoInicio = pygame.sprite.Group()
galo = GaloAnimacao()
galoInicio.add(galo)

dinheiro = pygame.sprite.Group()
dim = Dinheiro()
dinheiro.add(dim)
dinheiro2 = pygame.sprite.Group()
dim2 = Dinheiro()
dinheiro2.add(dim2)
fonte_animacao = pygame.font.SysFont("Vermin_Vibes_1989.ttf", 20)
nomeJogo = pygame.image.load('data/logoJogo.png')

#FUNCOES
# LIMITANDO FPS
timer = 0
clock = pygame.time.Clock()

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

    #INICIO DA ANIMAÇÃO   ############################################
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
            #Atribui elementos na tela de animação #####
            screen.fill((128, 128, 128))
            screen.blit(nomeJogo, (70,90))
            #o text abaixo é opcional
            text = fonte_animacao.render("PRESSIONE [E] PARA PULAR A ANIMAÇÂO", True, (255, 255, 255), (0, 0, 0))
            screen.blit(text, (250, 450))
            #dinheiros
            dinheiro.draw(screen)
            dinheiro.update()
            pygame.display.flip()
            dinheiro2.draw(screen)
            dinheiro2.update()
            pygame.display.flip()
            #galo andando na tela
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
    # Entra no laço pq o gamelooping não é True
    while not gameLooping:
        #Inicia a música do menu
        #Define a fonte que usaremos
        fonteGameMENU1 = pygame.font.SysFont("data/Vermin_Vibes_1989.ttf", 25)
        #CARREGA O FUNDO DO MENU
        screen.blit(Menu_fundo, pos_fase_1)
        #CARREGA O LOGO DO MENU
        screen.blit(imagemMenu, (135, 50))
        #OPÇÕES DO MENU
        textom1 = fonteGameMENU1.render("START GAME PRESS [S]", True, (255, 255, 255))
        textom2 = fonteGameMENU1.render("QUIT GAME PRESS [Q]", True, (255, 255, 255))
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
        screen.blit(fase_1, pos_fase_1)
        screen.blit(instrucoes, pos_instruções)
        screen.blit(objetivo, pos_objetivos)

        ##Eventos do game

        #(IMPORTANTE) LISTA DE TECLAS ###############################
        for event in pygame.event.get():
            ##Quando aperta o X ele exita o pygame
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
        #(IMPORTANTE) FIM DA LISTA DE TECLAS ####################3###################

        #Lógica do game em sí

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




            colliTiro = pygame.sprite.groupcollide(tiro_bossGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)

            #Analisa se tem impacto
            collisions=pygame.sprite.spritecollide(personagem,obstaculosGroup, True, pygame.sprite.collide_mask)
            colliTiro=pygame.sprite.groupcollide(tiroGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)
            collitiro_boss=pygame.sprite.spritecollide(personagem, tiro_bossGroup, True, pygame.sprite.collide_mask)
            collitiro_Boss=pygame.sprite.spritecollide(boss, tiroGroup, True, pygame.sprite.collide_mask)
            collitiro_=pygame.sprite.groupcollide(tiroGroup, tiro_bossGroup, True, True,pygame.sprite.collide_mask)

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

                screen.blit(fase_2, pos_fase_1)
                screen.blit(objetivo, pos_objetivos)

            elif fase == 3:
                screen.blit(fase_3, pos_fase_1)
                screen.blit(objetivo3, pos_objetivos3)

            #QUANDO O JOGADOR CHEGA AQUI O JOGO ACABA, DAR OS PARABÉNS E VERIFICA SE QUER CONTINUAR OU SAIR
            if fase == 4:
                #VARIAVEL DE CONTROLE
                fase4=True
                # PARANDO DE REPRODUZIR A MUSICA
                fase1.stop()
                fase2.stop()
                fase3.stop()
                #REPETICAO ATÉ O CLIENTE RESPONDER ALGUMA COISA, QUANDO RESPONDE OU VAI SAIR OU VAI VOLTAR PRA FASE 1
                while fase4:
                    #IMPRESSÃO NA TELA DO GAME
                    screen.blit(fase_4, pos_fase_1)
                    screen.blit(voce_venceu, pos_global)
                    #exto("VOCÊ VENCEU! SE DESEJAR JOGAR DE NOVO PRESSIONE [C] PARA SAIR [E]", (0, 0, 0))
                    pygame.display.update()
                    #ANALISE DE QUAL OPÇÃO ELE OPTOU
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameLooping = False
                            perdeu = False
                            fase4=False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_e:
                                pygame.quit()
                                exit(0)
                            if event.key == pygame.K_c:
                                limpa()
                                fase = 1
                                timer = 0
                                cont = 0
                                vidas = 3
                                vida_boss = 10
                                balas = 40
                                perdeu = False
                                gameLooping = True
                                fase4=False
                                if fase == 1:
                                    fase1.play()

            #FIM DO TRATAMENTO DAS FASES DO GAME ##########################################################

            #Contador de vidas e balas
            #SE HOUVER COLIZÃO COM ALGUM GALO OU O TIRO DO GALO BOSS PERDE VIDA
            if collisions or collitiro_boss:
                vidas -= 1
                perdeu_vida.play()
                if vidas <= 0:
                    morreu.play()
                    perdeu = True
            #SE AS BALAS ACABARAM VC PERDE
            if balas <= 0:
                perdeu = True


             # Exibir contadores

            contador = fonteGame.render("Mortes: %i | Balas: %i | Vidas: %i | Fase: %i | BOSS: %i" % (cont, balas, vidas, fase, vida_boss),True, (255, 255, 255), (0, 0, 0))


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
            while perdeu:
                #CARREGA IMAGENS E ETC...
                screen.blit(funeral, pos_fase_1)
                screen.blit(voce_morreu, pos_global)
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
                            gameLooping = True
                            if fase == 1:
                                fase1.play()
                            limpa()
                #FIM DA LISTA DE TECLAS ##########
        #Contador
        screen.blit(contador, pos_contador)
        objectGroup.draw(screen)


        pygame.display.update()
