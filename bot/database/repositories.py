from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload
from bot.database.models import Category, User, What, How, Image, user_tasks
from sqlalchemy import exists, and_, or_, func
from sqlalchemy import true, false
from bot.settings.config import MAX_ATTEMPTS


from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload
from bot.database.models import Category, User, What, How, Image
from sqlalchemy import true, false


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session


class CategoryRepository(BaseRepository):
    async def get_by_name_and_type(self, name: str, category_type: str):
        stmt = select(Category).where(
            func.lower(Category.name) == func.lower(name),
            func.lower(Category.type) == category_type.lower()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_type(self, category_type: str):
        stmt = select(Category).where(
            func.lower(Category.type) == category_type.lower())
        result = await self.session.execute(stmt)
        return ', '.join([i[0].name for i in result.all()])

    async def add(self, category: Category):
        existing = await self.get_by_name_and_type(category.name, category.type)
        if existing:
            raise ValueError("Категория с таким именем и типом уже существует")
        self.session.add(category)
        await self.session.commit()


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: int):
        stmt = select(User).options(
            selectinload(User.disabled_categories)
        ).where(User.telegram_id == telegram_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user: User, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def create_user(self, telegram_id: int, username: Optional[str], is_admin: bool = False):
        new_user = User(
            telegram_id=telegram_id,
            username=username,
            is_admin=is_admin
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_random_task_pair(self, user: User) -> tuple[How, What]:
        attempts = 0

        async def get_random_how():
            stmt = select(How).order_by(func.random()).limit(1)
            result = await self.session.execute(stmt)
            return result.scalar()

        async def get_random_what():
            stmt = select(What).order_by(func.random()).limit(1)
            result = await self.session.execute(stmt)
            return result.scalar()

        while attempts < MAX_ATTEMPTS:
            how_task = await get_random_how()
            what_task = await get_random_what()

            if not how_task or not what_task:
                raise ValueError("Отсутствуют задания в базе данных")

            # Проверяем, использовалась ли эта пара ранее
            existing = await self.session.execute(
                select(user_tasks)
                .where(
                    user_tasks.c.user_id == user.id,
                    user_tasks.c.how_id == how_task.id,
                    user_tasks.c.what_id == what_task.id
                )
            )
            if existing.scalar():
                attempts += 1
                continue

            try:
                # Добавляем новую запись
                await self.session.execute(
                    user_tasks.insert().values(
                        user_id=user.id,
                        how_id=how_task.id,
                        what_id=what_task.id
                    )
                )
                await self.session.commit()
                return how_task, what_task
            except IntegrityError:
                await self.session.rollback()
                attempts += 1
                continue

        await self.session.execute(
            user_tasks.delete().where(user_tasks.c.user_id == user.id)
        )
        await self.session.commit()
        return await self.get_random_task_pair(user)


class WhatRepository(BaseRepository):
    async def get_by_text(self, text: str):
        stmt = select(What).where(
            func.lower(What.text) == func.lower(text)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, what_task: What):
        existing = await self.get_by_text(what_task.text)
        if existing:
            raise ValueError("What задача с таким именем уже существует")
        self.session.add(what_task)
        await self.session.commit()


class HowRepository(BaseRepository):
    async def get_by_text(self, text: str):
        stmt = select(How).where(
            func.lower(How.text) == func.lower(text)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, how_task: How):
        existing = await self.get_by_text(how_task.text)
        if existing:
            raise ValueError("How задача с таким именем уже существует")
        self.session.add(how_task)
        await self.session.commit()


class ImageRepository(BaseRepository):
    async def get_by_name(self, file_path: str):
        stmt = select(Image).where(
            func.lower(Image.file_path) == func.lower(file_path)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, image_task: Image):
        existing = await self.get_by_name(image_task.file_path)
        if existing:
            raise ValueError("Изображение с таким именем уже существует")
        self.session.add(image_task)
        await self.session.commit()