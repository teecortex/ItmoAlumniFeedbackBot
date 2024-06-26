from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.states import Poll, User_Data
from bot.filters.filters import EmailTypeFilter
from bot.keyboards.keyboard_utils import (keyboard_grade, keyboard_instruments,
                                          keyboard_inter_problems,keyboard_org_problems, inter_problems, org_problems)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from bot.models.models import Menti, Mentor, Feedback

start_router = Router(name="start")
registration_router = Router(name="registration")
poll_router = Router(name="poll")


@start_router.message(Command("start"))
async def starting(message: Message, session: AsyncSession):
    result = await session.execute(select(Menti).where(Menti.telegram_id==message.from_user.id))
    if len(result.all()) == 0:
        await message.answer("Привет!\nЯ бот, который собирает фидбек от встречи менторов с менти.\nДля того, чтобы пройти"
                         " опрос нужно сначала зарегестрироваться.\nЧтобы начать регистрацию введи команду /register")
    else:
        await message.answer("Привет!\nЯ бот, который собирает фидбек от встречи менторов с менти. Для того, чтобы пройти опрос можешь ввести команду /feedback")

@registration_router.message(StateFilter(None), Command("register"))
async def cmd_isu(message: Message, state: FSMContext, session: AsyncSession):
    result = await session.execute(select(Menti).where(Menti.telegram_id==message.from_user.id))
    if len(result.all()) > 0:
        await message.answer("Вы уже зарегестрированы.\nМожете дать фидбек с помощью /feedback")
    else:
        await session.merge(Menti(isu=0, telegram_id=message.from_user.id, email=''))
        await session.commit()
        await message.answer(text="Введи свой ИСУ, пожалуйста (всего 6 цифр)")
        await state.set_state(User_Data.respond_to_isu)

@registration_router.message(Command("register"))
async def qwerty(message: Message):
    await message.answer("Сейчас вы не можете воспользоваться этой командой, потому что либо уже регестрируетесь, либо проходите опрос")

@registration_router.message(User_Data.respond_to_isu, F.text.regexp(r"^\d{6}$"))
async def get_isu(message: Message, state: FSMContext, session: AsyncSession):
    await session.execute(update(Menti).where(Menti.telegram_id==message.from_user.id).values(isu=int(message.text)))
    await session.commit()
    await message.answer("Супер! Можешь ввести еще свое ФИО\n(В формате Фамилия Имя Отчество (Отчество при наличии))")
    await state.set_state(User_Data.respond_to_name_surname)

@registration_router.message(User_Data.respond_to_isu)
async def error_isu(message: Message):
    await message.answer("Ты немного неправильно ввел. Должно быть всего 6 последовательных цифр. Попробуй еще раз")

@registration_router.message(User_Data.respond_to_name_surname, F.text.regexp(r"^[А-Яa-яA-Za-z\s]*$"), F.text.split().len() >= 2)
async def get_surname_name(message: Message, state: FSMContext, session: AsyncSession):
    full_name = message.text.split()
    if len(full_name) == 2:
        await session.execute(update(Menti).where(Menti.telegram_id == message.from_user.id).values(surname=full_name[0], name=full_name[1]))
    else:
        await session.execute(update(Menti).where(Menti.telegram_id == message.from_user.id).values(surname=full_name[0], name=full_name[1], patronymic=full_name[2]))

    await session.commit()
    await message.answer("Отлично. Введи еще электронную почту пожалуйста")
    await state.set_state(User_Data.respond_to_email)


@registration_router.message(User_Data.respond_to_name_surname)
async def error_surname_name(message: Message):
    await message.answer("Ты неправильно ввел. Нужно ввести в формате Фамилия Имя Отчество(при наличии). Попробуй еще раз")


@registration_router.message(User_Data.respond_to_email, EmailTypeFilter())
async def get_email(message: Message, state: FSMContext, session: AsyncSession):
    await session.execute(update(Menti).where(Menti.telegram_id==message.from_user.id).values(email=message.text))
    await session.commit()
    await message.answer("Замечательно!\nТеперь, чтобы дать фидбек, тебе нужно ввести команду /feedback")
    await state.clear()


@registration_router.message(User_Data.respond_to_email)
async def error_email(message: Message):
    await message.answer("Ты неправильно ввел почту, давай еще раз")


@poll_router.message(StateFilter(None), Command("feedback"))
async def get_mentor(message: Message, state: FSMContext, session: AsyncSession):
    result = await session.execute(select(Menti).where(Menti.telegram_id==message.from_user.id))
    if len(result.all()) > 0:
        await message.answer("Напиши фамилию и имя ментора, с которым у тебя была встреча")
        await state.set_state(Poll.respond_to_utility)
    else:
        await message.answer("Для прохождения опроса нужно быть зарегестрированным. Для регистрации введите команду /register")

