from bot.keyboard.strategies.keyboard_strategy import (
    IKeyboardStrategy,
    UserKeyboardStrategy,
    AdminKeyboardStrategy
)

class KeyboardService:
    def __init__(self, is_admin: bool):
        self.strategy: IKeyboardStrategy = AdminKeyboardStrategy() if is_admin else UserKeyboardStrategy()

    def get_main_keyboard(self):
        return self.strategy.get_main_menu()

    def get_daily_start_keyboard(self):
        return self.strategy.get_daily_start_menu()

    def get_sketches_time_keyboard(self):
        return self.strategy.get_sketches_time_menu()

    def get_sketches_amount_keyboard(self):
        return self.strategy.get_sketches_amount_menu()

    def get_admin_keyboard(self):
        return self.strategy.get_admin_menu()