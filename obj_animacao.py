import pygame
import math
import random

class GaloAnimacao(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.sprites = []
		self.sprites.append(pygame.image.load('data/galo_11.png'))
		self.sprites.append(pygame.image.load('data/galo_22.png'))
		self.galoAtual=0
		self.image = self.sprites[self.galoAtual]
		self.rect = self.image.get_rect()
		self.x=0
		self.rect.topleft = self.x, 300
		
	def update(self):
		self.image = self.sprites[self.galoAtual]
		self.galoAtual += 1
		if self.galoAtual >= len(self.sprites):
			self.galoAtual=0
		self.x+=5
		self.rect.topleft = self.x, 300
		if self.x >= 600:
			self.x=0

class Dinheiro(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('data/bolsaD.png')
		self.image = pygame.transform.scale(self.image , [60,60])
		self.rect = pygame.Rect(50, 50,100,100)
		self.rect.y = 0
		self.rect.x = random.randint(1, 600)
		self.speed = 10 + random.random()*5
		
	def update(self):
		self.rect.y += self.speed
		if self.rect.y >500:
			self.rect.y = 0
			self.rect.x = random.randint(1, 600)