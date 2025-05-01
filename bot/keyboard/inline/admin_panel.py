from bot.keyboard.base import BaseInlineKeyboard

class AdminPanelKeyboard(BaseInlineKeyboard):
    def __init__(self):
        super().__init__()
        self.add_row(("📊 Статистика", "admin_stats"))
        self.add_row(("👥 Пользователи", "admin_users"))
        self.add_row(("📢 Рассылка", "admin_broadcast"))