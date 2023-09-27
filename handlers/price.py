""" Он пока не закончен, т.к он еще не скинул прайс свой """

from aiogram import Dispatcher, types


async def price(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Месячный", callback_data="button_1")
    button2 = types.InlineKeyboardButton("Годовой", callback_data="button_2")
    button3 = types.InlineKeyboardButton("Одноразовый", callback_data="button_3")

    inline_keyboard.add(button1, button2, button3)

    await message.answer("Снизу предоставлен прайс ⬇\n"
                         "Можете выбрать подходящий вам\n\n"
                         "Цены: \n"
                         "Одноразовый: 4$\n"
                         "Месячный: 10$\n"
                         "Годовой: 100$", reply_markup=inline_keyboard)

def register_price(dp: Dispatcher):
    dp.register_message_handler(price, commands=["Прайс", "Price"])
