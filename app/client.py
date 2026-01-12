import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from app.states import Reg, Enter, RefilBalance
from datetime import datetime
from decimal import Decimal

from decimal import Decimal
from app.texts_with_description import DESTINY_TEXTS, PERSONAL_YEAR_TEXTS
from app.validation_functions import is_valid_name, is_valid_birth_date, is_valid_count_tokens

import app.keyboards as kb

from app.database.requests import set_user, update_user, get_user, calculate_NoD, calculate_NoPY

from dotenv import load_dotenv

load_dotenv()

client = Router()

@client.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    
    is_user = await set_user(message.from_user.id, message.from_user.username)
    if not is_user:
        await message.answer('👋🏻Добро пожаловать!\nПройдите процесс регистрации...📋\n\nВведите ваше имя✍️',
                             reply_markup=await kb.clients_name(message.from_user.first_name))
        await state.set_state(Reg.name)
    else:
        await message.answer('👋🏻Добро пожаловать! Я нумерологический бот Numly. Ознакомьтесь с меню⬇️',
                             reply_markup=kb.menu)
        

@client.message(Reg.name)
async def get_reg_name(message: Message, state: FSMContext):
    name_str = message.text.strip()
    
    if not is_valid_name(name_str):
        await message.answer(
            '❌ **Неверный формат имени!**\n\n'
            '👤 **Пожалуйста, введите ваше имя:**\n\n'
            '✅ **Примеры правильных имен:**\n'
            '• Иван\n'
            '• Анна\n'
            '• Александр\n'
            '• Мария\n\n'
            '📝 **Правила ввода:**\n'
            '• Только буквы (русские или английские)\n'
            '• Без цифр и специальных символов\n'
            '• От 2 до 15 символов\n'
            '✍️ **Введите ваше имя:**',
            reply_markup=kb.back_to_menu,
            parse_mode="Markdown"
        )
        
        return
    
    valid_name = name_str
    await state.update_data(name=valid_name.capitalize())
    
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'])
    await message.answer('✅Вы успешно зарегистрированы!\n\nДобро пожаловать!👋🏻 Я нумерологический бот Numly. Ознакомьтесь с меню⬇️',
                         reply_markup=kb.menu)
    await state.clear()


@client.callback_query(F.data == 'back_to_menu')
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        'Добро пожаловать!👋🏻 Я нумерологический бот Numly. Ознакомьтесь с меню⬇️',
        reply_markup=kb.menu
    )
    

