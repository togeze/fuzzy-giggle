from bot.keyboard.reply.common_reply_btn import CommonMenuKeyboard
from bot.keyboard.inline.common_inline_btn import CommonInlineKeyboard
from bot.keyboard.inline.admin_panel import AdminPanelKeyboard
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


class KeyboardFactory:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().build()
    @staticmethod
    def get_daily_start_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_set_daily_start.build()
    @staticmethod
    def get_sketches_time_menu() -> ReplyKeyboardMarkup:
        return ExampleInline().inline_buttons_sketches_time().build()
    @staticmethod
    def get_sketches_amount_menu() -> ReplyKeyboardMarkup:
        return ExampleInline().inline_buttons_sketches_amount().build()

    @staticmethod
    def get_example_inline_menu() -> InlineKeyboardMarkup:
        return ExampleInline().build()

    @staticmethod
    def get_admin_panel() -> InlineKeyboardMarkup:
        return AdminPanelKeyboard().build()

