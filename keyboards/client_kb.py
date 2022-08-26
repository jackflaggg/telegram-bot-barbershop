from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Создаем клавиатуру для пользователей
user_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Поиск барберов 🔍'),
            KeyboardButton(text='Моя запись 📝'),
        ],
        [
            KeyboardButton(text='О нас🧐'),
            KeyboardButton(text='Наши услуги💅🏼'),
        ],
        [
            KeyboardButton(text='Местоположение🌍'),
            KeyboardButton(text='Контакты☎'),
        ]
    ]
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вернуть средства", callback_data='cancel_zapis')
        ]
    ]
)

# Кнопка для отправьки локацию
send_location_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton('Моя локация 📍', request_location=True)
        ]
    ]
)

barbers_callback = CallbackData('barber', 'position', 'action')
services_callback = CallbackData('service', 'service_id')
update_callback = CallbackData('update', 'service', 'weekday_index', 'time')


# Инлайн Кнопки для перемещения между барберов
async def move_between_barbers_kb(current_barber_id):
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='<== Пред.',
                                     callback_data=barbers_callback.new(position=current_barber_id - 1, action='move')),
                InlineKeyboardButton(text='Выбрать',
                                     callback_data=barbers_callback.new(position=current_barber_id, action='select')),
                InlineKeyboardButton(text='След. ==>',
                                     callback_data=barbers_callback.new(position=current_barber_id + 1, action='move')),
            ]
        ]
    )


# Инлайн Кнопки для перемещения между барберов
async def show_services_btn(current_barber_id, services):
    markup = InlineKeyboardMarkup(
        row_width=3
    )

    if services:
        for index, service in enumerate(services):
            markup.insert(
                InlineKeyboardButton(text=f'{index + 1}', callback_data=services_callback.new(service_id=service[0])))

    markup.add(InlineKeyboardButton(text='Назад',
                                    callback_data=barbers_callback.new(position=current_barber_id, action='move')))

    return markup


# Инлайн Кнопки для перемещения между барберов
async def payment_markup(url, service, weekday_index, time):
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Оплатить', url=url)
            ],
            [
                InlineKeyboardButton(text='Проверить', callback_data=update_callback.new(
                    weekday_index=weekday_index,
                    time=time,
                    service=service
                ))
            ],
            [
                InlineKeyboardButton(text='Отменить', callback_data='cancel')
            ]
        ]
    )
    return markup


week_day_callback = CallbackData('weekday', 'day', 'service_id')
time_callback = CallbackData('clock', 'time', 'weekday_index', 'service_id')


# Инлайн Кнопки для оставшый дней недели
async def weeks_kb(data, weekday_index, service_id):
    markup = InlineKeyboardMarkup(
        row_width=2,
    )

    for i, days in enumerate(data):
        markup.insert(InlineKeyboardButton(text=days[0], callback_data=week_day_callback.new(day=weekday_index + i,
                                                                                             service_id=service_id)))

    return markup


# Инлайн Кнопки свободных времи
async def time_kb(time, data, weekday_index, service_id):
    markup = InlineKeyboardMarkup(
        row_width=2,
    )

    for i, zapis in enumerate(data):
        if zapis == '':
            markup.insert(
                InlineKeyboardButton(text=time[i], callback_data=time_callback.new(time=time[i].replace(':', '.'),
                                                                                   weekday_index=weekday_index,
                                                                                   service_id=service_id)))

    return markup
