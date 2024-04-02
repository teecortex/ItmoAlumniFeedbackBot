import asyncio

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import Poll
from middlewares import EmailTypeFilter

poll_router = Router(name="poll")

@poll_router.message(StateFilter(None), Command("poll"))
async def cmd_isu(message: Message, state: FSMContext):
    await message.answer(text="Введи свой ИСУ, пожалуйста (всего 6 цифр)")
    await state.set_state(Poll.respond_to_isu)

@poll_router.message(Poll.respond_to_isu, F.text.regexp(r"^\d{6}$"))
async def get_isu(message: Message, state: FSMContext):
    await state.update_data(isu=F.text)
    await message.answer("Супер! Можешь ввести еще свое ФИО")
    await state.set_state(Poll.respond_to_name_surname)

@poll_router.message(Poll.respond_to_isu)
async def error_isu(message: Message):
    await message.answer("Ты немного неправильно ввел. Должно быть всего 6 последовательных цифр. Попробуй еще раз")

@poll_router.message(Poll.respond_to_name_surname, F.text.regexp(r"^[А-Яa-яA-Za-z\s]*$"))
async def get_surname_name(message: Message, state: FSMContext):
    await state.update_data(surname_name=F.text)
    await message.answer("Отлично. Введи еще электронную почту пожалуйста")
    await state.set_state(Poll.respond_to_email)


@poll_router.message(Poll.respond_to_name_surname)
async def error_surname_name(message: Message):
    await message.answer("Ты неправильно ввел. Нужно ввести в формате Фамилия Имя Отчество(при наличии). Попробуй еще раз")


@poll_router.message(Poll.respond_to_email, EmailTypeFilter())
async def get_email(message: Message, state: FSMContext):
    await message.answer("Замечательно!")
    await asyncio.sleep(2)
    await message.answer("Теперь начнем наш опрос! Понравилась ли тебе встреча?")

@poll_router.message(Poll.respond_to_email)
async def error_email(message: Message):
    await message.answer("Ты неправильно ввел почту, давай еще раз")