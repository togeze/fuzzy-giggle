from email.policy import default
from typing import Optional, List
from bot.settings.config import CATEGORY_TYPES
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())



user_disabled_categories = Table(
    'user_disabled_categories',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('category_id', Integer, ForeignKey('categories.id')),
    UniqueConstraint('user_id', 'category_id', name='uq_user_category')
)

user_tasks = Table(
    'user_tasks',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('how_id', Integer, ForeignKey('how.id')),
    Column('what_id', Integer, ForeignKey('what.id')),
    Column('assigned_at', DateTime(timezone=True), default=func.now()),
    UniqueConstraint('user_id', 'how_id', 'what_id', name='uq_user_how_what')
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(64))
    is_admin: Mapped[bool] = mapped_column(default=False)

    # Relationships
    disabled_categories: Mapped[List['Category']] = relationship(
        secondary=user_disabled_categories,
        back_populates='users'
    )
    assigned_tasks: Mapped[List['How']] = relationship(
        secondary=user_tasks,
        back_populates='users'
    )


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint('name', 'type', name='uq_category_name_type'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(10))  # 'how' или 'what' или 'image'

    # Relationships
    how_tasks: Mapped[List['How']] = relationship(back_populates='category')
    what_tasks: Mapped[List['What']] = relationship(back_populates='category')
    images: Mapped[List['Image']] = relationship(back_populates='category')
    users: Mapped[List['User']] = relationship(
        secondary=user_disabled_categories,
        back_populates='disabled_categories'
    )


class How(Base):
    __tablename__ = 'how'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    # Relationships
    category: Mapped['Category'] = relationship(back_populates='how_tasks')
    users: Mapped[List['User']] = relationship(
        secondary=user_tasks,
        back_populates='assigned_tasks'
    )


class What(Base):
    __tablename__ = 'what'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship(back_populates='what_tasks')


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_path: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship(back_populates='images')
