from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

Token = config('TOKEN')

storage = MemoryStorage()
bot = Bot(Token)
dp = Dispatcher(bot=bot, storage=storage)

Admins = [659106628, ]