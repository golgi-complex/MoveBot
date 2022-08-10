from aiogram import types, Dispatcher
from main import dp
from dictionary import CENSURE_SET
import string


#@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text.lower().translate(str.maketrans('', '', string.punctuation)) in CENSURE_SET:
        await message.reply('Фу, как не культурно!')
        await message.delete()


def register_handlers_censure(dp: Dispatcher):
    dp.register_message_handler(echo_send)
