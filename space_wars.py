import pygame

from pygame.sprite import Group

from settings import Settings

from game_stats import GameStats

from earth import Earth

from moon import Moon

from sun import Sun

from scoreboard import Scoreboard

from button import Button

from pause_message import PauseMessage

from ship import Ship

from alien_boss import AlienBoss

import game_functions as gf

def run_game():
	pygame.init()
	pygame.mixer.music.load('music/Phantom from Space.mp3')
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.5)
	sw_settings = Settings()
	screen = pygame.display.set_mode((sw_settings.screen_width, sw_settings.screen_height))
	pygame.display.set_caption("Earth's Defender")
	earth = Earth(sw_settings, screen)
	moon = Moon(sw_settings, screen)
	sun = Sun(sw_settings, screen) 
	play_button = Button(sw_settings, screen, "Play")
	pause_message = PauseMessage(sw_settings, screen, "Pause")
	game_stats = GameStats(sw_settings)
	scoreboard = Scoreboard(sw_settings, screen, game_stats)
	ship = Ship(sw_settings, screen)
	alien_boss = AlienBoss(sw_settings, screen)
	bullets = Group()
	aliens = Group()
	aliens_bullets = Group()
	asteroids = Group()
	gf.create_fleet(sw_settings, screen, ship, aliens)
	
	while True:
		gf.check_events(sw_settings, screen, game_stats, scoreboard, play_button, pause_message, ship, aliens, bullets, aliens_bullets, asteroids)
		if game_stats.game_active and game_stats.game_pause:
			ship.update()
			gf.update_bullets(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss)
			gf.update_aliens(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
			gf.check_alien_fires(sw_settings, screen, aliens, aliens_bullets)
			gf.update_aliens_bullets(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
			gf.check_asteroid_fall(sw_settings, screen, asteroids)
			gf.update_asteroids(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
			gf.update_alien_boss(sw_settings, screen, game_stats, alien_boss, aliens, aliens_bullets, bullets, asteroids)
		gf.update_screen(sw_settings, screen, earth, moon, sun, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, play_button, pause_message, alien_boss)
run_game()
