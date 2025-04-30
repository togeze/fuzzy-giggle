from abc import ABC, abstractmethod
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

class IKeyboardBuilder(ABC):
    @abstractmethod
    def build(self) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
        pass

class BaseInlineKeyboard(IKeyboardBuilder):
    def __init__(self):
        self.builder = InlineKeyboardBuilder()
        self.buttons = []

    def add_button(self, text: str, callback_data: str):
        self.buttons.append((text, callback_data))
        return self

    def add_buttons_row(self, buttons: list[tuple[str, str]]):
        self.buttons.extend(buttons)
        return self

    def adjust(self, *sizes: int):
        self.builder.adjust(*sizes)
        return self

    def build(self) -> InlineKeyboardMarkup:
        for text, callback_data in self.buttons:
            self.builder.button(text=text, callback_data=callback_data)
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