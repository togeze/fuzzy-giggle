from bot.keyboard.base import BaseInlineKeyboard

class ExampleInline(BaseInlineKeyboard):
    def __init__(self):
        super().__init__()
        self.add_button("⏮", "left")
        self.add_button("⏭", "right")
        self.add_button("📊 ", "progress")
        self.add_button("🏠 ", "main_menu")
        self.adjust(2, 2)