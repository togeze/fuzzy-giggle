from abc import ABC, abstractmethod

class IAdminService(ABC):
    @abstractmethod
    async def add_category(self, user_id: int, category_type: str, name: str) -> str:
        pass

    @abstractmethod
    async def add_what_task(self, user_id: int, category_name: str, task_text: str) -> str:
        pass