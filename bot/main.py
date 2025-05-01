import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, html, types

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F

load_dotenv(find_dotenv())

from settings.commands import user_cmds, admin_cmds
from keyboard.factory import KeyboardFactory
from core.middlewares.role_checker import RoleMiddleware
from features.admin.presentation.routers import AdminRouter
from features.user.presentation.routers import UserRouter


ALLOWED_UPDATES = ['message, edited_message']

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# @dp.message(F.text, Command("exit"))
# async def any_message(message: Message):
#     await message.answer(
#         "Пока, до новых встреч!"  # TODO сбросить всё в ноль, убрать все кнопки
#     )

# добавить /settings где будет краткая инфа о боте

# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"Приветствую, {html.bold(message.from_user.full_name)}!", reply_markup=KeyboardFactory.get_main_menu())
#     await message.answer("Example", reply_markup=KeyboardFactory.get_example_inline_menu())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=user_cmds, scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=admin_cmds,
        scope=types.BotCommandScopeChat(chat_id=1870995730)
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
