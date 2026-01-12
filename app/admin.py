import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
from aiogram.fsm.context import FSMContext
from app.states import Enter

from app.database.requests import add_tokens_NoD, add_tokens_NoPY, get_user_by_username, get_users, is_user

import app.keyboards as kb
from app.validation_functions import is_valid_username, is_valid_count_tokens

from dotenv import load_dotenv

load_dotenv()

admin = Router()

admins_str = os.getenv('ADMINS', '')
admins_list = [int(admin_id.strip()) for admin_id in admins_str.split(',') if admin_id.strip()]

class Admin(Filter):
    def __init__(self):
        self.admins = admins_list

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
    

@admin.message(Admin(), Command('admin'))
async def cmd_start(message: Message):
    await message.answer(
        '👋🏻Добро пожаловать в панель администратора!\n\n'
        'Ознакомьтесь с функциями администратора⬇️',
        reply_markup=kb.admin_menu
    )

@admin.message(Command('admin'))
async def no_admin_rights(message: Message):
    await message.answer('❌У вас нет прав администратора!')
    
    
    
@admin.callback_query(Admin(), F.data == 'back_to_adm_menu')
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        '👋🏻Добро пожаловать в панель администратора!\n\n'
        'Ознакомьтесь с функциями администратора⬇️',
        reply_markup=kb.admin_menu
    )



@admin.message(Admin(), F.text == 'Выдать токен для разбора числа судьбы')
async def enter_username(message: Message, state: FSMContext):
    await state.set_state(Enter.username_for_NoD)
    await message.answer(
        '✍️Введите имя пользователя\n\n'
        '📋Формат: @имя_пользователя',
        reply_markup=kb.back_to_adm_menu
    )

@admin.message(Enter.username_for_NoD)
async def enter_count_tokens(message: Message, state: FSMContext):
    username_str = message.text.strip()
    
    if not is_valid_username(username_str):
        await message.answer(
            '❌ **Неверный формат username!**\n\n'
            '👤 **Пожалуйста, введите username в формате:**\n'
            '**@username**\n\n'
            '📋 **Требования к username:**\n'
            '• Должен начинаться с символа `@`\n'
            '• Может содержать: *латинские буквы*, *цифры* и *нижнее подчеркивание*\n'
            '• Длина: *от 4 до 32 символов* (без @)\n'
            '• Не должен начинаться с цифры\n'
            '• Не должен заканчиваться на `_`\n\n'
            '✅ **Примеры правильных username:**\n'
            '• @john_doe\n'
            '• @alexandra2023\n'
            '• @user_name\n'
            '• @michael123\n\n'
            '✍️ **Введите username пользователя:**',
            reply_markup=kb.back_to_adm_menu,
            parse_mode="Markdown"
        )
        return
    
    valid_username = username_str[1:]
    if await is_user(valid_username):
        await state.update_data(username=valid_username)
        
        await state.set_state(Enter.count_tokens_for_NoD)
        await message.answer('✍️Введите количество выдаваемых токенов', reply_markup=kb.back_to_adm_menu)
    else:
        await message.answer('❌Пользователь не найден!\nПроверьте имя пользователя', reply_markup=kb.back_to_adm_menu)

@admin.message(Enter.count_tokens_for_NoD)
async def bot_response(message: Message, state: FSMContext):
    tokens = message.text.strip()
    
    if not is_valid_count_tokens(tokens):
        await message.answer(
            '❌ Неверный формат количества токенов\n\n'
            '📋 Требования:\n'
            '• Только положительное число\n'
            '• Не равно ноль*\n'
            '✍️ Введите количество токенов:',
            reply_markup=kb.back_to_adm_menu
        )
        return
    
    await state.update_data(tokens=tokens)
    
    data = await state.get_data()
    await add_tokens_NoD(data['username'], data['tokens'])
    
    user = await get_user_by_username(data['username'])
    await message.answer(
        f'✅Вы успешно добавили токены пользователю: @{user.username}\n\n'
        f'🛒Добавлено токенов: {data["tokens"]}\n'
        f'💵Баланс токенов пользователя @{user.username} для разбора числа судьбы: {user.tokens_for_NoD}\n\n'
        f'💵Баланс токенов пользователя @{user.username} для разбора числа персонального года: {user.tokens_for_NoPY}'
    )
    await state.clear()
    



