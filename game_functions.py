import sys

import pygame

from time import sleep

import random

from bullet import Bullet

from alien import Alien

from alien_bullet import AlienBullet

from asteroid import Asteroid

def check_keydown_events(event, sw_settings, screen, game_stats, scoreboard, play_button, pause_message, ship, aliens, bullets, aliens_bullets, asteroids):
	if event.key == pygame.K_RIGHT:
	    ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(sw_settings, screen, ship, bullets)
	elif event.key == pygame.K_PAUSE:
		game_stats.game_pause = False
		pygame.mixer.music.set_volume(0.5)
		while game_stats.game_pause:
			sleep(1)
			check_events(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids)
	elif event.key == pygame.K_ESCAPE:
		game_stats.game_pause = True
		pygame.mixer.music.set_volume(1)
	elif event.key == pygame.K_q:
		with open('recordscore.txt', 'w') as file_object:
			file_object.write(str(game_stats.high_score))
		sys.exit()
	elif event.key == pygame.K_p and not game_stats.game_active:
		start_game(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids)
		
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(sw_settings, screen, game_stats, scoreboard, play_button, pause_message, ship, aliens, bullets, aliens_bullets, asteroids):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, sw_settings, screen, game_stats, scoreboard, play_button, pause_message, ship, aliens, bullets, aliens_bullets, asteroids)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
def check_play_button(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not game_stats.game_active:
		start_game(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids)
		
def start_game(sw_settings, screen, game_stats, scoreboard, play_button, ship, aliens, bullets, aliens_bullets, asteroids):
	sw_settings.initialize_dynamic_settings()
	pygame.mixer.music.set_volume(1)
	pygame.mouse.set_visible(False)
	game_stats.reset_stats()
	game_stats.game_active = True
		
	scoreboard.prep_images()
		
	aliens.empty()
	bullets.empty()
	aliens_bullets.empty()
	asteroids.empty()
		
	create_fleet(sw_settings, screen, ship, aliens)
	
	ship.center_ship()
	
def check_asteroid_fall(sw_settings, screen, asteroids):
	random_fall = random.randint(0, 10000)
	if random_fall < 3:
		asteroid_fall(sw_settings, screen, asteroids)
		
def asteroid_fall(sw_settings, screen, asteroids):
	asteroid = Asteroid(sw_settings, screen)
	asteroids.add(asteroid)
	
def update_asteroids(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	asteroids.update()
	screen_rect = screen.get_rect()
	for asteroid in asteroids.copy():
		if asteroid.rect.top == screen_rect.bottom:
			asteroids.remove(asteroid)
	check_asteroid_ship_collision(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
	check_asteroid_alien_collision(sw_settings, screen, asteroids, aliens)
	check_asteroid_bullets_collision(sw_settings, screen, asteroids, bullets, aliens_bullets)

def check_asteroid_ship_collision(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	if pygame.sprite.spritecollideany(ship, asteroids):
		ship_hit(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
		
def check_asteroid_alien_collision(sw_settings, screen, aliens, asteroids):
	asteroid_alien_collsion = pygame.sprite.groupcollide(asteroids, aliens, True, False)
	
def check_asteroid_bullets_collision(sw_settings, screen, asteroids, bullets, aliens_bullets):
	asteroid_bullet_collsion = pygame.sprite.groupcollide(asteroids, bullets, False, True)
	asteroid_alien_bullet_collision = pygame.sprite.groupcollide(asteroids, aliens_bullets, False, True)

def fire_bullet(sw_settings, screen, ship, bullets):
	if len(bullets) < sw_settings.bullets_allowed:
		new_bullet = Bullet(sw_settings, screen, ship)
		bullets.add(new_bullet)
			
def update_bullets(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss):
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, asteroids, aliens_bullets, alien_boss)
	check_bullets_bullets_collision(sw_settings, screen, bullets, aliens_bullets)
	if game_stats.level == 2:
		if len(aliens) == 0:
			check_bullets_alien_boss_collision(sw_settings, screen, bullets, alien_boss, game_stats, aliens_bullets, asteroids, scoreboard, ship, aliens)
	
def check_alien_fires(sw_settings, screen, aliens, aliens_bullets):
	aliens_fires = random.randint(0, 350)
	if len(aliens) != 0:
		if aliens_fires < 2:
			fire_alien_bullet(sw_settings, screen, aliens, aliens_bullets)
	
def fire_alien_bullet(sw_settings, screen, aliens, aliens_bullets):
	alien_y_values = [alien.rect.y for alien in aliens.sprites()]
	max_alien_y = max(alien_y_values)
	bottom_aliens = []
	for alien in aliens.sprites():
		if alien.rect.y == max_alien_y:
			bottom_aliens.append(alien)
	for alien in bottom_aliens:
		new_alien_bullet = AlienBullet(sw_settings, screen, alien)
		aliens_bullets.add(new_alien_bullet)
	
def update_aliens_bullets(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	aliens_bullets.update()
	screen_rect = screen.get_rect()
	for alien_bullet in aliens_bullets.copy():
		if alien_bullet.rect.top == screen_rect.bottom:
			aliens_bullets.remove(alien_bullet)
	check_bullet_ship_collisions(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
	check_bullets_bullets_collision(sw_settings, screen, bullets, aliens_bullets)
	
def check_bullet_ship_collisions(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	if pygame.sprite.spritecollideany(ship, aliens_bullets):
		ship_hit(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
		
def check_bullets_bullets_collision(sw_settings, screen, bullets, aliens_bullets):
	bullets_bullets_collision = pygame.sprite.groupcollide(bullets, aliens_bullets, True, True)
			
def check_bullet_alien_collisions(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss):
	colisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if colisions:
		for aliens in colisions.values():
			game_stats.score += sw_settings.alien_points * len(aliens)
		scoreboard.prep_score()
		check_high_score(game_stats, scoreboard)
	if game_stats.level != 2:
		if len(aliens) == 0:
			start_new_level(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss)
			
def check_bullets_alien_boss_collision(sw_settings, screen, bullets, alien_boss, game_stats, aliens_bullets, asteroids, scoreboard, ship, aliens):
	collision = pygame.sprite.spritecollide(alien_boss, bullets, False)
	if collision:
		start_new_level(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss)
		
def start_new_level(sw_settings, screen, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, alien_boss):
	bullets.empty()
	aliens_bullets.empty()
	asteroids.empty()
	sw_settings.increase_speed()
	game_stats.level += 1
	scoreboard.prep_level()
	create_fleet(sw_settings, screen, ship, aliens)
	sleep(0.5)
	
def update_alien_boss(sw_settings, screen, game_stats, alien_boss, aliens, aliens_bullets, bullets, asteroids):
	check_alien_boss_edges(sw_settings, alien_boss)
	alien_boss.update()
	
def check_alien_boss_edges(sw_settings, alien_boss):
	if alien_boss.alien_boss_check_edges():
		change_alien_boss_direction(sw_settings, alien_boss)
		
def change_alien_boss_direction(sw_settings, alien_boss):
	alien_boss.rect.y += sw_settings.alien_boss_drop_speed
	sw_settings.alien_boss_direction *= -1
	
def check_high_score(game_stats, scoreboard):
	if game_stats.score > game_stats.high_score:
		game_stats.high_score = game_stats.score
		scoreboard.prep_high_score()

def get_number_aliens_x(sw_settings, alien_width):
	avialable_space_x = sw_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avialable_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(sw_settings, ship_height, alien_height):
	avialable_space_y = (sw_settings.screen_height - (2 * alien_height) - ship_height)
	number_rows = int(avialable_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(sw_settings, screen, aliens, alien_number, row_number):
	alien = Alien(sw_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def create_fleet(sw_settings, screen, ship, aliens):
	alien = Alien(sw_settings, screen)
	number_aliens_x = get_number_aliens_x(sw_settings, alien.rect.width)
	number_rows = get_number_rows(sw_settings, ship.rect.height, alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(sw_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(sw_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(sw_settings, aliens)
			break
			
def change_fleet_direction(sw_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += sw_settings.fleet_drop_speed
	sw_settings.fleet_direction *= -1
	
def ship_hit(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	if game_stats.ships_left > 0:
		game_stats.ships_left -= 1
		scoreboard.prep_ships()
		aliens.empty()
		bullets.empty()
		aliens_bullets.empty()
		asteroids.empty()
	
		create_fleet(sw_settings, screen, ship, aliens)
		ship.center_ship()
	
		sleep(1)
	else:
		game_stats.game_active = False
		pygame.mouse.set_visible(True)
		pygame.mixer.music.set_volume(0.5)
	
def check_aliens_bottom(sw_settings, game_stats, scoreboard, screen, ship, aliens, aliens_bullets, bullets, asteroids):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
			break
			
def update_aliens(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids):
	check_fleet_edges(sw_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(sw_settings, game_stats, scoreboard, screen, ship, aliens, bullets, aliens_bullets, asteroids)
	check_aliens_bottom(sw_settings, game_stats, scoreboard, screen, ship, aliens, aliens_bullets, bullets, asteroids)
	
def update_screen(sw_settings, screen, earth, moon, sun, game_stats, scoreboard, ship, aliens, bullets, aliens_bullets, asteroids, play_button, pause_message, alien_boss):
	screen.fill(sw_settings.bg_color)
	earth.show_earth()
	moon.show_moon()
	sun.show_sun()
	for alien_bullet in aliens_bullets.sprites():
		alien_bullet.draw_alien_bullet()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	if game_stats.level == 2:
		aliens.empty()
		if len(aliens) == 0:
			alien_boss.blitme()
	aliens.draw(screen)
	for asteroid in asteroids.sprites():
		asteroid.blitme()
	scoreboard.show_score()
	if not game_stats.game_active:
		play_button.draw_button()
	if not game_stats.game_pause:
		pause_message.draw_pause_message()
	
	pygame.display.flip()
