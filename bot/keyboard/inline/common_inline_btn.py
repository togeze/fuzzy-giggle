from bot.keyboard.base import BaseInlineKeyboard

class CommonInlineKeyboard(BaseInlineKeyboard):
    def __init__(self):
        super().__init__()

    def inline_buttons_every_day_time(self):
        """ Выводим эти значки, когда нажата кнопка 'Выбрать время' для ежедневных практик """
        self.add_row(("00:00", "0_hour"), ("01:00", "1_hour"), ("09:00", "9_hour"), ("15:00", "15_hour"))
        return self

    def inline_buttons_sketches_time(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' """
        self.add_row(("3 мин", "3_min"), ("5 мин", "5_min"), ("7 мин", "7_min"), ("10 мин", "10_min"))
        return self

    def inline_buttons_sketches_amount(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' и было выбрано время в inline_buttons_time """
        self.add_row(("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"))
        return self

    def inline_buttons_sketches_start(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' и было выбрано время в inline_buttons_time и кол-во inline_buttons_sketches_amount"""
        self.add_row(("▶️ Начать", "start_sketches"))
        self.add_row(("Изменить время", "fix_sketches_time"))
        self.add_row(("Изменить количество", "fix_sketches_amount"))
        return self