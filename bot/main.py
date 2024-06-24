import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers.user_handlers import poll_router, start_router, registration_router
from aiogram.filters import StateFilter
from config_data.config import load_config, Config



# config = load_config()
# dp = Dispatcher()
# bot = Bot(token=config.tg_bot.bot_token)
#
# @dp.message(StateFilter(None), Command('start'))
# async def cmd_start(message: types.Message):
#     await message.answer("Привет! Я бот, собирающий фидбек касательно встречи с менторами!")
#     await message.answer("Чтобы дать фидбек тебе всего лишь нужно ввести команду /poll, а если хочешь выйти из опроса, "
#                          "то нужно ввести команду /stop")
#
#
# @dp.message(Command('help'))
# async def cmd_help(message: types.Message):
#     await message.answer("Чтобы дать фидбек тебе всего лишь нужно ввести команду /poll, а если хочешь выйти из опроса, "
#                          "то нужно ввести команду /stop")

async def main():
    config: Config = load_config()

    # storage = ...
    bot = Bot(
        token=config.tg_bot.bot_token
    )
    dp = Dispatcher()

    #Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(poll_router)

    #Регистрируем миддлвари


    #Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())