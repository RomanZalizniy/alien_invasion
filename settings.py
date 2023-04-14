class Settings:
    """Клас для збереження налаштувань гри"""

    def __init__(self):
        """Ініціалізувати налаштування гри"""
        
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Налаштування корабля
        self.ship_speed = 1
        self.ship_limit = 3

        #Налаштування кулі
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 12
        self.bullet_color = 'black'
        self.bullet_allowed = 3

        #Налаштування прибульця
        self.alien_speed = 0.5
        self.fleet_drop_speed = 5
        # fleet_direction 1 - рух праворуч, -1 - рух ліворуч
        self.fleet_direction = 1
