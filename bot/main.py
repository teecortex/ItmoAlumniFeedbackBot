import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from handlers.user_handlers import poll_router, start_router, registration_router
from config_data.config import load_config, Config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.throttling import DbSessionMiddleware


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

    engine = create_async_engine(url=f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DATABASE')}", echo=True)
    session = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(
        token=config.tg_bot.bot_token
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    #Регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(poll_router)

    #Регистрируем миддлвари
    dp.update.middleware(DbSessionMiddleware(session_pool=session))

    #Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



