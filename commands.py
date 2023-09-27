from aiogram import Dispatcher, types
from datetime import time


async def on_start(message: types.Message):
    await message.reply("Привет, это бот психолог! \n"
                        "За ботом есть психолог, не бойтесь, всё анонимно!")



async def about_the_service(message: types.Message):
    await message.answer("О сервисе:\n\n"
                         "✨ Что делает нас особенными? \n"
                         "Мы - первый сервис такого рода в нашей стране, который сделал психологическую помощь "
                         "доступной для всех. Мы убеждены, что каждый заслуживает поддержки и понимания, и стремимся "
                         "разрушить стереотипы, мешающие получить профессиональную помощь.\n\n"
                         "🫂 На данный момент работает команда живых и опытных психологов. Они выслушают, "
                         "помогут успокоиться, разобраться с чувствами и предоставят вам индивидуальную поддержку. \n"
                         "💌 Не ждите, чтобы преодолеть свои проблемы одни. Давайте вместе сделаем вашу жизнь более "
                         "счастливой и здоровой. Начните общение с нами прямо сейчас!")


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

