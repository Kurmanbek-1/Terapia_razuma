from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import Admins, Psychologist
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers import buttons
from db.ORM import sql_insert_check, sql_insert_payment_request, check_user_has_used_trial


class Pay(StatesGroup):
    user_tariff = State()
    photo_check = State()


async def tariff_process(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton("Пробный", callback_data="button_1")
    button2 = types.InlineKeyboardButton("Последующая", callback_data="button_2")
    button3 = types.InlineKeyboardButton("Базовый", callback_data="button_3")
    button4 = types.InlineKeyboardButton("Продвинутый", callback_data="button_4")

    inline_keyboard.add(button1, button2, button3, button4)

    user_id = message.chat.id
    await bot.send_message(user_id, text="Выберите тариф для оплаты👇",
                           reply_markup=inline_keyboard)
    await message.answer("Для выхода нажмите 'Отмена' снизу  ⬇",
                         reply_markup=buttons.cancel_markup)
    await Pay.user_tariff.set()


async def check_test(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    tariff = None

    if call.data == "button_2":
        tariff = "Последующая"
    elif call.data == "button_3":
        tariff = "Базовый"
    elif call.data == "button_4":
        tariff = "Продвинутый"

    if tariff:
        async with state.proxy() as data:
            data["tariff"] = tariff
    await Pay.next()
    await bot.send_message(user_id,
                           text=f"Вы выбрали тариф: {tariff}\n"
                                "Для оплаты выбранного тарифа отправьте, пожалуйста, "
                                "фото или скриншот квитанции\n\n"
                                "Реквизиты:\n"
                                "Мбанк: 4177490173421654\n"
                                "            +996 774 881 885\n"
                                "            Расул. У"
                                "\n\n"
                                "Для выхода нажмите 'Отмена' снизу  ⬇", reply_markup=buttons.cancel_markup)
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


async def probnyi_tariff(call: types.CallbackQuery, state: FSMContext):
    inline_keyboard = InlineKeyboardMarkup()
    ok_button = InlineKeyboardButton("OK✅", callback_data="ok_button")
    inline_keyboard.add(ok_button)

    fullname = call.message.chat.full_name
    user_id = call.message.chat.id
    username = call.message.chat.username
    tariff = "Пробный"

    has_used_trial = await check_user_has_used_trial(user_id)

    if has_used_trial:
        await bot.send_message(user_id, "Извините, вы уже использовали тариф 'Пробный'. ❌")
        return

    if not username:
        username = fullname

    async with state.proxy() as data:
        data["tariff"] = tariff
        data["user_id"] = user_id
        data["user_name"] = f"@{username}"
        data["photo_check"] = None

    await sql_insert_check(state)
    await bot.send_message(user_id, text=f"Вы выбрали тариф: Пробный\n"
                                         f"Вот аккаунт психолога - {Psychologist}")

    await bot.send_message(chat_id=Admins[0],
                           text=f"Пользователь выбрал тариф: Пробный\n"
                                f"Username: @{username}\n"
                                f"Fullname: {fullname}",
                           reply_markup=inline_keyboard)

    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)
    await state.finish()


async def answer_ok(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)


async def exit_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Вы вышли из раздела оплаты', reply_markup=None)


async def process_receipt(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    username = message.from_user.username
    fullname = message.chat.full_name
    photo_check = message.photo[-1].file_id

    if not username:
        username = fullname

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    button_yes = InlineKeyboardButton("Да✅", callback_data="button_yes")
    button_no = InlineKeyboardButton("Нет❌", callback_data="button_no")
    inline_keyboard.add(button_yes, button_no)

    async with state.proxy() as data:
        if data.get("photo_check") is not None:
            return
        data["photo_check"] = photo_check
        data["user_id"] = user_id
        data["user_name"] = username
    for admin in Admins:
        await bot.send_photo(chat_id=admin,
                             photo=photo_check,
                             caption=f"Поступила ли оплата от @{message.from_user.username}\n"
                                     f"Fullname: {fullname}\n"
                                     f"Тариф: {data['tariff']}\n"
                                     f"{user_id}\n",
                             reply_markup=inline_keyboard)
    await message.answer("Отправлено на проверку администратору!  🙌🏼\n"
                         "Это займет какое-то время, прошу подождать! ⏳")
    await sql_insert_payment_request(state)
    await state.finish()


async def answer_yes(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.message.caption.split()[-1])
    username = call.message.caption.split()[4]
    tariff = call.message.caption.split()[8]
    fullname = call.message.caption.split()[6]
    photo_check = call.message.photo[-1].file_id
    if username == "@None":
        username = fullname

    async with state.proxy() as data:
        data["tariff"] = tariff
        data["user_id"] = user_id
        data["user_name"] = username
        data["photo_check"] = photo_check

    await sql_insert_check(state)

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(user_id, text=f"Оплата прошла успешно✅\n"
                                         f"Аккаунт психолога - {Psychologist}", reply_markup=None)


async def answer_no(call: types.CallbackQuery):
    user_id = int(call.message.caption.split()[-1])

    await bot.send_message(user_id, text="Оплата не прошла❌", reply_markup=None)

    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_pay_handler(dp: Dispatcher):
    dp.register_message_handler(tariff_process, commands=["pay"])
    dp.register_message_handler(exit_command, state='*', commands='Отмена')
    dp.register_message_handler(exit_command, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_callback_query_handler(check_test,
                                       lambda call: call.data in ["button_2", "button_3", "button_4"],
                                       state=Pay.user_tariff)
    dp.register_callback_query_handler(probnyi_tariff,
                                       lambda call: call.data == "button_1",
                                       state=Pay.user_tariff)
    dp.register_message_handler(process_receipt, state=Pay.photo_check,
                                content_types=types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(answer_yes, lambda call: call.data == "button_yes")
    dp.register_callback_query_handler(answer_no, lambda call: call.data == "button_no")
    dp.register_callback_query_handler(answer_ok, lambda call: call.data == "ok_button")
