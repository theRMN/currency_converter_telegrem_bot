import logging
from datetime import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from logic import actual_course
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    count = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Для получения списка команд введи /help', reply=False)


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
    course = float(actual_course())
    count = message.text
    try:
        count = int(count)
        await message.reply(f'{count} долларов = {count * round(course, 1)} тенге', reply=False)
        await state.finish()
    except ValueError:
        await message.reply('Введите число:')


@dp.message_handler(commands=['ac'])
async def ac(message: types.Message):
    await message.reply(f'Актуальный курс на момент {datetime.now(tz=None)}:'
                        f'\n1 доллар = {actual_course()} тенге', reply=False)


@dp.message_handler(commands=['calculate'])
async def calc(message: types.Message):
    await Form.count.set()
    await message.reply("Введите число", reply=False)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


