from bot.keyboard.reply.common_reply_btn import CommonMenuKeyboard
from bot.keyboard.inline.common_inline_btn import CommonInlineKeyboard
from bot.keyboard.inline.admin_panel import AdminPanelKeyboard
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


class KeyboardFactory:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_main_menu().build()

    @staticmethod
    def get_daily_start_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_set_daily_start().build()

    @staticmethod
    def get_draw_now_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_draw_now().build()

    @staticmethod
    def get_stop_sketches_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_stop_sketches().build()

    @staticmethod
    def get_daily_stop_menu() -> ReplyKeyboardMarkup:
        return CommonMenuKeyboard().push_button_set_daily_stop().build()

    @staticmethod
    def get_sketches_time_menu() -> ReplyKeyboardMarkup:
        return CommonInlineKeyboard().inline_buttons_sketches_time().build()

    @staticmethod
    def get_sketches_fix_time_menu() -> ReplyKeyboardMarkup:
        return CommonInlineKeyboard().inline_buttons_sketches_fix_time().build()

    @staticmethod
    def get_start_sketches_menu() -> ReplyKeyboardMarkup:
        return CommonInlineKeyboard().inline_buttons_sketches_start().build()

    @staticmethod
    def get_sketches_amount_menu() -> ReplyKeyboardMarkup:
        return CommonInlineKeyboard().inline_buttons_sketches_amount().build()

    @staticmethod
    def get_daily_time_menu() -> ReplyKeyboardMarkup:
        return CommonInlineKeyboard().inline_buttons_daily_time().build()

    @staticmethod
    def get_admin_panel() -> InlineKeyboardMarkup:
        return AdminPanelKeyboard().build()

