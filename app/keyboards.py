from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔮Число судьбы')],
    [KeyboardButton(text='📅Персональное число года')],
    [KeyboardButton(text='💎Мой баланс токенов')],
    [KeyboardButton(text='💰Пополнить баланс')],
    [KeyboardButton(text='📞Помощь')],
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

choices = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Разбор числа судьбы')],
    [KeyboardButton(text='Разбор числа персонального года')]
],
                              resize_keyboard=True,
                              input_field_placeholder='Выберите разбор...')

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выдать токен для разбора числа судьбы')],
    [KeyboardButton(text='Выдать токен для разбора числа персонального года')],
    [KeyboardButton(text='Получить данные всех пользователей')],
    [KeyboardButton(text='Помощь (панель администратора)')]
], 
                                 resize_keyboard=True,
                                 input_field_placeholder='Выберите пункт меню')


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад в меню🔙', callback_data='back_to_menu')]])
back_to_adm_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад в меню🔙', callback_data='back_to_adm_menu')]])

async def clients_name(name):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=name)]], 
                               resize_keyboard=True,
                               input_field_placeholder='Введите имя или оставьте такое же')

async def clients_phone():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📱Поделиться контактом✍️',
                                                         request_contact=True)]],
                               resize_keyboard=True,
                               input_field_placeholder='Введите номер или поделитесь контактом')