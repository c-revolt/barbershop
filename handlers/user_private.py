from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, or_f
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


@user_private_router.message(F.text.lower() == "💈 услуги")
@user_private_router.message(Command("services"))
async def get_services(message: types.Message, session: AsyncSession):
    for service in await orm_get_services(session):
        await message.answer(f"💈 {round(service.price, 0)} ₽ | {service.name} | {service.time} 💈",
                             reply_markup=get_menu_callback_btns(btns={f"Выбрать": f" select_{service.id} "}))


@user_private_router.message(F.text.lower() == "✂️ Барберы")
@user_private_router.message(Command("barbers"))
async def get_barbers(message: types.Message, session: AsyncSession):
    for barber in await orm_get_barbers(session):
        await message.answer_photo(barber.photo,
                                   caption=f"<stronng>{barber.name}</strong> \n"
                                           f"{barber.description}",
                                   reply_markup=get_menu_callback_btns(btns={f"Выбрать": f" select_{barber.id} "}))
