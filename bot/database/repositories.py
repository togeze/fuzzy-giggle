from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload
from bot.database.models import Category, User, What, How
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
            func.lower(Category.type) == category_type.lower()
        )
        result = await self.session.execute(stmt)
        ss = result.all()[0][0]
        print(ss)
        print(ss.name)
        return [i[0] for i in result.all()]

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

class WhatRepository(BaseRepository):
    async def add(self, what_task: What):
        self.session.add(what_task)
        await self.session.commit()

class HowRepository(BaseRepository):
    async def add(self, how_task: How):
        self.session.add(how_task)
        await self.session.commit()