from bot.core.routers.base_routers import BaseRouter
from aiogram import F, types
from aiogram.filters import Command
from bot.core.services.keyboard_service import KeyboardService


class UserRouter(BaseRouter):
    def register_handlers(self):
        self.router.message(Command("start"))(self.start_handler)

    async def start_handler(self, message: types.Message, is_admin: bool):
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Добро пожаловать!",
            reply_markup=keyboard_service.get_main_keyboard()
        )