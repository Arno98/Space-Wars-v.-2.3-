import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	
	def __init__(self, sw_settings, screen, ship):
		super(Bullet, self).__init__()
		self.screen = screen
		self.sw_settings = sw_settings
		
		self.rect = pygame.Rect(0, 0, self.sw_settings.bullet_width, self.sw_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		self.y = float(self.rect.y)
		
		self.color = self.sw_settings.bullet_color
	
	def update(self):
		self.y -= self.sw_settings.bullet_speed_factor
		self.rect.y = self.y
		
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
