from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from os import environ
import asyncio
from dotenv import load_dotenv


load_dotenv()
loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)
