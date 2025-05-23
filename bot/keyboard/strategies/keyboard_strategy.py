from abc import ABC, abstractmethod
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from bot.keyboard import KeyboardFactory

class IKeyboardStrategy(ABC):
    @abstractmethod
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_daily_start_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_daily_stop_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_draw_now_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_stop_sketches_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_sketches_time_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_sketches_fix_time_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_start_sketches_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_sketches_amount_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_daily_time_menu(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_admin_menu(self) -> InlineKeyboardMarkup:
        pass

class UserKeyboardStrategy(IKeyboardStrategy):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_main_menu()

    def get_daily_start_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_start_menu()

    def get_daily_stop_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_stop_menu()

    def get_draw_now_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_draw_now_menu()

    def get_stop_sketches_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_stop_sketches_menu()

    def get_sketches_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_time_menu()

    def get_sketches_fix_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_fix_time_menu()

    def get_start_sketches_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_start_sketches_menu()

    def get_sketches_amount_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_amount_menu()

    def get_daily_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_time_menu()

    def get_admin_menu(self) -> InlineKeyboardMarkup:
        raise NotImplementedError("У пользователя нет админ-меню")


class AdminKeyboardStrategy(IKeyboardStrategy):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_main_menu()

    def get_daily_start_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_start_menu()

    def get_daily_stop_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_stop_menu()

    def get_draw_now_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_draw_now_menu()

    def get_stop_sketches_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_stop_sketches_menu()

    def get_sketches_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_time_menu()

    def get_sketches_fix_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_fix_time_menu()

    def get_start_sketches_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_start_sketches_menu()

    def get_sketches_amount_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_sketches_amount_menu()

    def get_daily_time_menu(self) -> ReplyKeyboardMarkup:
        return KeyboardFactory.get_daily_time_menu()

    def get_admin_menu(self) -> InlineKeyboardMarkup:
        return KeyboardFactory.get_admin_panel()