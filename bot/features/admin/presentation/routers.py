from bot.core.routers.base_routers import BaseRouter
from aiogram import F, types
from aiogram.filters import Command
from bot.core.services.keyboard_service import KeyboardService
from bot.core.services.task_service import TaskService


class AdminRouter(BaseRouter):
    def __init__(self, task_service: TaskService):
        super().__init__()
        self.task_service = task_service
        self.register_handlers()

    def register_handlers(self):
        self.router.message(Command("admin"))(self.admin_handler)
        self.router.message(Command("add_category"))(self.add_category_handler)
        self.router.message(Command("get_categories"))(self.get_categories_handler)
        self.router.message(Command("add_what"))(self.add_what_handler)
        self.router.message(Command("add_how"))(self.add_how_handler)

    async def admin_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Админ-панель",
            reply_markup=keyboard_service.get_admin_keyboard()
        )

    async def add_category_handler(self, message: types.Message):
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            return await message.answer(
                "❌ Неправильный формат команды.\n"
                "Используйте: /add_category <тип> <название>\n"
                "Пример: /add_category what Животные"
            )

        _, category_type, category_name = command_parts
        response = await self.task_service.add_category(
            user_id=message.from_user.id,
            category_type=category_type,
            name=category_name
        )
        await message.answer(response)

    async def get_categories_handler(self, message: types.Message):
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            return await message.answer(
                "❌ Неправильный формат команды.\n"
                "Используйте: /get_categories <тип>\n"
                "Пример: /get_categories what"
            )

        _, category_type = command_parts
        response = await self.task_service.get_categories(
            user_id=message.from_user.id,
            category_type=category_type
        )
        await message.answer(response)

    async def add_what_handler(self, message: types.Message):
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            return await message.answer(
                "❌ Неправильный формат команды.\n"
                "Используйте: /add_what <категория> <текст задания>\n"
                "Пример: /add_what Животные Нарисовать кота в стиле кубизма"
            )

        _, category_name, task_text = command_parts
        response = await self.task_service.add_what_task(
            user_id=message.from_user.id,
            category_name=category_name,
            task_text=task_text
        )
        await message.answer(response)

    async def add_how_handler(self, message: types.Message):
        command_parts = message.text.split(maxsplit=2)
        if len(command_parts) < 3:
            return await message.answer(
                "❌ Неправильный формат команды.\n"
                "Используйте: /add_how <категория> <текст задания>\n"
                "Пример: /add_how материал акварелью"
            )

        _, category_name, task_text = command_parts
        response = await self.task_service.add_how_task(
            user_id=message.from_user.id,
            category_name=category_name,
            task_text=task_text
        )
        await message.answer(response)