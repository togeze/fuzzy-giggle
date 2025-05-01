from bot.features.admin.presentation.routers import AdminRouter
from bot.features.user.presentation.routers import UserRouter

class RouterFactory:
    @staticmethod
    def create_routers(is_admin: bool) -> list:
        base_routers = [UserRouter()]
        if is_admin:
            base_routers.append(AdminRouter())
        return base_routers