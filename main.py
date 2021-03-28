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

# CARREGANDO TODAS AS MÚSICAS

menu = pygame.mixer.Sound("data/background_menu.wav")
fase1 = pygame.mixer.Sound("data/background_fase1.wav")
fase2 = pygame.mixer.Sound("data/background_fase2.wav")
fase3 = pygame.mixer.Sound("data/background_fase3.wav")
fase1.play()

# SONS DE AÇÕES
tiro = pygame.mixer.Sound("data/tiro.wav")
morreu = pygame.mixer.Sound("data/morreu.wav")
dano = pygame.mixer.Sound("data/dano.wav")
perdeu_vida = pygame.mixer.Sound("data/perdeu_vida.wav")

# CHAMANDO OBJETO
objectGroup = pygame.sprite.Group()
obstaculosGroup=pygame.sprite.Group()
tiroGroup=pygame.sprite.Group()

#INSTANCIA DO OBJETO
personagem =Persona(objectGroup)

#CONTADOR DE MORTES
fase = 1
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

# LIMITANDO FPS
timer = 0
clock = pygame.time.Clock()

if __name__ == "__main__":
    gameLooping=True
    perdeu=False
    while gameLooping:
        #LIMITADOR DE FPS
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
                    tiro.play()
                    balas -= 1
                    newTiro=Municao(objectGroup,tiroGroup)
                    newTiro.rect.center=personagem.rect.center




        #Lógica do game em sí

        if not perdeu:
            #Gera Os galo schaves
            objectGroup.update()

            # DEFININDO APARIÇÃO DOS OBSTACULOS
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
                dano.play()


            # CONTADOR DE FASES

            if cont == 20:
                fase = 2
                balas = 40

            if fase == 2:
                fase1.stop()
                fase2.play()

            if cont == 40:
                fase = 3
                balas = 20
            if fase == 3:
                fase2.stop()
                fase3.play()

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

            contador = font.render("Mortes: %i | Balas: %i | Vidas: %i | Fase: %i" % (cont, balas, vidas, fase),True, (255, 255, 255), (0, 0, 0))

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
                screen.fill([19, 173, 235])
                texto("VOCÊ MORREU PRESSIONE 'C' PARA CONTINUAR OU 'S' PARA SAIR", (0,0,0))
                pygame.display.update() 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameLooping=False
                        perdeu=False
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_s:
                            pygame.quit()
                            exit(0)
                        if event.key==pygame.K_c:
                            fase = 1
                            vidas = 0
                            timer = 0
                            cont = 0
                            vidas = 3
                            balas = 40
                            perdeu = False
                            gameLooping=True
                            fase1.play()
        #Contador
        screen.blit(contador, pos_contador)
        objectGroup.draw(screen)

        ##mouse=pygame.mouse.get_pos()
        ##print(mouse)

        pygame.display.update()







