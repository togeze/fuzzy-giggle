import asyncio
import os
from aiogram import Bot, Dispatcher, html, types

from settings.config import TOKEN, ADMINS
from settings.commands import user_cmds, admin_cmds
from core.middlewares.role_checker import RoleMiddleware
from core.services.start_bot_service import StartBotService
from bot.core.dependencies import get_uow, engine
from bot.database.models import Base


ALLOWED_UPDATES = ['message, edited_message']


bot = Bot(token=TOKEN)
dp = Dispatcher()
uow = get_uow()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=user_cmds, scope=types.BotCommandScopeAllPrivateChats())

    for admin_id in ADMINS:
        await bot.set_my_commands(
            commands=admin_cmds,
            scope=types.BotCommandScopeChat(chat_id=admin_id)
        )

    dp.update.middleware(RoleMiddleware())

    async with uow.atomic() as session:
        start_bot_service = StartBotService(session)
        await start_bot_service.initialize()

        dp.include_router(start_bot_service.user_router.router)
        dp.include_router(start_bot_service.admin_router.router)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=ALLOWED_UPDATES,
            skip_updates=True
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
