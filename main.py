from logic import actual_course
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN

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


@dp.message_handler(commands=['calculate'])
async def converter(message: types.Message):
    await message.reply('Введите количество тенге:')

    await message.reply('Sorry')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
