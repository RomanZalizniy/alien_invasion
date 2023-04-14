import pygame

class Ship:
    """Клас керування корабле"""
    
    def __init__(self, ai_game):
        """Ініціалізуємо корабель та задаємо йому початкову позицію"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Завантажити зображення корабля та отримати його rect
        self.image = pygame.image.load('images/ship2.bmp')
        self.rect = self.image.get_rect()

        # Створювати кожен новий корабель внизу екрану, по центру
        self.rect.midbottom = self.screen_rect.midbottom

        #Додаємо дробове значення для позиції нашого корабля
        self.x = float(self.rect.x)

        #Індикатори руху
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """
        Оновити поточне розташування корабля
        на основі індикаторів руху.
        """
        #Оновлюємо значення self.x а не rect(розташування)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:        
            self.x -= self.settings.ship_speed

        #Оновлюємо self.rect.x з self.x
        self.rect.x = self.x


    def blitme(self):
        """Намалювати корабель у його поточному розташуванні"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Ставимо корабель на центр"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)