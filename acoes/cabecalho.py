#CABEÇALHO COM TODAS AS CHAMADA DE FUNÇÕES QUE O JOGO PRECISA cabecalho acoes

import pygame, sys, os
from pygame.locals import *
from objetos_.obstaculos import Obstaculos
from objetos_.personagem import Persona
from objetos_.municao import *
from objetos_.boss import Boss
from acoes.grupos import *
from plot.fundos import *
from plot.imagens import *
from plot.sons import *
from plot.texto_e_contadores import *
from obj_animacao import GaloAnimacao
from obj_animacao import Dinheiro
from barricada import Barricada
import random