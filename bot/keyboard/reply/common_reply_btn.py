from bot.keyboard.base import BaseReplyKeyboard
from bot.keyboard import button_names
#from bot.main import command_sketches_handler

class CommonMenuKeyboard(BaseReplyKeyboard):
    def __init__(self):
        super().__init__()
        (self.add_row(button_names.btn_set_daily)
         .add_row(button_names.btn_draw_now))

    def push_button_set_daily_start(self):
        """ Переходим в это меню, когда:
        1) нажата кнопка 'Настроить ежедневные практики', при этом либо ранее была нажата кнопка 'Остановить ежедневные практики', либо ежедневные практики вообще ещё не запускали.
        2) нажата кнопка 'Остановить ежедневные практики' из меню push_button_set_every_day_stop """
        (self.add_row(button_names.btn_set_time, button_names.btn_daily_start)
         .add_row(button_names.btn_back))
        return self

    def push_button_set_daily_stop(self):
        """ Переходим в это меню, когда нажата кнопка 'Настроить ежедневные практики',
                если ранее уже была нажата кнопка 'Начать ежедневные практики',
                иначе переходим в push_button_set_every_day_start вместо этой ф-ии """
        (self.add_row(button_names.btn_change_time, button_names.btn_daily_stop)
         .add_row(button_names.btn_back))
        return self

    def push_button_draw_daily_start(self):
        """ Переходим в это меню, когда нажата кнопка 'Начать ежедневные практики' """
        (self.add_row(button_names.btn_change_time, button_names.btn_daily_stop)
         .add_row(button_names.btn_back))
        return self
        # каждый день в выбранное время (из push_button_set_every_day_time) присылаем текст Тема дня: ...
        # рандомно выбираем тему из соответствующего столбика таблицы

    def push_button_draw_daily_stop(self):
        """ Переходим в это меню, когда нажата кнопка 'Остановить ежедневные практики' """
        (self.add_row(button_names.btn_set_time, button_names.btn_daily_start)
         .add_row(button_names.btn_back))
        return self
        # останавливаем ежедневные задания из push_button_draw_every_day_start
        # Текст: Ежедневные практики приостановлены. Отдыхайте.

    def push_button_set_daily_time(self):
        """ Переходим сюда, когда нажата кнопка 'Выбрать время' для ежедневных практик.
            Если время не выбрано, по-умолчанию присылаем задания в 6 утра (?) """
        # await message.answer(f"Выберите время ежедневных практик по Москве (UTC+03):", reply_markup=KeyboardFactory.inline_buttons_every_day_time())

    def push_button_draw_now(self):
        """ Переходим в это меню, когда нажата кнопка 'Хочу рисовать прямо сейчас!' """
        (self.add_row(button_names.btn_get_reference, button_names.btn_get_task)
         .add_row(button_names.btn_sketches)
         .add_row(button_names.btn_back))
        return self

    def push_button_reference_now(self):
        """ Переходим сюда, когда нажата кнопка 'Прислать референс' """
        # выбираем одну рандомную картинку из всех папков с референсами на ядиске и присылаем

    def push_button_task_now(self):
        """ Переходим сюда, когда нажата кнопка 'Прислать задание' """
        # выбираем по одному рандомному заданию из столбиков 'что' и 'как' в таблице и присылаем
        # Текст: Что: ...
        #        Как: ...

    def push_button_sketches(self):
        """ Переходим сюда, когда нажата кнопка 'Наброски' """
        sketches_theme = "руки"  # Тема набросков должна рандомно выбираться из названия папок, которые я собрала пока на ядиске
        # await message.answer(f"Ваша тема для набросков: {sketches_theme}!")
        # Выводим inline кнопки с выбором времени
        # await message.answer(f"Выберите время на один набросок:", reply_markup=KeyboardFactory.inline_buttons_sketches_time())
        # Выводим inline кнопки с выбором количества референсов
        # await message.answer(f"Выберите количество набросков:", reply_markup=KeyboardFactory.inline_buttons_sketches_amount())
        # Выводим inline кнопки старт либо изменить время/количество
        # await message.answer(f"Приготовьте свои любимые материалы. N набросков за T минут", reply_markup=KeyboardFactory.inline_buttons_sketches_start())
        # После этого начинаем присылать рандомные картинки из папки с названием sketches_theme (по одному референсу раз в выбранное кол-во минут)
        (self.add_row(button_names.btn_stop_exit))  # по этой кнопке прекращаем присылать фотки и выходим обратно в меню push_button_draw_now
        # await message.answer(f"Наброски окончены. Если есть желание, можете выложить результаты в соцсети с тегом #GigDraw_bot")
        return self
