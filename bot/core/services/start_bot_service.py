from abc import ABC
from bot.database.repositories import CategoryRepository, UserRepository, WhatRepository, HowRepository
from bot.features.admin.presentation.routers import AdminRouter
from bot.features.user.presentation.routers import UserRouter
from bot.core.services.task_service import TaskService


class StartBotService:
    def __init__(self, session):
        category_repo = CategoryRepository(session)
        user_repo = UserRepository(session)
        what_repo = WhatRepository(session)
        how_repo = HowRepository(session)
        self.task_service = TaskService(category_repo, user_repo, what_repo, how_repo)
        self.user_router = UserRouter(self.task_service)
        self.admin_router = AdminRouter(self.task_service)

    async def initialize(self):
        await self.task_service.fill_categories_images()


