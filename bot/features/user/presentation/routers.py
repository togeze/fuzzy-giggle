from aiogram.types import CallbackQuery

from bot.core.routers.base_routers import BaseRouter
from aiogram import F, types
from aiogram.filters import Command
from bot.core.services.keyboard_service import KeyboardService
from bot.keyboard import button_names


class UserRouter(BaseRouter):
    def register_handlers(self):
        self.router.message(Command("start"))(self.start_handler)
        self.router.message(F.text == button_names.btn_set_daily)(self.start_daily)
        self.router.message(F.text == button_names.btn_sketches)(self.sketches)
        self.router.callback_query(F.data.in_({"3_min", "7_min"}))(self.sketches)

    async def start_handler(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Добро пожаловать!",
            reply_markup=keyboard_service.get_main_keyboard()
        )

    async def start_daily(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "pupupu",
            reply_markup=keyboard_service.get_daily_start_keyboard()
        )

    async def sketches(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Выберите время на один набросок:",
            reply_markup=keyboard_service.get_sketches_keyboard()
        )

    async def inline_time(self, callback: CallbackQuery, is_admin: bool):
        await callback.message.answer("Выберите время на один набросок:")
        await callback.answer()
