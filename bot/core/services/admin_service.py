from abc import ABC, abstractmethod

class IAdminService(ABC):
    @abstractmethod
    async def add_category(self, category_type: str, name: str) -> str:
        pass

    @abstractmethod
    async def get_categories(self, category_type: str) -> str:
        pass

    @abstractmethod
    async def add_task(self, category_type: str, category_name: str, task_text: str) -> str:
        pass