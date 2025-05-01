from aiogram.types import BotCommand

user_cmds = [
    BotCommand(command='start', description='Get start')
]

admin_cmds = user_cmds +  [
    BotCommand(command='admin', description='Админ-панель')
]