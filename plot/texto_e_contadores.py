from acoes.cabecalho import *

#CRIANDO CADA TEXTO USADO NO TEXTO, SALVO O CONTADOR

fonteGame=pygame.font.SysFont("data/Vermin_Vibes_1989.ttf",15)
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
pos_instrucoes = instrucoes.get_rect()
pos_instrucoes = (18, 480)
voce_morreu = fonteGame.render("VOCÊ MORREU PRESSIONE 'C' PARA CONTINUAR OU 'S' PARA SAIR", True, (255, 255, 255), (0, 0, 0))
pos_global = voce_morreu.get_rect()
pos_global = (200, 100)
voce_venceu = fonteGame.render("VOCÊ VENCEU! SE DESEJAR JOGAR DE NOVO PRESSIONE [C] PARA SAIR [S]", True, (255, 255, 255), (0, 0, 0))
# Define as fonte que usaremos
fonteGameMENU1 = pygame.font.SysFont("data/Vermin_Vibes_1989.ttf", 25)
fonteGame=pygame.font.SysFont("data/Vermin_Vibes_1989.ttf",15)
fonte_animacao = pygame.font.SysFont("Vermin_Vibes_1989.ttf", 20)
text = fonte_animacao.render("PRESSIONE [E] PARA PULAR A ANIMAÇÂO", True, (255, 255, 255), (0, 0, 0))

##Define variáveis com valores de cor ou coordenada

azul=(108,194,236)
branco=(255,255,255)


#TEXTO MENU
textom1 = fonteGameMENU1.render("START GAME PRESS [S]", True, (255, 255, 255))
textom2 = fonteGameMENU1.render("QUIT GAME PRESS [Q]", True, (255, 255, 255))

