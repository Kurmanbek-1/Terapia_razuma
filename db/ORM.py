import sqlite3
import types
from aiogram import types, Dispatcher
from config import Admins, bot

from db import sql_queris


db = sqlite3.connect("db/checks_db")
cursor = db.cursor()


async def sql_create():
    if db:
        print("База Бишкек подключена!")
    cursor.execute(sql_queris.CREATE_TABLE_CHECK)
    cursor.execute(sql_queris.CREATE_TABLE_PAYMENT_CHECK)
    db.commit()


async def sql_insert_check(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_CHECK, tuple(data.values()))
        db.commit()

async def sql_insert_payment_request(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_PAYMENT_REQUEST, tuple(data.values()))
        db.commit()

async def check_user_has_used_trial(user_id):
    cursor.execute(sql_queris.SELECT_TARIFF_PROBNYI, (user_id,))
    count = cursor.fetchone()[0]
    return count > 0

async def get_all_checks(message: types.Message):
    all_checks = cursor.execute(sql_queris.SELECT_CHECKS_ALL).fetchall()

    for check in all_checks:
        if message.from_user.id in Admins:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=check[2],
                                 caption=f"Тариф: {check[1]}\n"
                                         f"User ID: {check[3]}\n"
                                         f"Username: {check[4]}")


async def get_done_checks(message: types.Message):
    done_checks = cursor.execute(sql_queris.SELECT_CHECKS_DONE).fetchall()

    for check in done_checks:
        if message.from_user.id in Admins:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=check[4],
                                 caption=f"Тариф: {check[1]}\n"
                                         f"User ID: {check[2]}\n"
                                         f"Username: {check[3]}")

def sql_get_ORM(dp: Dispatcher):
    dp.register_message_handler(get_all_checks, commands=['checks_all'])
    dp.register_message_handler(get_done_checks, commands=['checks_done'])
