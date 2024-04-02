import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import poll_router

dp = Dispatcher()
bot = Bot(token=os.environ['BOT_TOKEN'])

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, собирающий фидбек касательно встречи с менторами!")

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(poll_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
