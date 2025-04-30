from abc import ABC, abstractmethod
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

class IKeyboardBuilder(ABC):
    @abstractmethod
    def build(self) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
        pass

class BaseInlineKeyboard(IKeyboardBuilder):
    def __init__(self):
        self.builder = InlineKeyboardBuilder()
        self.rows = []

    def add_row(self, *buttons: tuple[str, str]):
        self.rows.append(buttons)
        return self

    def build(self) -> InlineKeyboardMarkup:
        for row in self.rows:
            inline_buttons = [
                InlineKeyboardButton(text=text, callback_data=data)
                for text, data in row
            ]
            self.builder.row(*inline_buttons)
        return self.builder.as_markup()

class BaseReplyKeyboard:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()
        self.rows = []

    def add_row(self, *texts: str):
        self.rows.append([KeyboardButton(text=text) for text in texts])
        return self

    def build(self) -> ReplyKeyboardMarkup:
        for row in self.rows:
            self.builder.row(*row)
        return self.builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выберите действие"
        )