@poll_router.message(Command("feedback"))
async def error_feedback(message: Message):
    await message.answer("Сейчас вы не можете воспользоваться этой командой, потому что либо уже регестрируетесь, либо проходите опрос")


@poll_router.message(Poll.respond_to_utility, F.text.regexp(r"^[А-Яa-яA-Za-z\s]*$"), F.text.split().len() == 2)
async def get_utility_grade(message: Message, state: FSMContext, session: AsyncSession):
    mentor_full_name = message.text.split()
    query = await session.execute(select(Mentor).where(Mentor.surname==mentor_full_name[0], Mentor.name==mentor_full_name[1]))
    mentor = query.scalar()

    if mentor is not None:
        menti = await session.execute(select(Menti.id).where(Menti.telegram_id==message.from_user.id))
        menti_id = menti.scalar()
        await state.update_data(menti_id=menti_id)

        await session.merge(Feedback(menti_id=menti_id, mentor_id=mentor.id))
        await session.commit()

        await state.update_data(mentor_id=mentor.id)


        await message.answer("Была ли встреча полезна для тебя? (1 - абсолютно бесполезно, 5 - очень полезно)",
                             reply_markup=keyboard_grade)
        await state.set_state(Poll.respond_to_instruments)
    else:
        await message.answer("Хм. Такого ментора нет, ты уверен, что правильно ввел его фамилию и имя?")


@poll_router.message(Poll.respond_to_utility)
async def error_mentor(message: Message):
    await message.answer("Ты неправильно ввел. Нужно ввести в формате Фамилия Имя")


@poll_router.message(Poll.respond_to_instruments, F.text.in_({'1','2','3','4','5'}))
async def get_instruments(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id==data['menti_id'], Feedback.mentor_id==data['mentor_id']).values(mentis_rate=int(message.text)))
    await session.commit()

    await message.answer("Применил(а) ли ты советы/инструменты, которые предложил тебе ментор? (Выбери ответ из предложенных)",
                         reply_markup=keyboard_instruments)
    await state.set_state(Poll.respond_to_inter_problems)

@poll_router.message(Poll.respond_to_instruments)
async def error_utility_grade(message: Message):
    await message.answer("Ты не совсем правильно ввел, нужно ввести целое число от 1 до 5",
                         reply_markup=keyboard_grade)


@poll_router.message(Poll.respond_to_inter_problems, F.text.in_({'Да','Нет, но планирую',
                                                              'Нет, ничего нового или подходящего не было предложено'}))
async def get_inter_problems(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(instruments=message.text))
    await session.commit()

    await message.answer("Супер! Теперь непосредственно про саму встречу", reply_markup=ReplyKeyboardRemove())
    await message.answer("Какие проблемы возникли при взаимодействии с ментором? "
                         "(Можешь ввести что-то не из предложенных вариантов)",
                         reply_markup=keyboard_inter_problems)

    await state.set_state(Poll.respond_to_org_problems)

@poll_router.message(Poll.respond_to_inter_problems)
async def error_instruments(message: Message):
    await message.answer("Тебе нужно выбрать что-то из предложенных вариантов")

@poll_router.callback_query(Poll.respond_to_org_problems)
async def get_inter_problems_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(interaction_problems=inter_problems[int(callback.data)]))
    await session.commit()

    print(callback.message.text)

    await callback.message.answer("Какие проблемы возникли в организационной части? (Можешь ввести что-то не из предложенных вариантов)",
                                  reply_markup=keyboard_org_problems)

    await state.set_state(Poll.respond_to_advice)

@poll_router.message(Poll.respond_to_org_problems)
async def get_inter_problems_message(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(interaction_problems=message.text))
    await session.commit()

    await message.answer("Какие проблемы возникли в организационной части? (Можешь ввести что-то не из предложенных вариантов)", reply_markup=keyboard_org_problems)

    await state.set_state(Poll.respond_to_advice)


@poll_router.callback_query(Poll.respond_to_advice)
async def get_org_problems(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(org_problems=org_problems[int(callback.data)]))
    await session.commit()

    await callback.message.answer("И напоследок. Поделись своими предложениями по улучшению программы, ам это поможет стать еще лучше :)")

    await state.set_state(Poll.respond_to_end_of_poll)


@poll_router.message(Poll.respond_to_advice)
async def get_org_problems(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(org_problems=message.text))
    await session.commit()

    await message.answer("И напоследок. Поделись своими предложениями по улучшению программы, ам это поможет стать еще лучше :)")

    await state.set_state(Poll.respond_to_end_of_poll)

@poll_router.message(Poll.respond_to_end_of_poll)
async def get_advice(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await session.execute(update(Feedback).where(Feedback.menti_id == data['menti_id'], Feedback.mentor_id == data['mentor_id']).values(suggestions=message.text))
    await session.commit()

    await message.answer("Отлично! Опрос окончен)")

    await state.clear()
