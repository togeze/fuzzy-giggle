from bot.keyboard.reply.main_menu import MainMenuKeyboard
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


class KeyboardFactory:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return MainMenuKeyboard().build()
