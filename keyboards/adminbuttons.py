from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

adminpanelmenu = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='С фото 🏞'),
            KeyboardButton(text='С видео 🎥')
        ],
        [
            KeyboardButton(text="Пропустить ➡️")
        ]
    ]
)

adminpanelcontinue = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='продолжить ➡️')
        ]
    ]
)

startposting = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить☀️', callback_data='startposting'),
            InlineKeyboardButton(text='Отменить❄️', callback_data='cancelposting')
        ]
    ]
)
