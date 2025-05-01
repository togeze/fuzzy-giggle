from bot.keyboard.reply.main_menu import MainMenuKeyboard
from bot.keyboard.inline.example_inline_btn import ExampleInline
from bot.keyboard.inline.admin_panel import AdminPanelKeyboard
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


class KeyboardFactory:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return MainMenuKeyboard().build()
    @staticmethod
    def get_example_inline_menu() -> InlineKeyboardMarkup:
        return ExampleInline().build()

    @staticmethod
    def get_admin_panel() -> InlineKeyboardMarkup:
        return AdminPanelKeyboard().build()

