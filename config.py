from aiogram import Bot, Dispatcher
from decouple import config

Token = config('TOKEN')

bot = Bot(Token)
dp = Dispatcher(bot=bot)

Admins = [995712956, ]
