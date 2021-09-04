# --------------Main file sample--------------

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import environ
import asyncio


loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
# MemoryStorage is needed if using FSM
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

if __name__ == '__main__':
    executor.start_polling(dp)


# -------------StateGroup sample--------------

class StateGroupClass(StatesGroup):
    state = State()
    another_state = State()


# ----------Message handlers' samples---------

@dp.message_handler(Text(contains='text'))
async def func(message: Message, state: FSMContext):
    pass


@dp.message_handler(Command('CommandText'))
async def show_subscriptions(message: Message):
    pass


@dp.message_handler(state=StateGroupClass.state)
async def add_pattern(message: Message, state: FSMContext):
    pass


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)


# -How to get/put data into StateGroup memory-

    async with state.proxy() as data:
        data['name'] = message.text
    
    await state.update_data(age=int(message.text))

    async with state.proxy() as data:
        data['gender'] = message.text
        variable = data['name']
