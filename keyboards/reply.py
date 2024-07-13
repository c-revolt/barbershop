from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎟 Абонементы"),
        ],
        [
            KeyboardButton(text="💈 Услуги"),
            KeyboardButton(text="✂️ Барберы")
        ],
        [
            KeyboardButton(text="🪪 Личный кабинет"),
        ],
[
            KeyboardButton(text="📲 Контакты"),
            KeyboardButton(text="🔒 Privacy"),
        ],
        [
            KeyboardButton(text="🌟 Отзывы"),
        ],
[
            KeyboardButton(text="Разработчик(только в демо боте)"),
        ],

    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎟 Абонементы"),
            KeyboardButton(text="Услуги"),
        ],
        [

            KeyboardButton(text="➕ Добавить услугу")
        ],
[
            KeyboardButton(text="👨‍🦰 Добавить барбера")
        ],
        [
            KeyboardButton(text="🖌 Изменить услугу")
        ],
        [
            KeyboardButton(text="📑 Заявки"),
            KeyboardButton(text="📊 Статистика")
        ],
        [
            KeyboardButton(text="🌟 Отзывы"),
        ],

    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

del_kbd = ReplyKeyboardRemove()

