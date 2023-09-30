""" Он пока не закончен, т.к он еще не скинул прайс свой """

from aiogram import Dispatcher, types


async def price(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("Пробный", callback_data="button_1")
    button2 = types.InlineKeyboardButton("Последующая", callback_data="button_2")
    button3 = types.InlineKeyboardButton("На месяц", callback_data="button_3")
    button4 = types.InlineKeyboardButton("На 3 месяца", callback_data="button_4")

    inline_keyboard.add(button1, button2, button3, button4)

    await message.answer("Снизу предоставлен прайс ⬇\n"
                         "(Можете выбрать подходящий вам 🫶🏻)\n\n"
                         "Цены: \n"
                         "«Одноразовая сессия»:\n"
                         "  - Пробная - 0 сом \n"
                         "  - Вторая и последующие - 500 сом"
                         "\n\n"
                         "«Полное сопровождение»\n"
                         "  - На месяц - 2500 сом \n"
                         "  - На 3 месяца - 6000 сом", reply_markup=inline_keyboard)


def register_price(dp: Dispatcher):
    dp.register_message_handler(price, commands=["Прайс", "price"])
