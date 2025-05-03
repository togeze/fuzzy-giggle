from bot.keyboard.base import BaseReplyKeyboard
from bot.keyboard import button_names
#from bot.main import command_sketches_handler

class CommonMenuKeyboard(BaseReplyKeyboard):
    def __init__(self):
        super().__init__()

    def push_button_main_menu(self):
        (self.add_row(button_names.btn_set_daily)
         .add_row(button_names.btn_draw_now))
        return self

    def push_button_set_daily_start(self):
        """ Переходим в это меню, когда:
        1) нажата кнопка 'Настроить ежедневные практики', при этом либо ранее была нажата кнопка 'Остановить ежедневные практики', либо ежедневные практики вообще ещё не запускали.
        2) нажата кнопка 'Остановить ежедневные практики' """
        (self.add_row(button_names.btn_set_time, button_names.btn_daily_start)
         .add_row(button_names.btn_back))
        return self

    def push_button_set_daily_stop(self):
        """ Переходим в это меню, когда нажата кнопка 'Начать ежедневные практики';
                либо 'Настроить ежедневные практики',
                если ранее уже была нажата кнопка 'Начать ежедневные практики',
                иначе переходим в push_button_set_every_day_start вместо этой ф-ии """
        (self.add_row(button_names.btn_change_time, button_names.btn_daily_stop)
         .add_row(button_names.btn_back))
        return self

    def push_button_draw_now(self):
        """ Переходим в это меню, когда нажата кнопка 'Хочу рисовать прямо сейчас!' """
        (self.add_row(button_names.btn_get_reference, button_names.btn_get_task)
         .add_row(button_names.btn_sketches)
         .add_row(button_names.btn_back))
        return self

    def push_button_stop_sketches(self):
        """ Переходим в это меню, когда нажата кнопка 'Начать' в набросках """
        (self.add_row(button_names.btn_stop_exit))  # по этой кнопке прекращаем присылать фотки и выходим обратно в меню push_button_draw_now
        return self
