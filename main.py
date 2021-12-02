from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types

from logic import cur_convert, get_currency_data
from config import API_TOKEN, MAIN_CURRENCY
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
Конвертер - /conv
Узнать актуальный курс - /ac
''',
        reply=False)


@dp.message_handler(state=Form.count)
async def converter(message: types.Message, state: FSMContext):
    count = message.text.split()

    if len(count) != 3:
        await message.reply('Неправильный формат ввода.')
        await state.finish()
        return

    try:
        str(count[0].upper())
        float(count[1])
        str(count[2].upper())
    except ValueError:
        await message.reply('Что то пошло не так, попробуйте снова.')
        await state.finish()
        return

    cur = str(count[0].upper())
    amount = float(count[1])
    new_cur = str(count[2].upper())
    result = cur_convert(amount, cur, new_cur)

    if result:
        await message.reply(f'{amount} {cur} = {result} {new_cur}', reply=False)
        await state.finish()
    else:
        await message.reply('Нет такой валюты')
        await state.finish()


@dp.message_handler(commands=['ac'])
async def ac(message: types.Message):
    text = ''
    currency_dict = get_currency_data()

    for i in currency_dict.items():
        text += f'{i[0]} --- {i[1]} {MAIN_CURRENCY}\n'

    await message.reply(f'Актуальный курс:\n{text}', reply=False)


@dp.message_handler(commands=['calculate', 'conv'])
async def calc(message: types.Message):
    await Form.count.set()
    await message.reply('Введите валюту, число и базовую валюту,\nнапример "USD 20 KZT"', reply=False)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


