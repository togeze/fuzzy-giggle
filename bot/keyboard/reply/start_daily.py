from bot.keyboard.base import BaseReplyKeyboard
from bot.keyboard import button_names


class DailyStartMenuKeyboard(BaseReplyKeyboard):
    def __init__(self):
        super().__init__()
        (self.add_row(button_names.btn_set_time, button_names.btn_daily_start)
         .add_row(button_names.btn_sketches).add_row(button_names.btn_back))
