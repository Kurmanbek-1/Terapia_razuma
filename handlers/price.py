""" Он пока не закончен, т.к он еще не скинул прайс свой """

from aiogram import Dispatcher, types


async def price(message: types.Message):
    await message.answer("Прайс  \n\n"
                         "«Одноразовая сессия»:\n"
                         "  - Пробная - 0 сом \n"
                         "  ⁃ Вторая и последующие (60-90мин) - 500сом"
                         "\n\n"
                         "«Пакеты»\n"
                         "   ⁃ Пакет «Базовый» из 4 сеансов в месяц (60-90мин) - 1500сом\n"
                         "   ⁃ Пакет «Продвинутый» из 8 сеансов в месяц (60-90мин) - 3000сом\n\n"
                         "Для перехода к оплате нажмите на \n"
                         "👉/pay")


def register_price(dp: Dispatcher):
    dp.register_message_handler(price, commands=["Прайс", "price"])
