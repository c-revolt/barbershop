from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_services, orm_get_barbers
from filters.chat_types import ChatTypeFilter
from keyboards.inline import get_menu_callback_btns
from keyboards.reply import main_menu_kb

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}, добро пожаловать в наш барбершоп!",
        reply_markup=main_menu_kb
    )


@user_private_router.message(F.text.lower() == "💈 услуги 💈")
@user_private_router.message(Command("services"))
async def get_services(message: types.Message, session: AsyncSession):
    services = await orm_get_services(session)
    if (services):
        for service in services:
            await message.answer(f"💵 <strong>{round(service.price, 0)} ₽</strong>  |  🕘 {service.time}\n"
                                 f"💈 {service.name} 💈\n\n"
                                 f"➡️ Тут будет небольшое красивое описание услуги, "
                                 f"которое рассказывает какие будут использоваться инструменты и прочее.\n\n",
                                 reply_markup=get_menu_callback_btns(
                                     btns={f"Выбрать": f"select_services_{service.id}"}))
    else:
        await message.answer(text='К сожалению, услуг пока нет. обратитесь к администратору!')


@user_private_router.message(F.text.lower() == "✂️ барберы ✂️")
@user_private_router.message(Command("barbers"))
async def get_barbers(message: types.Message, session: AsyncSession):
    barbers = await orm_get_barbers(session)
    if (barbers):
        for barber in barbers:
            await message.answer_photo(barber.photo,
                                       caption=f"<strong>{barber.name}</strong> \n"
                                               f"{barber.description}",
                                       reply_markup=get_menu_callback_btns(
                                           btns={f"Выбрать": f"select_barbers_{barber.id}"}))
    else:
        await message.answer(text='Список барберов пуст!')


@user_private_router.message(F.text == "⬅️ Назад")
async def back_to_main_menu(message: types.Message):
    await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu_kb)