@admin.message(Admin(), F.text == 'Выдать токен для разбора числа персонального года')
async def enter_username(message: Message, state: FSMContext):
    await state.set_state(Enter.username_for_NoPY)
    await message.answer(
        '✍️Введите имя пользователя\n\n'
        '📋Формат: @имя_пользователя',
        reply_markup=kb.back_to_adm_menu
    )

@admin.message(Enter.username_for_NoPY)
async def enter_count_tokens(message: Message, state: FSMContext):
    username_str = message.text.strip()
    
    if not is_valid_username(username_str):
        await message.answer(
            '❌ **Неверный формат username!**\n\n'
            '👤 **Пожалуйста, введите username в формате:**\n'
            '**@username**\n\n'
            '📋 **Требования к username:**\n'
            '• Должен начинаться с символа `@`\n'
            '• Может содержать: *латинские буквы*, *цифры* и *нижнее подчеркивание*\n'
            '• Длина: *от 4 до 32 символов* (без @)\n'
            '• Не должен начинаться с цифры\n'
            '• Не должен заканчиваться на `_`\n\n'
            '✅ **Примеры правильных username:**\n'
            '• @john_doe\n'
            '• @alexandra2023\n'
            '• @user_name\n'
            '• @michael123\n\n'
            '✍️ **Введите username пользователя:**',
            reply_markup=kb.back_to_adm_menu,
            parse_mode="Markdown"
        )
        return
    
    valid_username = username_str[1:]
    
    if await is_user(valid_username):
        await state.update_data(username=valid_username)
        
        await state.set_state(Enter.count_tokens_for_NoPY)
        await message.answer('✍️Введите количество выдаваемых токенов', reply_markup=kb.back_to_adm_menu)
    else:
        await message.answer('❌Пользователь не найден!\nПроверьте имя пользователя', reply_markup=kb.back_to_adm_menu)

@admin.message(Enter.count_tokens_for_NoPY)
async def bot_response(message: Message, state: FSMContext):
    tokens = message.text.strip()
    await state.update_data(tokens=tokens)
    
    data = await state.get_data()
    await add_tokens_NoPY(data['username'], data['tokens'])
    
    user = await get_user_by_username(data['username'])
    await message.answer(
        f'✅Вы успешно добавили токены пользователю: @{user.username}\n\n'
        f'🛒Добавлено токенов: {data["tokens"]}\n'
        f'💵Баланс токенов пользователя @{user.username} для разбора числа судьбы: {user.tokens_for_NoD}\n\n'
        f'💵Баланс токенов пользователя @{user.username} для разбора числа персонального года: {user.tokens_for_NoPY}'
    )
    await state.clear()
    
    

@admin.message(Admin(), F.text == 'Получить данные всех пользователей')
async def get_info(message: Message):
    users = await get_users()
    
    if not users:
        await message.answer('❗️Нет пользователей в базе данных❗️')
        return
    
    header = "📊 *Данные всех пользователей*\n\n"
    table_header = "ID | Name | Username | NoD | NoPY \n"
    
    table_rows = []
    for user in users:
        row = f"{user.tg_id} | {user.name} | @{user.username} | {user.tokens_for_NoD} | {user.tokens_for_NoPY}"
        table_rows.append(row)
    
    full_message = header + table_header + "\n".join(table_rows)
    
    await message.answer(full_message, parse_mode="Markdown")



@admin.message(Admin(), F.text == 'Помощь (панель администратора)')
async def get_help(message: Message):
    help_text = """
🆘 <b>Помощь для администратора</b>

📌 <b>1. Как работать с выдачей токенов?</b>
👉 Отправляем имя пользователя в формате @имя_пользователя
🔍 Его можно найти в профиле человека
➡️ Затем отправляем количество токенов для начисления

📊 <b>2. Как работать с кнопкой "Получить данные всех пользователей"?</b>
📋 При нажатии получим данные всех пользователей бота:

📝 <b>Информация о столбцах:</b>
🆔 tg_id - телеграм ID пользователя
👤 name - имя (введенное при регистрации)
📱 username - имя пользователя без @
🔮 tokens_for_NoD - токены разбора числа судьбы
📅 tokens_for_NoPY - токены разбора числа персонального года
"""
    await message.answer(help_text, parse_mode="HTML", reply_markup=kb.admin_menu)
    
@admin.message(F.photo)   
@admin.message(F.text)
async def trash(message: Message):
    await message.answer('Привет!\n\nДля работы с ботом нажмите /start \nНужна помощь? /help')