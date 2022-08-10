from handlers import questionnaire, censure
from aiogram.utils import executor
from main import dp, bot
from data_base import sqlite_db


async def on_startup(_):
    print('Bot is online')
    sqlite_db.sql_start()


questionnaire.register_handlers_questionnaire(dp)
censure.register_handlers_censure(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)