from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Ассоциативная таблица для использованных категорий
user_seen_category = Table(
    'user_seen_category',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

# Ассоциативная таблица для отключенных категорий
user_disabled_category = Table(
    'user_disabled_category',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    daily_time = Column(Integer)
    sketches_time = Column(Integer)
    sketches_amount = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    seen_categories = relationship("Category", secondary=user_seen_category)
    disabled_categories = relationship("Category", secondary=user_disabled_category, lazy="selectin")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(String(10), nullable=False)  # 'что' или 'как'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    type = Column(String(10), nullable=False)  # 'что' или 'как'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="tasks")


Category.tasks = relationship("Task", back_populates="category")