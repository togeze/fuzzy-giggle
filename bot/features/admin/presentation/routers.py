from bot.core.routers.base_routers import BaseRouter
from aiogram import F, types
from aiogram.filters import Command
from bot.core.services.keyboard_service import KeyboardService


class AdminRouter(BaseRouter):
    def register_handlers(self):
        self.router.message(Command("admin"))(self.admin_handler)

    async def admin_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Админ-панель",
            reply_markup=keyboard_service.get_admin_keyboard()
        )