@client.message(F.text == '🔮Число судьбы')
async def enter_date_of_birth(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if Decimal(user.tokens_for_NoD) > 0:
        
        await state.set_state(Enter.num_of_destiny)
        await message.answer('✍️Введите дату рождения\n\nФормат: ЧЧ.ММ.ГГГГ', reply_markup=kb.back_to_menu)
    else:
        await message.answer(f'Недостаточно токенов для разбора!\n\nВаш текущий баланс токенов: {user.tokens_for_NoD}\nОбратитесь к администратору для пополнения баланса!',
                             reply_markup=kb.back_to_menu)
    
@client.message(Enter.num_of_destiny)
async def calculate_num_of_destiny(message: Message, state: FSMContext):
    date_text = message.text.strip()
    user = await get_user(message.from_user.id)
    
    if Decimal(user.tokens_for_NoD) > 0:
        
        if not is_valid_birth_date(date_text):
            await message.answer(
                '❌ **Неверный формат даты!**\n\n'
                '📅 **Пожалуйста, введите дату рождения в формате:**\n'
                '**ДД.ММ.ГГГГ**\n\n'
                '✅ **Примеры правильных дат:**\n'
                '• 01.01.2000\n'
                '• 15.09.1990\n'
                '• 30.12.1985\n\n'
                '✍️ **Введите вашу дату рождения:**',
                reply_markup=kb.back_to_menu,
                parse_mode="Markdown"
            )
            # Состояние НЕ очищаем - ждем правильный ввод
            return
        
        date_of_birth = date_text
        
        def calculate_num(str_date_of_birth):
            num_of_destiny = sum([int(el) for el in str_date_of_birth if el.isdigit()])
            
            while num_of_destiny > 9:
                if num_of_destiny in [11, 22, 33]:
                    return num_of_destiny # Это мастер-число
                num_of_destiny = sum([int(el) for el in str(num_of_destiny)])
            return num_of_destiny
        
        num_of_destiny = calculate_num(date_of_birth)
        
        match num_of_destiny:
            case num if num in DESTINY_TEXTS:
                text_data = DESTINY_TEXTS[num]
                await calculate_NoD(message.from_user.id) # пересчитали баланс
                await message.answer(
                    f"{text_data['title']}\n\n{text_data['description']}"
                )
                await state.clear()
            case _:
                await message.answer("Неизвестное число судьбы")
                await state.clear()
    else:
        await message.answer(f'Недостаточно токенов для разбора!\n\nВаш текущий баланс токенов: {user.tokens_for_NoD}\nОбратитесь к администратору для пополнения баланса!',
                             reply_markup=kb.back_to_menu)
        await state.clear()


@client.message(F.text == '📅Персональное число года')
async def enter_date_of_birth(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if Decimal(user.tokens_for_NoPY) > 0:
        await state.set_state(Enter.num_of_personal_year)
        await message.answer('✍️Введите дату рождения\n\nФормат: ЧЧ.ММ.ГГГГ', reply_markup=kb.back_to_menu)
    else:
        await message.answer(f'Недостаточно токенов для разбора!\n\nВаш текущий баланс токенов: {user.tokens_for_NoPY}\nОбратитесь к администратору для пополнения баланса!',
                             reply_markup=kb.back_to_menu)

@client.message(Enter.num_of_personal_year)
async def calculate_num_of_personal_year(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if Decimal(user.tokens_for_NoPY) > 0:
        date_text = message.text.strip()
        
        if not is_valid_birth_date(date_text):
            await message.answer(
                '❌ **Неверный формат даты**!\n\n'
                '📅 **Пожалуйста, введите дату рождения в формате:**\n'
                'ДД.ММ.ГГГГ**\n\n'
                '✅ **Примеры правильных дат**:\n'
                '• 01.01.2000\n'
                '• 15.09.1990\n'
                '• 30.12.1985\n\n'
                '✍️ **Введите вашу дату рождения:**',
                reply_markup=kb.back_to_menu,
                parse_mode="Markdown"
            )
            # Состояние НЕ очищаем - ждем правильный ввод
            return
        
        date_of_birth = date_text
        
        def calculate_num_year(date_of_birth):
            current_year = datetime.now().year
            new_date = date_of_birth[:-4] + str(current_year)
            
            num_of_personal_year = sum([int(el) for el in new_date if el.isdigit()])
            
            while num_of_personal_year > 9:
                if num_of_personal_year in [11, 22, 33]:
                    return num_of_personal_year # Это мастер-число
                num_of_personal_year = sum([int(el) for el in str(num_of_personal_year)])
            return num_of_personal_year
        
        num_of_personal_year = calculate_num_year(date_of_birth)
        
        
        match num_of_personal_year:
            case num if num in PERSONAL_YEAR_TEXTS:
                text_data = PERSONAL_YEAR_TEXTS[num]
                await calculate_NoPY(message.from_user.id) # пересчитали баланс
                await message.answer(
                    f"{text_data['title']}\n\n{text_data['description']}"
                )
                await state.clear()
            
            case _:
                await message.answer('Неизвестное число персонального года')
                await state.clear()
    else:
        await message.answer(f'Недостаточно токенов для разбора!\n\nВаш текущий баланс токенов: {user.tokens_for_NoPY}\nОбратитесь к администратору для пополнения баланса!',
                             reply_markup=kb.back_to_menu)
        await state.clear()
        

 
@client.message(F.text == '💎Мой баланс токенов')
async def view_count_tokens(message: Message):
    user = await get_user(message.from_user.id)
    
    await message.answer(
    f'🪙 <b>КОШЕЛЕК ТОКЕНОВ</b>\n\n'
    f'✨✨✨✨✨✨✨\n\n'
    f'🔮 <b>Число судьбы:</b>\n'
    f'🌟 Доступно: {user.tokens_for_NoD} токенов 🌟\n\n'
    f'📅 <b>Персональный год:</b>\n'
    f'🎯 Доступно: {user.tokens_for_NoPY} токенов 🎯\n\n'
    f'💎 Всегда к вашим услугам!',
    parse_mode="HTML"
)
    


@client.message(F.text == '💰Пополнить баланс')
async def choice_user(message: Message, state: FSMContext):
    await state.set_state(RefilBalance.choice_analysis)
    await message.answer('Выберите тип разбора', reply_markup=kb.choices)
    
@client.message(RefilBalance.choice_analysis)
async def choice_count_tokens(message: Message, state: FSMContext):
    choice = message.text.strip()
    
    if choice not in ['Разбор числа судьбы', 'Разбор числа персонального года']:
        await message.answer(
            '❌Неверный формат, повторите попытку',
            reply_markup=kb.back_to_menu
        )
        return
    
    await state.update_data(choice=choice)
    await state.set_state(RefilBalance.choice_sum)
    await message.answer('✍️Введите количество токенов для пополнения')

@client.message(RefilBalance.choice_sum)
async def send_info(message: Message, state: FSMContext):
    count_tokens = message.text.strip()
    
    if not is_valid_count_tokens(count_tokens):
        await message.answer(
            '❌ Неверный формат количества токенов\n\n'
            '📋 Требования:\n'
            '• Только положительное число\n'
            '• Не равно ноль\n'
            '✍️ Введите количество токенов:',
            reply_markup=kb.back_to_menu
        )
        return
    
    await state.update_data(count_tokens=count_tokens)
    
    data = await state.get_data()
    user = await get_user(message.from_user.id)
    full_info = (
        f'❗️Новая заявка на пополнение баланса токенов❗️\n\n'
        f'👨‍💻Пользователь: {user.name}, @{user.username}, телеграм айди: {user.tg_id}\n'
        f'📍Выбрал разбор: {data['choice']}\n'
        f'🛒Количество токенов: {data['count_tokens']}'
    )
    
    await message.bot.send_message(int(os.getenv('ADMIN_PM')), full_info)
    await message.answer('❤️Спасибо! Ваша заявка на пополнение баланса токенов принята✅\n\nАдминистратор свяжется с вами в ближайшее время...👨‍💻',
                         reply_markup=kb.menu)
    await state.clear()
    

@client.message(Command('help'))
@client.message(F.text == '📞Помощь')
async def help(message: Message):
    await message.answer(
    '🆘 *Помощь*\n\n'
    '🌟 *Доступные разделы:*\n\n'
    '🔮 *Разбор числа судьбы*\n'
    'Расшифровка вашего жизненного пути, талантов и предназначения на основе даты рождения.\n\n'
    '📅 *Разбор персонального года*\n'
    'Анализ энергии текущего года и рекомендации для успешного периода.\n\n'
    '💰 *Пополнить баланс*\n'
    'Приобретение токенов для получения разборов.\n\n'
    '💎 *Мой баланс*\n'
    'Просмотр доступного количества токенов.\n\n'
    '📊 *Информация о токенах:*\n'
    '• Разбор числа судьбы: X токенов\n'
    '• Разбор персонального года: Y токенов\n\n'
    '🔄 *Как получить разбор:*\n'
    '1. Нажмите на нужный раздел\n'
    '2. Введите необходимые данные\n'
    '3. Получите подробный анализ\n\n'
    '📞 *Поддержка:*\n'
    f'Для технических вопросов: {os.getenv('MAIL')}',
    parse_mode="Markdown"
)