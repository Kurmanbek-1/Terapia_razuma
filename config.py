from aiogram import Bot, Dispatcher
from decouple import config

Token = config('TOKEN')

bot = Bot(Token)
dp = Dispatcher(bot=bot)

Admins = [995712956, ]

# Psychologists = (995712956, )

st_1_shift = [995712956, ]
st_2_shift = [995712956, ]
st_3_shift = [995712956, ]