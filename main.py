from aiogram.utils import executor
from config import bot, Admins, dp
from commands import register_commands
from handlers import price, fsm_pay
import logging
from db import ORM

admins = [Admins[0], Admins[1]]


# ===========================================================================
async def on_startup(_):
    for admin in admins:
        await bot.send_message(chat_id=admin, text="Бот запущен!")
        await ORM.sql_create()


# ===========================================================================
register_commands(dp)
price.register_price(dp)
fsm_pay.register_pay_handler(dp)
ORM.sql_get_ORM(dp)
# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
