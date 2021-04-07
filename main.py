import pygame, sys, os
from pygame.locals import *
from obstaculos import Obstaculos
from personagem import Persona
from municao import *
from boss import Boss
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
#INSTANCIA DO OBJETO
personagem =Persona(objectGroup)
boss = Boss(objectGroup)
#CONTADOR DE MORTES E FASES
fase = 1
cont = 0
contador = fonteGame.render("Mortes: ", True, (255, 255, 255), (0, 0, 0))
pos_contador = contador.get_rect()
pos_contador.center = (300, 50)

#TEXTOS

instrucoes = fonteGame.render("USE AS TECLAS DIRECIONAIS DO SEU TECLADO PARA MOVER O GALO PARA CIMA OU PARA BAIXO, E USE A TECLA SPACE BAR PARA ATIRAR ", True, (255, 255, 255), (0, 0, 0))
pos_instruções = instrucoes.get_rect()
pos_instruções = (18, 480)
voce_morreu = fonteGame.render("VOCÊ MORREU PRESSIONE 'C' PARA CONTINUAR OU 'S' PARA SAIR", True, (255, 255, 255), (0, 0, 0))
pos_morreu = voce_morreu.get_rect()
pos_morreu = (200, 250)
voce_venceu = fonteGame.render("VOCÊ VENCEU! SE DESEJAR JOGAR DE NOVO PRESSIONE [C] PARA SAIR [E]", True, (255, 255, 255), (0, 0, 0))
#Contador de vidas e balas
vidas = 3
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


#FUNCOES
#txt do game over
def texto(mensagem, cor):
	textoTela = fonteGame.render(mensagem, True, cor)
	screen.blit(textoTela, [750/8, 500/2])
# LIMITANDO FPS
timer = 0
clock = pygame.time.Clock()

if __name__ == "__main__":
    gameLooping=False
    perdeu=False
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

    #INICIA A TOCAR A MÚSICA DO JOGO
    fase1.play()

    while gameLooping:

        #LIMITADOR DE FPS
        clock.tick(120)

        pygame.display.flip()
        screen.fill(azul)
        screen.blit(fase_1, pos_fase_1)
        screen.blit(instrucoes, pos_instruções)
        ##Eventos do game

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

                if event.key == pygame.K_j and fase<4:
                    fase+=1









        #Lógica do game em sí

        if not perdeu:
            #Gera Os galo schaves
            objectGroup.update()

            # DEFININDO APARIÇÃO DOS OBSTACULOS
            timer += 1
            if timer > 30*fase:
                timer = 0
                if random.random() < 0.3*fase:
                    newObstaculos = Obstaculos(objectGroup,obstaculosGroup)
                    newTiro_boss = Municao_boss(objectGroup, tiro_bossGroup)
                    newTiro_boss.rect.center = boss.rect.center


            colliTiro = pygame.sprite.groupcollide(tiro_bossGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)

            #Analisa se tem impacto
            collisions=pygame.sprite.spritecollide(personagem,obstaculosGroup, True, pygame.sprite.collide_mask)
            colliTiro=pygame.sprite.groupcollide(tiroGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)


            #Conta as mortes
            if  colliTiro :
                cont += 1
                dano.play()

            # CONTADOR DE FASES

            if cont == 20:
                fase = 2
                balas = 40


            if fase == 2:
                fase1.stop()
                fase2.play()
                screen.blit(fase_2, pos_fase_1)

            if cont == 40:
                fase = 3
                balas = 20
            if fase == 3:
                fase2.stop()
                fase3.play()

                screen.blit(fase_3, pos_fase_1)

            #QUANDO O JOGADOR CHEGA AQUI O JOGO ACABA, DAR OS PARABÉNS E VERIFICA SE QUER CONTINUAR OU SAIR
            if fase == 4:
                #VARIAVEL DE CONTROLE
                fase4=True
                # PARANDO DE REPRODUZIR A MUSICA
                fase3.stop()
                #REPETICAO ATÉ O CLIENTE RESPONDER ALGUMA COISA, QUANDO RESPONDE OU VAI SAIR OU VAI VOLTAR PRA FASE 1
                while fase4:
                    #IMPRESSÃO NA TELA DO GAME
                    screen.blit(fase_4, pos_fase_1)
                    screen.blit(voce_venceu, pos_morreu)
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
                                fase = 1
                                timer = 0
                                cont = 0
                                vidas = 3
                                balas = 40
                                perdeu = False
                                gameLooping = True
                                fase4=False
                                fase1.play()

            #Contador de vidas e balas
            if collisions:
                vidas -= 1
                perdeu_vida.play()
                if vidas <= 0:
                    morreu.play()
                    perdeu = True
            if balas <= 0:
                perdeu = True

             # Exibir contadores

            contador = fonteGame.render("Mortes: %i | Balas: %i | Vidas: %i | Fase: %i" % (cont, balas, vidas, fase),True, (255, 255, 255), (0, 0, 0))

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
                screen.blit(funeral, pos_fase_1)
                screen.blit(voce_morreu, pos_morreu)
                pygame.display.update()
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
                            balas = 40
                            perdeu = False
                            gameLooping = True
                            fase1.play()
        #Contador
        screen.blit(contador, pos_contador)
        objectGroup.draw(screen)


        pygame.display.update()







