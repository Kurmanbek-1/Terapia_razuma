from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import types


cancel_button = KeyboardButton('Отмена')
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(cancel_button)
