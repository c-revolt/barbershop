from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_service, orm_get_services, orm_delete_service, orm_get_service, \
    orm_update_service, orm_add_barber, orm_update_barber

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import admin_kb, main_menu_kb
from keyboards.inline import get_callback_btns

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

admin_private_router = Router()
admin_private_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


class AddService(StatesGroup):
    name = State()
    price = State()
    time = State()

    service_for_change = None
    texts = {
        'AddService:name': 'Введите название заново:',
        'AddService:price': 'Введите стоимость заново:',
        'AddService:time': 'Этот стейт последний, поэтому...',
    }


class AddBarber(StatesGroup):
    name = State()
    description = State()
    photo = State()
    earnings = None
    completed_jobs = None

    barber_for_change = None
    texts = {
        'AddBarber:name': 'Введите имя заново:',
        'AddBarber:description': 'Введите описание заново:',
        'AddBarber:photo': 'Этот стейт последний, поэтому...',
    }


@admin_private_router.message(Command("admin"))
async def add_service(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, вы в панели администратора. Что хотите сделать?",
                         reply_markup=admin_kb)


@admin_private_router.message(F.text.lower() == "услуги")
async def starring_at_service(message: types.Message, session: AsyncSession):
    for service in await orm_get_services(session):
        await message.answer(
            text=f"💈 {round(service.price, 0)} ₽ <strong>|</strong> "
                 f"{service.name} <strong>|</strong> "
                 f"{service.time}",
            reply_markup=get_callback_btns(btns={
                "🗑 Удалить": f"delete_{service.id}",
                "🖌 Изменить": f"change_{service.id}"
            })
        )
    await message.answer("Выберите услугу")


@admin_private_router.callback_query(F.data.startswith('delete_'))
async def delete_service(callback: types.CallbackQuery, session: AsyncSession):
    service_id = callback.data.split("_")[-1]
    await orm_delete_service(session, int(service_id))

    await callback.answer("Услуга удалена", show_alert=True)
    await callback.message.answer("Услуга удалена!")


@admin_private_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_service(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    serivce_id = callback.data.replace("change_", "")
    service_for_change = await orm_get_service(session, int(serivce_id))

    AddService.service_for_change = service_for_change
    await callback.answer()
    await callback.message.answer("Введите название услуги", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddService.name)


# Добавление УСЛУГИ (FSM)
@admin_private_router.message(StateFilter(None), F.text == "➕ Добавить услугу")
async def add_service(message: types.Message, state: FSMContext):
    await message.answer(
        "🪧 Введите название услуги:", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddService.name)


@admin_private_router.message(StateFilter("*"), Command("отмена"))
@admin_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddService.service_for_change:
        AddService.service_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=admin_kb)


@admin_private_router.message(StateFilter("*"), Command("назад"))
@admin_private_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddService.name:
        await message.answer('Предыдушего шага нет. Или введите название услуги или напишите "отмена"')

    previos = None
    for step in AddService.__all_states__:
        if step.state == current_state:
            await state.set_state(previos)
            await message.answer(f"Ок, вы вернулись к предыдущему шагу,\n{AddService.texts[previos.state]}")
            return
        previos = step


@admin_private_router.message(AddService.name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddService.service_for_change.name)
    else:
        if len(message.text) >= 29:
            await message.answer("Название услуги не должно превышать 29 символов. \nВведите название заново.")
            return

        await state.update_data(name=message.text)
    await message.answer("💷 Укажите цену услуги:")
    await state.set_state(AddService.price)


@admin_private_router.message(AddService.name)
async def add_name_second(message: types.Message):
    await message.answer("Упс! Вы ввели не допустимые данные, ведите текст <b>НАЗВАНИЯ</b> услуги.")


@admin_private_router.message(AddService.price, or_f(F.text, F.text == "."))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddService.service_for_change.price)
    else:
        try:
            float(message.text)
        except:
            await message.answer("Введите корректное значение цены.")
            return
        await state.update_data(price=message.text)
    await message.answer("Введите время на оказание услуги в формате: <strong>1ч</strong> "
                         "или <strong>30м</strong>. Ввод ограничен до 3 символов.")
    await state.set_state(AddService.time)


@admin_private_router.message(AddService.price)
async def add_price_second(message: types.Message):
    await message.answer("Упс! Вы ввели не допустимые данные, ведите <strong>ЦЕНУ</strong> услуги.")


