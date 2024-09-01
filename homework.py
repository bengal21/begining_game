from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from tok import tok_telegram, tok_bid
from random import randint, choice
import os
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

bot = Bot(token=tok_bid, parse_mode="HTML")
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

cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', ['Детская', 5,
                                                           'На этой горке можно оставить детей, пока вы сами получаете адреналин на одной из взрослых горок'])
cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', ['Закатное солнце', 20,
                                                            'Одна из самых популярных горок, Можно кататься как взрослым, так и детям от шести лет'])
cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', ['Жираф', 31,
                                   'На этой горке можно испытать те же чувства, что и при скатывании по шее настоящего жирафа. Одна из самых популярных горок'])
cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', ['Красный дракон', 53,
                                   'Горка в японском стиле. В верхней части тоннеля горки расположено несколько мониторов, на которых можно посмотреть аниме'])
cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', ['Кантемир', 100,
                   'Не самая популярная горка, потому что не все любят экстрим. Если вы хотите провести ближайший час незабываемо, эта длинная горка - для вас'])

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
    await message.answer('Спасибо! Менеджер свяжется с вами для оплаты заказа.')
    data = await state.get_data()
    cur.execute('INSERT INTO requests(name, number) VALUES (?, ?)', [data.get('name'), data.get('number')])
    await HandleClient.waiting_for_slide.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(on_slide, state=HandleClient.waiting_for_slide)
    dp.register_message_handler(on_name, state=HandleClient.waiting_for_name)
    dp.register_message_handler(on_number, state=HandleClient.waiting_for_number)


register_handlers(dp)

executor.start_polling(dp, skip_updates=True)
