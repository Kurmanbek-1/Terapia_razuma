import sqlite3
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
