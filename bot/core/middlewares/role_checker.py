from typing import Any, Dict, Callable
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from bot.core.services.user_service import UserService
from bot.core.services.keyboard_service import KeyboardService


class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            data["is_admin"] = await UserService.is_admin(user.id)
            data["keyboard_service"] = KeyboardService(data["is_admin"])
        return await handler(event, data)