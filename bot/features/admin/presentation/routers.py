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
        self.router.message(Command("add_what"))(self.add_handler)
        self.router.message(Command("add_how"))(self.add_handler)
        self.router.message(Command("update_db"))(self.update_database)

    async def admin_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return
        keyboard_service = KeyboardService(is_admin)
        await message.answer(
            "Админ-панель",
            reply_markup=keyboard_service.get_admin_keyboard()
        )

    async def add_category_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return await message.answer("❌ Доступ запрещен. Требуются права администратора.")

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
        return await message.answer(response)

    async def get_categories_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return await message.answer("❌ Доступ запрещен. Требуются права администратора.")
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
        return await message.answer(response)

    async def add_handler(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return await message.answer("❌ Доступ запрещен. Требуются права администратора.")

        command_parts = message.text.split(maxsplit=2)
        category_type = command_parts[0][5:]
        print(category_type)
        if len(command_parts) < 3:
            return await message.answer(
                "❌ Неправильный формат команды.\n"
                f"Используйте: /add_{category_type} <категория> <текст задания>\n"
                f"Пример: /add_{category_type} Животные Нарисовать кота в стиле кубизма"
            )

        _, category_name, task_text = command_parts
        response = await self.task_service.add_task(
            user_id=message.from_user.id,
            category_type=category_type,
            category_name=category_name,
            task_text=task_text
        )
        return await message.answer(response)

    async def update_database(self, message: types.Message, is_admin: bool):
        if not is_admin:
            return await message.answer("❌ Доступ запрещен. Требуются права администратора.")

        response = await self.task_service.fill_database_from_csv(
            user_id=message.from_user.id
        )
        await message.answer(response)

        response = await self.task_service.fill_database_image()
        return await message.answer(response)
