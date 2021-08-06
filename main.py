import logging
from logic import actual_course
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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


@dp.message_handler(commands=['ac'])
async def ac(message: types.Message):
    await message.reply(f'Актуальный курс:\n1 доллар = {actual_course()} тенге', reply=False)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def converter(message: types.Message):
    course = float(actual_course())
    text = message.text
    try:
        text = int(text)
        await message.reply(f'{text} долларов = {text * round(course, 1)} тенге', reply=False)
    except ValueError:
        await message.reply('Введите число:')


# @dp.message_handler(commands=['calculate'])
# async def cc(message: types.Message):
#     ...

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
