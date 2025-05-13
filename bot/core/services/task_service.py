from os import listdir, path
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Tuple

from numpy.ma.extras import unique

from bot.core.services.admin_service import IAdminService
from bot.database.models import Category, What, How, Image
from bot.settings.config import CATEGORY_TYPES, IMAGES_PATH, CSV_PATH


class ITaskService(ABC):
    ...


class TaskService(ITaskService, IAdminService):
    def __init__(self, category_repo, user_repo, what_repo, how_repo, image_repo):
        self.category_repo = category_repo
        self.user_repo = user_repo
        self.what_repo = what_repo
        self.how_repo = how_repo
        self.image_repo = image_repo

    async def add_category(self, category_type: str, name: str) -> str:

        if category_type.lower() not in CATEGORY_TYPES:
            return f"❌ Некорректный тип категории. Допустимые значения: {', '.join(CATEGORY_TYPES)}."

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

    async def get_categories(self, category_type: str) -> str:

        if category_type.lower() not in CATEGORY_TYPES:
            return f"❌ Некорректный тип категории. Допустимые значения: {', '.join(CATEGORY_TYPES)}."

        try:
            names = await self.category_repo.get_by_type(category_type)
            if names:
                return f"✅ Категории {category_type}: {names}."
            else:
                return f"✅ Нет категорий в {category_type}."
        except Exception as e:
            return f"❌ Ошибка при поиске категорий для {category_type}: {str(e)}"

    async def add_task(self, category_type: str, category_name: str, task_text: str) -> str:
        """ category_type: how, what, image """

        print(f"category_type = {category_type}")
        print(f"category_name = {category_name}")
        category = await self.category_repo.get_by_name_and_type(
            name=category_name,
            category_type=category_type
        )

        if not category:
            return f"❌ Категория '{category_name}' типа '{category_type}' не найдена."

        try:
            match category_type:
                case 'how':
                    new_task = How(
                        text=task_text.strip(),
                        category_id=category.id
                    )
                    await self.how_repo.add(new_task)
                case 'what':
                    new_task = What(
                        text=task_text.strip(),
                        category_id=category.id
                    )
                    await self.what_repo.add(new_task)
                case 'image':
                    new_task = Image(
                        file_path=task_text.strip(),
                        category_id=category.id
                    )
                    await self.image_repo.add(new_task)
                case _:
                    return f"❌ Некорректный тип {category_type}. Допустимые значения: {', '.join(CATEGORY_TYPES)}"
            return (f"✅ Задание для '{category_type}' успешно добавлено:\n"
                    f"Категория: {category_name}\n"
                    f"Текст: {task_text}")
        except Exception as e:
            print(f"❌ Ошибка при добавлении задания: {str(e)}")
            return f"❌ Ошибка при добавлении задания: {str(e)}"

    async def fill_database_image(self):
        """ При старте бота или команде /update_db сначала удаляет (если есть),
            а затем заполняет в БД типы image в таблице categories и таблицу images """

        # TODO clear table categorise (type image) and table images

        # get all folder names from images_path
        image_category_names = [item for item in listdir(IMAGES_PATH) if path.isdir(path.join(IMAGES_PATH, item))]

        # fill database
        try:
            for category_name in image_category_names:
                # fill categories image
                await self.add_category('image', category_name)

                # fill table images
                image_names = [item for item in listdir(path.join(IMAGES_PATH, category_name))]
                for image_name in image_names:
                    image_file_name = path.join(IMAGES_PATH, category_name, image_name)
                    await self.add_task(
                        category_type='image',
                        category_name=category_name,
                        task_text=image_file_name
                    )
            print(f"✅ Категории image успешно добавлены: {', '.join(image_category_names)}")
            print(f"✅ Таблица images заполнена.")
        except Exception as e:
            print(f"❌ Ошибка при добавлении категорий image: {str(e)}")

    async def clear_categories_image(self):
        # get all folder names from images_path
        image_category_names = [item for item in listdir(IMAGES_PATH) if path.isdir(path.join(IMAGES_PATH, item))]

    async def fill_database_from_csv(self):
        # чтение данных из csv
        csv = pd.read_csv(CSV_PATH)
        how_categories = csv['категория как'].dropna()
        what_categories = csv['категория что'].dropna()
        daily_themes = csv['тема на день'].dropna()
        what_tasks = csv['что'].dropna()
        how_tasks = csv['как'].dropna()

        # заполнение таблицы categories
        for category_name in how_categories.unique():
            await self.add_category('how', category_name)
        for category_name in what_categories.unique():
            await self.add_category('what', category_name)

        # заполнение таблицы how
        for idx, task_text in how_tasks.items():
            await self.add_task('how', how_categories.loc[idx], task_text)

        # заполнение таблицы what
        for idx, task_text in what_tasks.items():
            await self.add_task('what', what_categories.loc[idx], task_text)


    async def is_admin(self, user_id: int):
        user = await self.user_repo.get_by_telegram_id(user_id)
        if not user or not user.is_admin:
            return False
        return True
