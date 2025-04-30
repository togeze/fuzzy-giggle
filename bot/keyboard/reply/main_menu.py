from bot.keyboard.base import BaseReplyKeyboard

class MainMenuKeyboard(BaseReplyKeyboard):
    def __init__(self):
        super().__init__()
        self.add_row("Продолжить курс", "Выбрать время").add_row("Мой прогресс")