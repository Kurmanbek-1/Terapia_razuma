from aiogram.utils import executor
from config import bot, Admins, dp
from commands import register_commands
import logging


# ===========================================================================
async def on_startup(_):
    await bot.send_message(chat_id=Admins[0], text="Бот запущен!")


# ===========================================================================
register_commands(dp)
# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)