@admin_private_router.message(AddService.time, or_f(F.text, F.text == "."))
async def add_time(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == ".":
        await state.update_data(time=AddService.service_for_change.time)
    else:
        if len(message.text) > 3:
            await message.answer("Время оказания услуги введено некорректно. Введите заново.")
            return
        await state.update_data(time=message.text)
    data = await state.get_data()
    try:
        if AddService.service_for_change:
            await orm_update_service(session, AddService.service_for_change.id, data)
        else:
            await orm_add_service(session, data)
        await message.answer("Услуга добавлена/изменена 👌", reply_markup=admin_kb)
        await state.clear()

    except Exception as e:
        await message.answer(f"ОШИБКА!\n{str(e)}\n"
                             f"Свяжитесь с разработчиком бота!", reply_markup=admin_kb)
        await state.clear()
    # print(data)

    AddService.service_for_change = None


@admin_private_router.message(AddService.time)
async def add_time_second(message: types.Message):
    await message.answer("Упс! Вы ввели не допустимые данные, ведите <b>ВРЕМЯ</b> оказания услуги.")


# Добавление БАРБЕРА (FSM)
@admin_private_router.message(StateFilter(None), F.text == "👨‍🦰 Добавить барбера")
async def add_barber(message: types.Message, state: FSMContext):
    await message.answer(
        "🪧 Введите имя нового барбера:", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddBarber.name)


@admin_private_router.message(AddBarber.name, or_f(F.text, F.text == "."))
async def add_barber_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddBarber.barber_for_change.name)
    else:
        if len(message.text) >= 29:
            await message.answer("Имя барбера не должно превышать 15 символов. \nВведите имя заново.")
            return

        await state.update_data(name=message.text)
    await message.answer("Коротко расскажите клиенту об этом барбере.")
    await state.set_state(AddBarber.description)


@admin_private_router.message(AddBarber.name)
async def add_barber_name_second(message: types.Message):
    await message.answer("Упс! Вы ввели не допустимые данные, ведите <b>ИМЯ</b> барбера.")


# Ловим данные для состояние description и потом меняем состояние на price
@admin_private_router.message(AddBarber.description, or_f(F.text, F.text == "."))
async def add_barber_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=AddBarber.barber_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Добавьте красивое фото барбера.")
    await state.set_state(AddBarber.photo)


# Хендлер для отлова некорректных вводов для состояния description
@admin_private_router.message(AddBarber.description)
async def add_barber_description_second(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст описания заново")


# @admin_private_router.message(AddBarber.earnings, or_f(F.text, F.text == "."))
# async def add_barber_earnings(message: types.Message, state: FSMContext):
#     if message.text == ".":
#         await state.update_data(earnings=AddBarber.barber_for_change.earnings)
#     else:
#         try:
#             float(message.text)
#         except:
#             await message.answer("Введите количество заработанных барбером денег. "
#                                  "Можно проставить 0, если их нет на старте.")
#             return
#         await state.update_data(earniings=message.text)
#     await message.answer("Укажите количество выполненных барбером работ. Если их нет, укажите 0.")
#     await state.set_state(AddBarber.completed_jobs)
#
#
# @admin_private_router.message(AddBarber.earnings)
# async def add_barber_earnings_second(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите зарплату заново.")


# @admin_private_router.message(AddBarber.completed_jobs, or_f(F.text, F.text == "."))
# async def add_barber_completed_jobs(message, state: FSMContext, session: AsyncSession):
#     if message.text == ".":
#         await state.update_data(completed_jobs=AddBarber.barber_for_change.completed_jobs)
#     else:
#         try:
#             int(message.text)
#         except:
#             await message.answer("Количество оказанных барбером услуг введено некорректно. Введите заново.")
#             return
#         await state.update_data(completed_jobs=message.text)
#     await message.answer("ДОбавьте красивую фотографию барбера.")
#     await state.set_state(AddBarber.photo)


# earnings

# Ловим данные для состояния photo и потом выходим из состояний
@admin_private_router.message(AddBarber.photo, or_f(F.photo, F.text == "."))
async def add_photo(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(photo=AddBarber.barber_for_change.photo)

    else:
        await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()

    data['description'] = data.get('description', '')
    # logging.debug(f'DESCRIPTION {data["description"]}')

    data['photo'] = data.get('photo', '')
    # logging.debug(f'PHOTO {data["photo"]}')

    data['earnings'] = data.get('earnings', 0.0)
    data['completed_jobs'] = data.get('completed_jobs', 0)

    try:
        if AddBarber.barber_for_change:
            await orm_update_barber(session, AddBarber.barber_for_change.id, data)
        else:
            await orm_add_barber(session, data)
        await message.answer("Барбер добавлен/изменен", reply_markup=admin_kb)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
            reply_markup=admin_kb,
        )
        await state.clear()

    AddBarber.barber_for_change = None


@admin_private_router.message(AddBarber.photo)
async def add_photo_second(message: types.Message, state: FSMContext):
    await message.answer("Нет, отправьте фото барбера.")


@admin_private_router.message(F.text == "⬅️ Назад")
async def back_to_main_menu(message: types.Message):
    await message.answer(text="Вы вернулись в главное меню.", reply_markup=main_menu_kb)
