from abc import ABC, abstractmethod
from bot.settings.config import ADMINS
class IUserService(ABC):
    @abstractmethod
    async def is_admin(self, user_id: int) -> bool:
        pass

class UserService(IUserService):
    @classmethod
    async def is_admin(cls, user_id: int) -> bool:
        return user_id in ADMINS