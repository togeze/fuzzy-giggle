from bot.keyboard.base import BaseInlineKeyboard

class CommonInlineKeyboard(BaseInlineKeyboard):
    def __init__(self):
        super().__init__()

    def inline_buttons_daily_time(self):
        """ Выводим эти значки, когда нажата кнопка 'Выбрать время' для ежедневных практик """
        self.add_row(("00:00", "0_hour"), ("01:00", "1_hour"), ("02:00", "2_hour"), ("03:00", "3_hour"))
        self.add_row(("04:00", "4_hour"), ("05:00", "5_hour"), ("06:00", "6_hour"), ("07:00", "7_hour"))
        self.add_row(("08:00", "8_hour"), ("09:00", "9_hour"), ("10:00", "10_hour"), ("11:00", "11_hour"))
        self.add_row(("12:00", "12_hour"), ("13:00", "13_hour"), ("14:00", "14_hour"), ("15:00", "15_hour"))
        self.add_row(("16:00", "16_hour"), ("17:00", "17_hour"), ("18:00", "18_hour"), ("19:00", "19_hour"))
        self.add_row(("20:00", "20_hour"), ("21:00", "21_hour"), ("22:00", "22_hour"), ("23:00", "23_hour"))
        return self

    def inline_buttons_sketches_time(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' """
        self.add_row(("3 мин", "3_min"), ("5 мин", "5_min"), ("7 мин", "7_min"), ("10 мин", "10_min"))
        return self

    def inline_buttons_sketches_amount(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' и было выбрано время в inline_buttons_time """
        self.add_row(("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"))
        return self

    def inline_buttons_sketches_fix_time(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' и 'Изменить время' """
        self.add_row(("3 мин", "3_min_fix"), ("5 мин", "5_min_fix"), ("7 мин", "7_min_fix"), ("10 мин", "10_min_fix"))
        return self

    def inline_buttons_sketches_start(self):
        """ Выводим эти значки, когда нажата кнопка 'Наброски' и было выбрано время в inline_buttons_time и кол-во inline_buttons_sketches_amount """
        self.add_row(("▶️ Начать", "start_sketches"))
        self.add_row(("Изменить время", "fix_sketches_time"))
        self.add_row(("Изменить количество", "fix_sketches_amount"))
        return self