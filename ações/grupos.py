from ações.cabeçarios import *

# CHAMANDO OBJETO
objectGroup = pygame.sprite.Group()
obstaculosGroup=pygame.sprite.Group()
tiroGroup=pygame.sprite.Group()
tiro_bossGroup = pygame.sprite.Group()
barreira = pygame.sprite.Group()
#INSTANCIA DO OBJETO
personagem = Persona(objectGroup)
boss = Boss(objectGroup)
#Animação dados
galoInicio = pygame.sprite.Group()
dinheiro = pygame.sprite.Group()
dinheiro2 = pygame.sprite.Group()
