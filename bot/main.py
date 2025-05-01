import asyncio
import os
from aiogram import Bot, Dispatcher, html, types

from settings.config import TOKEN, ADMINS
from settings.commands import user_cmds, admin_cmds
from core.middlewares.role_checker import RoleMiddleware
from features.admin.presentation.routers import AdminRouter
from features.user.presentation.routers import UserRouter


ALLOWED_UPDATES = ['message, edited_message']


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=user_cmds, scope=types.BotCommandScopeAllPrivateChats())

    for admin_id in ADMINS:
        await bot.set_my_commands(
            commands=admin_cmds,
            scope=types.BotCommandScopeChat(chat_id=admin_id)
        )

    dp.update.middleware(RoleMiddleware())

    user_router = UserRouter()
    admin_router = AdminRouter()

    user_router.register_handlers()
    admin_router.register_handlers()

    dp.include_router(user_router.get_router)
    dp.include_router(admin_router.get_router)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=ALLOWED_UPDATES,
            skip_updates=True
        )
    finally:
        await bot.session.close()

asyncio.run(main())
