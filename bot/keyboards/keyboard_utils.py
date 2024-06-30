from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_grade = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(i)) for i in range(1, 6)]],
                                     resize_keyboard=True)

keyboard_instruments = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да'),
                                                      KeyboardButton(text='Нет, но планирую')],
                                                      [KeyboardButton(text='Нет, ничего нового или подходящего не было предложено')]],
                                           resize_keyboard=True)

inter_problems = ['Не отвечал или долго отвечал на сообщения','Вел себя некорректно',
                'Не пришел на встречу','Агрессивно навязывал свою точку зрения', 'Проблем при взаимодействии не возникло']

keyboard_inter_problems = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=prob, callback_data=str(index))] for index, prob in enumerate(inter_problems)])

org_problems = ['Координатор не связался','На сайте не было свободных слотов',
               'Неточная информация в сообщении от координатора','Проблемы с доступом в Calendly',
               'Организационных проблем не возникло']
keyboard_org_problems = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=prob, callback_data=str(index))] for index, prob in enumerate(org_problems)])


