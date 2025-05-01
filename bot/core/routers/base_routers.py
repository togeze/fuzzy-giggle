from abc import ABC, abstractmethod
from aiogram import Router

class BaseRouter(ABC):
    def __init__(self):
        self.router = Router()

    @abstractmethod
    def register_handlers(self):
        pass

    @property
    def get_router(self) -> Router:
        return self.router