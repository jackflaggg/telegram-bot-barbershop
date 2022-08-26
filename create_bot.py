from SimpleQIWI import *
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

# storage = MemoryStorage
from data import NUMBER_QIWI
from data_base.db_commands import Database

bot = Bot(token='5327606415:AAG_4Dyh7sJuxvCAnRi0e6O_koLM1lN2ARs')

# token выводить в .env
qiwi = QApi(token='4b53a4b1221946855ca0e65f346f53f7', phone=NUMBER_QIWI)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()
