from aiogram import Dispatcher, types
from config import bot, st_1_shift, st_2_shift, st_3_shift
from datetime import time


async def on_start(message: types.Message):
    await message.reply("Привет, это бот психолог! \n"
                        "За ботом есть психолог, не бойтесь, всё анонимно!")


""" Разделить по сменам! """
async def echo_message(message: types.Message):
    pass

"""======================"""

async def about_the_service(message: types.Message):
    await message.answer("О сервисе:\n\n"
                         "'Терапия разума'- это сервис личной психотерапии в онлайн формате, с психологом\n"
                         "❤️Сейчас в чате работает команда профессиональных психологов. Вы пишете психологу "
                         "в чат, психолог знакомится с вами, проводит первичную сессию, на которой уточняет запрос "
                         "и составляет план терапии. Далее вы назначаете даты и время сессий и начинаете работу. "
                         "Между сессиями вы получаете поддержку, ответы на вопросы, обучающие и мотивирующие материалы "
                         "по теме его запроса.\n"
                         "")


async def service_rules(message: types.Message):
    await message.answer("Правила сервиса: \n"
                         "Уважительно относиться к вашему собесеседнику-психологу\n"
                         "Не материться, не выражаться")


async def service_support(message: types.Message):
    await message.answer("Здесь будет номера или аккаунты поддержки!")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(on_start, commands=["start"])
    dp.register_message_handler(about_the_service, commands=['about'])
    dp.register_message_handler(service_rules, commands=['rules'])
    dp.register_message_handler(service_support, commands=['support'])

    dp.register_message_handler(echo_message)
