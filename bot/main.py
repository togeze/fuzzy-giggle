import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, html, types

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F

load_dotenv(find_dotenv())

from settings.commands import cmds
from keyboard.factory import KeyboardFactory


ALLOWED_UPDATES = ['message, edited_message']

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text, Command("exit"))
async def any_message(message: Message):
    await message.answer(
        "Пока, до новых встреч!"  # TODO сбросить всё в ноль, убрать все кнопки
    )

# добавить /settings где будет краткая инфа о боте

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Приветствую, {html.bold(message.from_user.full_name)}!", reply_markup=KeyboardFactory.get_main_menu())
    await message.answer("Example", reply_markup=KeyboardFactory.get_example_inline_menu())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=cmds, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())
