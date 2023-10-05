import sqlite3
from db import sql_queris


db = sqlite3.connect("db/checks_db")
cursor = db.cursor()


def sql_create():
    if db:
        print("База Бишкек подключена!")
    cursor.execute(sql_queris.CREATE_TABLE_CHECK)
    db.commit()


async def sql_insert_check(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.CREATE_TABLE_CHECK, tuple(data.values()))
        db.commit()
