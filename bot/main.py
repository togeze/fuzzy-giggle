import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.types import ReplyKeyboardRemove

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "-"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2')], [KeyboardButton(text='3')]], resize_keyboard=True, input_field_placeholder="Цифры")
il = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Меню', callback_data="Menu"), InlineKeyboardButton(text='Меню', callback_data="Menu")], [InlineKeyboardButton(text='Меню', callback_data="Menu")], [InlineKeyboardButton(text='Меню', callback_data="Menu")], [InlineKeyboardButton(text='Меню', callback_data="Menu")], [InlineKeyboardButton(text='Меню', callback_data="Menu")]])


@dp.message(Command('settings'))
async def settings_bot(message: Message):
    await message.answer('Hi', reply_markup=kb)

@dp.callback_query(F.data == 'Menu')
async def menu(callback: CallbackQuery):
    await callback.answer("Работа")
    #await callback.message.answer('Hi', reply_markup=kb)
    await callback.message.answer(
        "Выберите дату:",
        reply_markup=await SimpleCalendar().start_calendar()
    )

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!, {message.from_user.id},", reply_markup=ReplyKeyboardRemove())
    await message.answer("Some text", reply_markup=il)
    #await message.answer('Hi', reply_markup=kb)


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except:
        print("off bot")