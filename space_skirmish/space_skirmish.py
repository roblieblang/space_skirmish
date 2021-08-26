import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from laser import Laser
from enemy import Enemy


class enemyInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1024, 768))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Space Skirmish")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.lasers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_lasers()
                self._update_enemies()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.enemies.empty()
            self.lasers.empty()
            
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_laser()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_laser(self):
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_lasers(self):
        self.lasers.update()

        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                 self.lasers.remove(laser)

        self._check_laser_enemy_collisions()

    def _check_laser_enemy_collisions(self):
        collisions = pygame.sprite.groupcollide(
                self.lasers, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.enemies:
            self.lasers.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_enemies(self):
        self._check_fleet_edges()
        self.enemies.update()

        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self._ship_hit()
        self._check_enemies_bottom()

    def _check_enemies_bottom(self):
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.enemies.empty()
            self.lasers.empty()

            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width - (2 * enemy_width)
        number_enemies_x = available_space_x // (2 * enemy_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * enemy_height) - ship_height)
        number_rows = available_space_y // (2 * enemy_height)
        
        for row_number in range(number_rows):
            for enemy_number in range(number_enemies_x):
                self._create_enemy(enemy_number, row_number)

    def _create_enemy(self, enemy_number, row_number):
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
        self.enemies.add(enemy)

    def _check_fleet_edges(self):
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(pygame.image.load('images/background.bmp'), (0,0))
        self.ship.blitme()
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.enemies.draw(self.screen)

        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = enemyInvasion()
    ai.run_game()
