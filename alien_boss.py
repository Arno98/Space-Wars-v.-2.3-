import pygame

class AlienBoss():
	
	def __init__(self, sw_settings, screen):
		self.sw_settings = sw_settings
		self.screen = screen
		
		self.image = pygame.image.load('images/boss.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		self.rect.top = self.screen_rect.top
		self.rect.centerx = self.screen_rect.centerx
		
		self.x = float(self.rect.x)
		
	def alien_boss_check_edges(self):
		if self.rect.right >= self.screen_rect.right:
			return True
		if self.rect.left <= 0:
			return True
			
	def update(self):
		self.x += (self.sw_settings.alien_boss_speed_factor * self.sw_settings.alien_boss_direction)
		self.rect.x = self.x
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
			
	
			
