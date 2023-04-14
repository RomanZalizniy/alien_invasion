class GameStats:
    """Відстежуємо статистику гри"""

    def __init__(self, ai_game):
        """Ініціюємо статистику"""
        
        self.settings = ai_game.settings
        self.reset_stats()


    def reset_stats(self):
        """Статистика яка може змінюватись під час гри"""
        self.ships_left = self.settings.ship_limit