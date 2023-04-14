import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Загальний клас, який керує ресурсами та поведінкою гри."""

    def __init__(self):
        """Ініціалізуємо гру та створюємо ресурси гри."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #Створюємо екземпляр класу статистики гри
        self.stats = GameStats(self)

        self.ship = Ship(self)
        #створюємо групу куль
        self.bullets = pygame.sprite.Group()

        #створюємо групу Нло
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """Розпочати головний цикл гри."""
        while True:

            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()


    def _check_events(self):
        """Реагувати на натискання клавіш та дії мишки"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)


    #Рефакторинг методу _check_events(self): на 2 допоміжні методи
    def _check_keydown_events(self, event):
        """Метод реагування на натискання клавіш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Метод реагування коли клавіші не натиснуті"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Створюємо нову кулю та додаємо її до нашої групи"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _update_bullets(self):
        """Оновлюємо позиції куль та видаляємо старі"""
        #Оновлюємо позицію кулі
        self.bullets.update()

        #Видаляємо кулі які перетнули екран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
     

    def _check_bullet_alien_collisions(self):
        #Перевіряємо чи rect кулі = rect прибульця
        #якщо = то видаляємо обох кандидатів
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        """Створюємо флот прибульців"""
        #створюємо прибульців та визначаємо їх кількість на екрані по х
        #Відстань між прибульцями = ширині 1 прибульця
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Визначаємо скільки рядів НЛО вміститься на екран
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Створити ряди з флотом
        for row_number in range(number_rows):
            if row_number <= 3:
            #Створюємо перший ряд прибульців
                for alien_number in range(number_aliens_x):
                    self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Створюємо прибульця та ставимо його в ряд"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_aliens(self):
        """Оновити позиції всіх прибульців"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
    

    def _check_fleet_edges(self):
        """Реагує на те чи прибулець дійшов до краю екрану"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Спускаємо наш флот до низу та міняємо напрямок"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Оновити зображення на екрані та переключатись на новий екран"""

        # Наново перемалювати екран на кожній ітерації циклу
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()    

        #малюємо кулі на екрані
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)        

        # Показати останній намальований екран.
        pygame.display.flip()            


    def _ship_hit(self):
        """Реагування на підбиття корабля"""
        #Зменшуємо ships_left
        self.stats.ships_left -= 1

        #Видаляємо всіх прибульців та кулі які залишились на екрані
        self.aliens.empty()
        self.bullets.empty()

        #Створюємо заново флот на ставимо ship по центру
        self._create_fleet()
        self.ship.center_ship()

        #Ставимо гру на паузу щоб користувач оговтався
        sleep(1)


if __name__ == "__main__":
    # Сворити екземпляр гри(класу) та запустити гру(функцію).
    ai = AlienInvasion()
    ai.run_game()
