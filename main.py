from aiogram.utils import executor
from config import bot, Admins, dp
from commands import register_commands
from handlers import price, fsm_pay
import logging
from db import ORM


# ===========================================================================
async def on_startup(_):
    await bot.send_message(chat_id=Admins[0], text="Бот запущен!")
    await ORM.sql_create()


# ===========================================================================
register_commands(dp)
price.register_price(dp)
fsm_pay.register_pay_handler(dp)
# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)




