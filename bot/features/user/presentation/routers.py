from xmlrpc.client import DateTime

from aiogram.types import CallbackQuery, FSInputFile

from bot.core.routers.base_routers import BaseRouter
from aiogram import F, types
from aiogram.filters import Command
from bot.core.services.keyboard_service import KeyboardService
from bot.keyboard import button_names
from bot.core.services.task_service import TaskService


class UserRouter(BaseRouter):
    def __init__(self, task_service: TaskService):
        super().__init__()
        self.task_service = task_service
        self.register_handlers()

    def register_handlers(self):
        self.router.message(Command("start"))(self.start_handler)
        self.router.message(Command("info"))(self.info_about)
        self.router.message(F.text == button_names.btn_set_daily)(self.set_daily_start)
        self.router.message(F.text == button_names.btn_set_time)(self.set_daily_time)
        self.router.message(F.text == button_names.btn_change_time)(self.set_daily_time)
        self.router.message(F.text == button_names.btn_daily_start)(self.daily_start)
        self.router.message(F.text == button_names.btn_daily_stop)(self.daily_stop)
        self.router.message(F.text == button_names.btn_draw_now)(self.set_draw_now)
        self.router.message(F.text == button_names.btn_sketches)(self.set_sketches)
        self.router.message(F.text == button_names.btn_get_reference)(self.get_reference)
        self.router.message(F.text == button_names.btn_get_task)(self.get_task)
        self.router.message(F.text == button_names.btn_stop_exit)(self.stop_sketches)
        self.router.message(F.text == button_names.btn_back)(self.back)
        # прислать ежедневное задание: self.send_daily_task
        # когда наброски закончились: self.end_sketches
        self.router.callback_query(F.data.in_({"fix_sketches_time"}))(self.inline_get_fix_time)
        self.router.callback_query(F.data.in_({"fix_sketches_amount"}))(self.inline_fix_amount)
        self.router.callback_query(F.data.in_({"start_sketches"}))(self.inline_start_sketches)
        self.router.callback_query(F.data.in_({"3_min", "5_min", "7_min", "10_min"}))(self.inline_time)
        self.router.callback_query(F.data.in_({"3_min_fix", "5_min_fix", "7_min_fix", "10_min_fix"}))(self.inline_fix_time)
        self.router.callback_query(F.data.in_({"3", "4", "5", "6", "7"}))(self.inline_amount)
        self.router.callback_query(F.data.in_({"0_hour", "1_hour", "2_hour", "3_hour", "4_hour", "5_hour", "6_hour", "7_hour", "8_hour", "9_hour",
                                               "10_hour", "11_hour", "12_hour", "13_hour", "14_hour", "15_hour", "16_hour", "17_hour", "18_hour",
                                               "19_hour", "20_hour", "21_hour", "22_hour", "23_hour"}))(self.inline_daily_time)

    async def start_handler(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        user_repo = self.task_service.user_repo
        current_username = message.from_user.username

        user = await user_repo.get_by_telegram_id(message.from_user.id)

        if not user:
            user = await user_repo.create_user(
                telegram_id=message.from_user.id,
                username=current_username,
                is_admin=is_admin
            )
        else:
            if user.username != current_username:
                await user_repo.update_user(
                    user,
                    username=current_username,
                    is_admin=is_admin or user.is_admin
                )
        how_task, what_task = await user_repo.get_random_task_pair(user)
        print(f"What: {what_task.text}\nHow: {how_task.text}")
        await message.answer(
            "Добро пожаловать!",
            reply_markup=keyboard_service.get_main_keyboard()
        )

    async def info_about(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Это бот помогает поддерживать мотивацию для ежедневного рисования, а также предлагает нескучные задания или идеи, когда желание рисовать "
            "возникло прямо сейчас. \n\nРезультаты можно выкладывать в соцсети с хэштегом #gigdrawbot \n\nВопросы, пожелания и предложения присылайте на почту "
            "gigdraw123@gmail.com \n\nЕсли есть желание, можно поддержать авторов донатом",
            reply_markup=keyboard_service.get_main_keyboard()
        )

    async def set_daily_start(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "pupupu",
            reply_markup=keyboard_service.get_daily_start_keyboard()
        )

    async def set_draw_now(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "pupupu",
            reply_markup=keyboard_service.get_draw_now_keyboard()
        )

    async def set_daily_stop(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "pupupu",
            reply_markup=keyboard_service.get_daily_stop_keyboard()
        )

    async def set_sketches(self, message: types.Message, is_admin: bool):
        sketches_theme = self.get_sketches_theme()
        keyboard_service = KeyboardService(is_admin)
        await message.answer(f"Ваша тема для набросков - {sketches_theme}")
        await message.answer(
            "Выберите время на один набросок:",
            reply_markup=keyboard_service.get_sketches_time_keyboard()
        )

    def get_sketches_theme(self):
        sketches_theme = "здесь будет рандомная тема для набросков"  # Тема набросков должна рандомно выбираться из названия папок, которые я собрала пока на ядиске
        return sketches_theme

    async def get_reference(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        photo_path = self.get_random_image()
        await message.answer_photo(  # выбираем одну рандомную картинку из всех папков с референсами на ядиске и присылаем
             photo=FSInputFile("data/6.jpeg"), caption="Здесь будет рандомный референс"
        )

    async def get_task(self, message: types.Message, is_admin: bool):
        await message.answer("Задания временно отсутствуют")

    async def daily_start(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Будем присылать задание ежедневно в hh:mm",
            reply_markup=keyboard_service.get_daily_stop_keyboard()
        )

    async def daily_stop(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(  # выбранное время ежедневных практик не сбрасывать
            "Ежедневные практики приостановлены. Отдыхайте ❤️",
            reply_markup=keyboard_service.get_daily_start_keyboard()
        )

    async def send_daily_task(self, message: types.Message, is_admin: bool):
        """ Вызывается когда пора присылать ежедневное задание """
        keyboard_service = KeyboardService(is_admin)
        daily_theme = self.get_daily_theme()
        await message.answer(
            f"Тема дня: {daily_theme}"
        )

    def get_daily_theme(self):
        daily_theme = "здесь будет новая тема на день"  # рандомно выбираем тему дня из соответствующего столбика таблицы
        return daily_theme

    async def set_daily_time(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(  #  если время не выбрано, по-умолчанию присылаем задания в 6 утра (?)
            "Выберите время по Москве (UTC+03) для ежедневных практик:",
            reply_markup=keyboard_service.get_daily_time_keyboard()
        )

    async def inline_daily_time(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        time_ = int(callback.data[:-5])
        print("Время практик = ",  time_, ": 00, id = ", callback.from_user.id)
        await callback.message.answer(
            f"Выбранное время {time_}:00")
        await callback.answer()

    async def inline_time(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        time_ = int(callback.data[:-4])
        print("Время = ",  time_, "мин, id = ", callback.from_user.id)
        await callback.message.answer(
            "Выберите количество набросков:",
            reply_markup=keyboard_service.get_sketches_amount_keyboard()
        )
        await callback.answer()

    async def inline_fix_time(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        time_ = int(callback.data[:-8])
        print("Время = ", time_, "мин, id = ", callback.from_user.id)
        await callback.message.answer(
            "Приготовьте свои любимые материалы!\nБудет N набросков раз в T минут",
            reply_markup=keyboard_service.get_start_sketches_keyboard()
        )
        await callback.answer()

    async def inline_get_fix_time(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await callback.message.answer(
            "Выберите время на один набросок:",
            reply_markup=keyboard_service.get_sketches_fix_time_keyboard()
        )

    async def inline_amount(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        amount_ = int(callback.data)
        print("Количество = ",  amount_, ", id = ", callback.from_user.id)
        # await callback.message.answer(f"Количество = {amount_}")
        await callback.message.answer(
            "Приготовьте свои любимые материалы!\nБудет N набросков раз в T минут",
            reply_markup=keyboard_service.get_start_sketches_keyboard()
        )
        await callback.answer()

    async def inline_fix_amount(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await callback.message.answer("Выберите количество набросков:", reply_markup=keyboard_service.get_sketches_amount_keyboard())
        await callback.answer()

    async def inline_start_sketches(self, callback: CallbackQuery, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await callback.message.answer(
            "Здесь будут присылаться картинки для выбранной темы N штук раз в T минут",
            reply_markup=keyboard_service.get_stop_sketches_keyboard()
        )

    async def stop_sketches(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Наброски остановлены",
                 reply_markup=keyboard_service.get_draw_now_keyboard()
        )

    async def end_sketches(self, message: types.Message, is_admin: bool):
        """ Эта ф-ия запускается, когда наброски кончились сами, их не прервали кнопкой btn_stop_exit """
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Наброски окончены. Если есть желание, можете выложить результаты в соцсети с тегом #gigdrawbot",
            reply_markup=keyboard_service.get_draw_now_keyboard()
        )

    async def back(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "pupupu",
                 reply_markup=keyboard_service.get_main_keyboard()
        )