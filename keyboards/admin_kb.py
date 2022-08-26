from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки клавиатуры админа
from aiogram.utils.callback_data import CallbackData

button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load) \
    .add(button_delete)

moderator_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Добавить барбера ➕'),
            KeyboardButton(text='Удалить барбера ➖'),
        ],
        [
            KeyboardButton(text='Добавить услугу ➕'),
            KeyboardButton(text='Удалить услугу ➖'),
        ],
        [
            KeyboardButton(text='Поиск барберов 🔍'),
            KeyboardButton(text='Моя запись 📝'),
        ]
    ]
)

refound_callback = CallbackData('refound', 'user', 'action')


async def refounding_kb(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить",
                                     callback_data=refound_callback.new(user=user_id, action='accept')),
                InlineKeyboardButton(text="Отменить",
                                     callback_data=refound_callback.new(user=user_id, action='ignore')),
            ]
        ]
    )

    return markup
