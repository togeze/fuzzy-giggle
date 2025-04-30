from bot.keyboard.base import BaseInlineKeyboard

class ExampleInline(BaseInlineKeyboard):
    def __init__(self):
        super().__init__()
        self.add_row(("⏮ ", "prev"), ("⏭", "next"))
        self.add_row(("📊 ", "progress"), ("🏠", "main_menu"))
        self.add_row(("ℹ️", "help"))