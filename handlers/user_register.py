from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

import re

from database.orm_query import orm_get_services, orm_get_barbers, orm_add_user, orm_get_user
from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_menu_callback_btns
from keyboards.reply import main_menu_kb, profile_kb

user_register_router = Router()
user_register_router.message.filter(ChatTypeFilter(["private"]))


class AddUser(StatesGroup):
    user_name = State()
    user_phone = State()

    user_for_change = None
    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddBarber:phone': 'Введите новый номер телефона:',
    }


@user_register_router.message(StateFilter(None), F.text == "🪪 Профиль")
@user_register_router.message(Command('profile'))
async def start_register(message: types.Message, session: AsyncSession, state: FSMContext, bot: Bot):
    check_user = orm_get_user(session, message.from_user.id)
    if check_user:
        await bot.send_message(message.from_user.id,
                               text='Вы вошли в свой профиль!',
                               reply_markup=profile_kb)
    else:
        await message.answer("Напиши своё имя", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddUser.user_name)


@user_register_router.message(AddUser.user_name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, "Укажите ваш номер телефона")
    await state.update_data(user_name=message.text)
    await state.set_state(AddUser.user_phone)


@user_register_router.message(AddUser.user_phone, or_f(F.text, F.text == "."))
async def add_number(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    if (re.findall(r'^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        data = await state.get_data()
        user_data = {
            'telegram_id': message.from_user.id,
            'user_name': data['user_name'],
            'user_phone': message.text
        }
        await state.update_data(user_phone=message.text)
        await orm_add_user(session, user_data)
        await message.answer("Поздравляем! Вы успешно прошли регистрацию!", reply_markup=main_menu_kb)
        await state.clear()
    else:
        await message.answer("Номер телефона введёт не корректно!")



