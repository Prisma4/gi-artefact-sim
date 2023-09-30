import logging
from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO)
bot = Bot(token=open('artefactsim/token.txt').readline())
dp = Dispatcher()