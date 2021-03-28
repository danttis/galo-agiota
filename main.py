import pygame
from pygame.locals import *
from obstaculos import Obstaculos
from personagem import Persona
from municao import Municao
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

# MUSICA DE FUNDO

pygame.mixer.music.load("data/ambiente.wav")
pygame.mixer.music.play(-1)

# SONS DE AÇÕES


# CHAMANDO OBJETO
objectGroup = pygame.sprite.Group()
obstaculosGroup=pygame.sprite.Group()
tiroGroup=pygame.sprite.Group()

#INSTANCIA DO OBJETO
personagem =Persona(objectGroup)

#CONTADOR DE MORTES
cont = 0
font = pygame.font.SysFont('arial black', 15)
contador = font.render("Mortes: ", True, (255, 255, 255), (0, 0, 0))
pos_contador = contador.get_rect()
pos_contador.center = (250, 50)

#Contador de vidas e balas
vidas = 3
balas = 40

#Texto de GameOver
def texto(mensagem, cor):
	textoTela = font.render(mensagem, True, cor)
	screen.blit(textoTela, [750/8, 500/2])

timer = 0
clock = pygame.time.Clock()

if __name__ == "__main__":
    gameLooping=True
    perdeu=False
    while gameLooping:
        #Limitador de FPS
        clock.tick(60)

        pygame.display.flip()
        screen.fill(branco)
        ##Eventos do game

        for event in pygame.event.get():
            ##Quando aperta o X ele exita o pygame
            if event.type ==pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and not perdeu:
                    balas -= 1
                    if balas > 0:
                        newTiro=Municao(objectGroup,tiroGroup)
                        newTiro.rect.center=personagem.rect.center
                    else:
                        perdeu = True



        #Lógica do game em sí

        if not perdeu:
            #Gera Os galo schaves
            objectGroup.update()

            timer += 1
            if timer > 30:
                timer = 0
                if random.random() < 0.3:
                    newObstaculos = Obstaculos(objectGroup,obstaculosGroup)
            #Analisa se tem impacto
            collisions=pygame.sprite.spritecollide(personagem,obstaculosGroup, True, pygame.sprite.collide_mask)
            colliTiro=pygame.sprite.groupcollide(tiroGroup, obstaculosGroup, True, True,pygame.sprite.collide_mask)

            #Conta as mortes
            if  colliTiro :
                cont += 1
            contador = font.render("Mortes: %i | balas: %i | vidas: %i" %(cont, balas, vidas), True, (255, 255, 255), (0, 0, 0))


            if collisions:
                vidas -= 1
                if vidas <= 0:
                    perdeu = True

            if perdeu == True:
                pygame.mixer.music.stop()
            #GAMEOVER
            while perdeu:
                screen.fill([19, 173, 235])
                texto("GAME OVER PRESS D PARA CONTINUAR OU S PARA SAIR", (0,0,0))
                pygame.display.update() 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameLooping=False
                        perdeu=False
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_s:
                            pygame.quit()
                            exit(0)
                        if event.key==pygame.K_d:
                            vidas = 0
                            timer = 0
                            cont = 0
                            vidas = 3
                            balas = 40
                            perdeu = False
                            gameLooping=True
        #Contador
        screen.blit(contador, pos_contador)
        objectGroup.draw(screen)

        ##mouse=pygame.mouse.get_pos()
        ##print(mouse)

        pygame.display.update()







