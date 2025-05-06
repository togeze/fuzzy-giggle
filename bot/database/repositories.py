from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload
from bot.database.models import Task, Category, User


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session


class TaskRepository(BaseRepository):
    async def get_random_task(self, task_type: str, exclude_categories: list[int]):
        stmt = select(Task).join(Category).where(
            Task.type == task_type,
            Category.id.notin_(exclude_categories)
        ).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class CategoryRepository(BaseRepository):
    async def get_by_type(self, category_type: str):
        stmt = select(Category).where(
            Category.type == category_type,
            Category.is_active == True
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: int):
        stmt = select(User).options(
            selectinload(User.disabled_categories)
        ).where(User.telegram_id == telegram_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user_settings(self, user_id: int, **kwargs):
        stmt = update(User).where(User.id == user_id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_user(self, telegram_id: int, is_admin: bool = False):
        new_user = User(telegram_id=telegram_id, is_admin=is_admin)
        self.session.add(new_user)
        await self.session.commit()
        return new_user