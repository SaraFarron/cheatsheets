from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import menu
from . import dp
from . import logger


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: Message, state: FSMContext, raw_state: Optional[str] = None):
    """Allow user to cancel any action"""

    if raw_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Canceled.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command('menu'))
async def send_menu(message: Message):
    """Menu, shows all bot functionality"""

    logger.info(f'sent menu to {message.from_user.username}')

    await message.answer("Please choose an action", reply_markup=menu)