from aiogram.types import BotCommand

user_cmds = [
    BotCommand(command='start', description='Get start'),
    BotCommand(command='info', description='Info about')
]

admin_cmds = user_cmds +  [
    BotCommand(command='admin', description='Админ-панель')
]