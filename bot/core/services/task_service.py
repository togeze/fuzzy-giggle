from abc import ABC, abstractmethod
from typing import Optional, Tuple
from bot.core.services.admin_service import IAdminService
from bot.database.models import Category, What



class ITaskService(ABC):
    ...


class TaskService(ITaskService, IAdminService):
    def __init__(self, category_repo, user_repo, what_repo):
        self.category_repo = category_repo
        self.user_repo = user_repo
        self.what_repo = what_repo

    async def add_category(self, user_id: int, category_type: str, name: str) -> str:
        user = await self.user_repo.get_by_telegram_id(user_id)
        if not user or not user.is_admin:
            return "❌ Доступ запрещен. Требуются права администратора."

        if category_type.lower() not in ['how', 'what', 'image']:
            return "❌ Некорректный тип категории. Допустимые значения: how, what, image."

        existing_category = await self.category_repo.get_by_name_and_type(name, category_type)
        if existing_category:
            return f"❌ Категория '{name}' ({category_type}) уже существует."

        try:
            new_category = Category(
                name=name.strip(),
                type=category_type.lower()
            )
            await self.category_repo.add(new_category)
            return f"✅ Категория '{name}' ({category_type}) успешно добавлена."
        except Exception as e:
            return f"❌ Ошибка при добавлении категории: {str(e)}"

    async def add_what_task(self, user_id: int, category_name: str, task_text: str) -> str:
        user = await self.user_repo.get_by_telegram_id(user_id)
        if not user or not user.is_admin:
            return "❌ Доступ запрещен. Требуются права администратора."

        category = await self.category_repo.get_by_name_and_type(
            name=category_name,
            category_type='what'
        )

        if not category:
            return f"❌ Категория '{category_name}' типа 'what' не найдена."

        try:
            new_task = What(
                text=task_text.strip(),
                category_id=category.id
            )
            await self.what_repo.add(new_task)
            return (f"✅ Задание для 'what' успешно добавлено:\n"
                    f"Категория: {category_name}\n"
                    f"Текст: {task_text}")
        except Exception as e:
            return f"❌ Ошибка при добавлении задания: {str(e)}"
