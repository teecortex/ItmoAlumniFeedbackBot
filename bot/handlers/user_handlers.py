import asyncio

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.states import Poll, User_Data
from bot.filters.filters import EmailTypeFilter
from bot.keyboards.keyboard_utils import (keyboard_grade, keyboard_instruments,
                                          keyboard_inter_problems,keyboard_org_problems)

start_router = Router(name="start")
registration_router = Router(name="registration")
poll_router = Router(name="poll")


@start_router.message(Command("start"))
async def starting(message: Message):
    await message.answer("Привет!\nЯ бот, который собирает фидбек от встречи менторов с менти.\nДля того, чтобы пройти"
                         " опрос нужно сначала зарегестрироваться.\nЧтобы начать регистрацию введи команду /register")


@registration_router.message(Command("register"))
async def cmd_isu(message: Message, state: FSMContext):
    await message.answer(text="Введи свой ИСУ, пожалуйста (всего 6 цифр)")
    await state.set_state(User_Data.respond_to_isu)

# @registration_router.message(~StateFilter(None), Command("stop"))
# async def stop_poll(message: Message, state: FSMContext):
#     await message.answer("Хорошо! Закончим наш опрос раньше времени", reply_markup=ReplyKeyboardRemove())
#     await state.clear()


@registration_router.message(User_Data.respond_to_isu, F.text.regexp(r"^\d{6}$"))
async def get_isu(message: Message, state: FSMContext):
    await state.update_data(isu=F.text)
    await message.answer("Супер! Можешь ввести еще свое ФИО")
    await state.set_state(User_Data.respond_to_name_surname)

@registration_router.message(User_Data.respond_to_isu)
async def error_isu(message: Message):
    await message.answer("Ты немного неправильно ввел. Должно быть всего 6 последовательных цифр. Попробуй еще раз")

@registration_router.message(User_Data.respond_to_name_surname, F.text.regexp(r"^[А-Яa-яA-Za-z\s]*$"))
async def get_surname_name(message: Message, state: FSMContext):
    await state.update_data(surname_name=F.text)
    await message.answer("Отлично. Введи еще электронную почту пожалуйста")
    await state.set_state(User_Data.respond_to_email)


@registration_router.message(User_Data.respond_to_name_surname)
async def error_surname_name(message: Message):
    await message.answer("Ты неправильно ввел. Нужно ввести в формате Фамилия Имя Отчество(при наличии). Попробуй еще раз")


@registration_router.message(User_Data.respond_to_email, EmailTypeFilter())
async def get_email(message: Message, state: FSMContext):
    await message.answer("Замечательно!\nТеперь, чтобы дать фидбек, тебе нужно ввести команду /feedback")
    # await asyncio.sleep(1)
    # await message.answer("Была ли встреча полезна для тебя? (1 - абсолютно бесполезно, 5 - очень полезно)",
    #                      reply_markup=keyboard_grade)

    await state.set_state(Poll.respond_to_utility)

@registration_router.message(User_Data.respond_to_email)
async def error_email(message: Message):
    await message.answer("Ты неправильно ввел почту, давай еще раз")

@poll_router.message(Command("feedback"))
async def get_utility_grade(message: Message, state: FSMContext):
    await message.answer("Была ли встреча полезна для тебя? (1 - абсолютно бесполезно, 5 - очень полезно)",
                          reply_markup=keyboard_grade)

    await state.set_state(Poll.respond_to_instruments)

@poll_router.message(Poll.respond_to_instruments, F.text.in_({'1','2','3','4','5'}))
async def get_instruments(message: Message, state: FSMContext):
    await message.answer("Применил(а) ли ты советы/инструменты, которые предложил тебе ментор? (Выбери ответ из предложенных)",
                         reply_markup=keyboard_instruments)
    await state.set_state(Poll.respond_to_inter_problems)

@poll_router.message(Poll.respond_to_instruments)
async def error_utility_grade(message: Message):
    await message.answer("Ты не совсем правильно ввел, нужно ввести целое число от 1 до 5",
                         reply_markup=keyboard_grade)



@poll_router.message(Poll.respond_to_inter_problems, F.text.in_({'Да','Нет, но планирую',
                                                              'Нет, ничего нового или подходящего не было предложено'}))
async def get_inter_problems(message: Message, state: FSMContext):
    await message.answer("Супер! Теперь непосредственно про саму встречу", reply_markup=ReplyKeyboardRemove())
    await message.answer("Какие проблемы возникли при взаимодействии с ментором? "
                         "(Можешь ввести что-то не из предложенных вариантов)",
                         reply_markup=keyboard_inter_problems)

    await state.set_state(Poll.respond_to_org_problems)

@poll_router.message(Poll.respond_to_inter_problems)
async def error_instruments(message: Message):
    await message.answer("Тебе нужно выбрать что-то из предложенных вариантов")

@poll_router.callback_query(Poll.respond_to_org_problems)
async def get_inter_problems_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Какие проблемы возникли в организационной части? (Можешь ввести что-то не из предложенных вариантов)",
                                  reply_markup=keyboard_org_problems)

    await state.set_state(Poll.respond_to_advice)

@poll_router.message(Poll.respond_to_org_problems)
async def get_inter_problems_message(message: Message, state: FSMContext):
    await message.answer("Какие проблемы возникли в организационной части? (Можешь ввести что-то не из предложенных вариантов)", reply_markup=keyboard_org_problems)

    await state.set_state(Poll.respond_to_advice)


@poll_router.callback_query(Poll.respond_to_advice)
async def get_org_problems(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("И напоследок. Поделись своими предложениями по улучшению программы, ам это поможет стать еще лучше :)")

    await state.set_state(Poll.respond_to_end_of_poll)


@poll_router.message(Poll.respond_to_advice)
async def get_org_problems(message: Message, state: FSMContext):
    await message.answer("И напоследок. Поделись своими предложениями по улучшению программы, ам это поможет стать еще лучше :)")

    await state.set_state(Poll.respond_to_end_of_poll)

@poll_router.message(Poll.respond_to_end_of_poll)
async def get_advice(message: Message, state: FSMContext):
    await message.answer("Отлично! Опрос окончен)")

    await state.clear()







