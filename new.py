from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from tok import tok_telegram
from random import randint, choice
import os
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

bot = Bot(token=tok_telegram, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect('aqua.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS slides(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
length INTEGER,
description TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS requests(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
number TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS managers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
tg_id INTEGER
)''')

conn.commit()


class HandleClient(StatesGroup):
    waiting_for_slide = State()
    waiting_for_name = State()
    waiting_for_number = State()


async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('КУПИТЬ БИЛЕТ')
    cur.execute('SELECT name FROM slides')
    slides = cur.fetchall()
    for slide in slides:
        keyboard.add(slide[0])
    await message.answer(
        'Добро пожаловать в аквапарк! Нажмите на название горки, чтобы получить больше информации, или на кнопку "купить билет", чтобы купить билет.',
        reply_markup=keyboard)
    await HandleClient.waiting_for_slide.set()


async def on_slide(message: types.Message):
    if message.text == 'КУПИТЬ БИЛЕТ':
        await message.answer(
            'Стоимость билета - 2000 рублей на весь день. Чтобы купить билет, отправьте в чат своё имя:')
        await HandleClient.waiting_for_name.set()
    else:
        cur.execute('SELECT length, description FROM slides WHERE name = ?', [message.text])
        slide = cur.fetchone()
        await message.answer(f'{message.text} - {slide[1]}.\nПротяжённость горки - {slide[0]} метров.')


async def on_name(message: types.Message, state):
    await state.update_data(name=message.text)
    await message.answer('И номер телефона:')
    await HandleClient.waiting_for_number.set()


async def on_number(message: types.Message, state):
    await state.update_data(number=message.text)

    await message.answer('Спасибо! Менеджер свяжется с вами для оплаты заказа.')
    data = await state.get_data()
    print(data)
    cur.execute('INSERT INTO requests(name, number) VALUES (?, ?)', [data.get('name'), data.get('number')])
    conn.commit()
    cur.execute('SELECT tg_id FROM managers')
    managers = cur.fetchall()
    # for manager in managers:
    #     await bot.send_message(manager[0], f'Имя: {data.get("name")}\nНомер: {data.get("number")}')
    await HandleClient.waiting_for_slide.set()


async def admin(message: types.Message):
    password = message.text.split()[1]
    if password == '1234':
        await message.answer('Теперь в этот чат будут приходить все заявки.')
        cur.execute('INSERT INTO managers(tg_id) VALUES (?)', [message.chat.id])
        conn.commit()
    else:
        print('Неправильный пароль')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(admin, commands="admin", state="*")
    dp.register_message_handler(on_slide, state=HandleClient.waiting_for_slide)
    dp.register_message_handler(on_name, state=HandleClient.waiting_for_name)
    dp.register_message_handler(on_number, state=HandleClient.waiting_for_number)


register_handlers(dp)

executor.start_polling(dp, skip_updates=True)
