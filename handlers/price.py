""" Он пока не закончен, т.к он еще не скинул прайс свой """

from aiogram import Dispatcher, types


async def price(message: types.Message):
    await message.answer("Снизу предоставлен прайс ⬇\n"
                         "(Можете выбрать подходящий вам 🫶🏻)\n\n"
                         "Цены: \n"
                         "«Одноразовая сессия»:\n"
                         "  - Пробная - 0 сом \n"
                         "  - Вторая и последующие - 500 сом"
                         "\n\n"
                         "«Полное сопровождение»\n"
                         "  - На месяц - 2500 сом \n"
                         "  - На 3 месяца - 6000 сом\n\n"
                         "Для перехода к оплате нажмите на \n"
                         "👉/pay")


def register_price(dp: Dispatcher):
    dp.register_message_handler(price, commands=["Прайс", "price"])
