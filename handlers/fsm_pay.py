from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import Admins, DESTINATION_DIR
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Pay(StatesGroup):
    receipt = State()

async def receipt_test(call: types.CallbackQuery, tariff: str):
    user_id = call.message.chat.id
    await bot.send_message(user_id,
                           text=f"Вы выбрали тариф: {tariff}\n"
                                "Для оплаты выбранного тарифа отправьте, пожалуйста, "
                                "фото или скриншот квитанции\n\n"
                                "Для выхода из раздела оплаты нажмите - /exit")
    await Pay.receipt.set()


async def exit_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Вы вышли из раздела оплаты')


async def process_receipt(message: types.Message, state: FSMContext):
    user_id = message.chat.id

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton("Да✅", callback_data="button_yes")
    button_no = InlineKeyboardButton("Нет❌", callback_data="button_no")
    inline_keyboard.add(button_yes, button_no)

    path = await message.photo[-1].download(
        destination_dir=DESTINATION_DIR
    )
    async with state.proxy() as data:
        data["user_id"] = user_id
        data["receipt"] = path.name
    with open(path.name, "rb") as photo:
        await bot.send_photo(chat_id=Admins[0],
                             photo=photo,
                             caption=f"Поступила ли оплата от {user_id}",
                             reply_markup=inline_keyboard)
        await message.answer("Отправлено на проверку админу")
    await state.finish()


async def answer_yes(call: types.CallbackQuery):
    user_id = int(call.message.caption.split()[-1])

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(user_id, text="Оплата прошла успешно✅")


async def answer_no(call: types.CallbackQuery):
    user_id = int(call.message.caption.split()[-1])

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(user_id, text="Оплата не прошла❌")



def register_pay_handler(dp: Dispatcher):
    dp.register_callback_query_handler(lambda call: receipt_test(call, "Пробный"),
                                       lambda call: call.data == "button_1")
    dp.register_callback_query_handler(lambda call: receipt_test(call, "Последующяя"),
                                       lambda call: call.data == "button_2")
    dp.register_callback_query_handler(lambda call: receipt_test(call, "На месяц"),
                                       lambda call: call.data == "button_3")
    dp.register_callback_query_handler(lambda call: receipt_test(call, "На 3 месяца"),
                                       lambda call: call.data == "button_4")

    dp.register_message_handler(exit_command, state='*', commands='exit')
    dp.register_message_handler(exit_command, Text(equals='exit', ignore_case=True), state='*')
    dp.register_message_handler(process_receipt, state=Pay.receipt,
                                content_types=types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(answer_yes, lambda call: call.data == "button_yes")
    dp.register_callback_query_handler(answer_no, lambda call: call.data == "button_no")


