import asyncio, random, logging, psycopg2
from aiogram import Bot, Dispatcher
from main import dp, bot
from handlers import arts

dp.include_routers(arts.router)

async def main(): # поллинг бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())