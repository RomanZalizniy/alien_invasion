import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """клас для керування кулями випущеними з корабля"""

    def __init__(self, ai_game):
        """Створюємо об'єкт bullet у поточній позиції корабля"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Створюємо форму кулі(rect) (0,0) та задаємо правильну позицію
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Зберігаємо позицію кулю в float
        self.y = float(self.rect.y)


    def update(self):
        """Посунути кулю на верх екрану"""

        #Оновлюємо десяткову позицію кулі
        self.y -= self.settings.bullet_speed
        #Оновлюємо позицію rect
        self.rect.y = self.y


    def draw_bullet(self):
        """Малюємо кулю на екрані гри"""
        pygame.draw.rect(self.screen, self.color, self.rect)