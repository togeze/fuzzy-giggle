from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ITaskService(ABC):
    @abstractmethod
    async def get_random_task_pair(self, user_id: int) -> Tuple[Optional[str], Optional[str]]:
        pass


class TaskService(ITaskService):
    def __init__(self, task_repo, category_repo, user_repo):
        self.task_repo = task_repo
        self.category_repo = category_repo
        self.user_repo = user_repo

    async def get_random_task_pair(self, user_id: int):
        user = await self.user_repo.get_by_telegram_id(user_id)
        if not user:
            return None, None

        disabled_cats = [c.id for c in user.disabled_categories]

        what_task = await self.task_repo.get_random_task('what', disabled_cats)
        how_task = await self.task_repo.get_random_task('how', disabled_cats)

        return (what_task.content if what_task else None,
                how_task.content if how_task else None)