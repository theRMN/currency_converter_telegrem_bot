from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types

from logic import currency
from config import API_TOKEN
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    count = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Для получения списка команд введи - /help', reply=False)


@dp.message_handler(commands=['help'])
async def menu(message: types.Message):
    await message.reply(
        text='''
Список комманд:
Калькулятор - /calculate
Узнать актуальный курс - /ac
''',
        reply=False)


@dp.message_handler(state=Form.count)
async def converter(message: types.Message, state: FSMContext):
    count = message.text.split()

    try:
        str(count[0].upper())
        float(count[1])
    except ValueError:
        await message.reply('Что то пошло не так, попробуйте снова.')
        await state.finish()

    cur = str(count[0].upper())
    value = float(count[1])

    if count[0].upper() in currency().keys():
        await message.reply(f'{count[1]} {cur} --- {round((float(currency()[cur]) * value), 2)} KZT', reply=False)
        await state.finish()
    else:
        await message.reply('Что то пошло не так, попробуйте снова.')
        await state.finish()


@dp.message_handler(commands=['ac'])
async def ac(message: types.Message):
    text = ''
    for i in currency().items():
        text += f'{i[0]} --- {i[1]} KZT\n'
    await message.reply(f'Актуальный курс:\n{text}')


@dp.message_handler(commands=['calculate'])
async def calc(message: types.Message):
    await Form.count.set()
    await message.reply('Введите валюту и число, например "USD 20"', reply=False)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


