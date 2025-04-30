from keyboards.base import BaseReplyKeyboard

class MainMenuKeyboard(BaseReplyKeyboard):
    def __init__(self):
        super().__init__()
        self.add_buttons_row(["Продолжить курс", "Выбрать время"])
            .add_button("Мой прогресс")