import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp, db, qiwi, bot
from data import NUMBER_QIWI, WEEKDAYS, MODERATORS
from googleapi.googledocs import get_data_time, update_status
from keyboards.admin_kb import refounding_kb
from keyboards.client_kb import send_location_kb, move_between_barbers_kb, barbers_callback, show_services_btn, \
    services_callback, payment_markup, user_kb, update_callback, weeks_kb, week_day_callback, time_callback, time_kb, \
    cancel_kb
from states.user_states import UserStates
from utils.location_calcs import choose_shortest


@dp.message_handler(text='Поиск барберов 🔍', state='*')
async def get_location(message: types.Message):
    await message.answer('Отправьте вашу геолокацию', reply_markup=send_location_kb)


@dp.message_handler(text='Моя запись 📝', state='*')
async def get_user_zapis(message: types.Message):
    user_id = message.from_user.id

    user = db.select_user(user_id)

    if user[7]:

        service = db.get_service(user[7])

        barber = db.get_barber(service[1])

        google_map_url = f'https://maps.google.com/maps?q={barber[5]},{barber[4]}'

        barber_photo = barber[1]

        data = {
            'week_day': WEEKDAYS[user[8]-1],
            'time': user[6],
            'service_name': service[2],
            'service_price': service[3],
            'barber_name': barber[2],
            'barber_phone': barber[3],
            'map': google_map_url
        }

        answer_text = """
Ваша запись:

Барбер: {barber_name}

Номер барбера: {barber_phone}

Услуга: {service_name}

Цена: {service_price}

Локация: <a href='{map}'>🗺 карта</a>
"""

        await message.answer(text=answer_text.format_map(data), disable_web_page_preview=True, parse_mode='HTML',
                             reply_markup=cancel_kb)
    else:
        await message.answer(text='Пока что вы ещё никуда не записаны')


@dp.callback_query_handler(text='cancel')
async def delete_message_show_menu(call: types.CallbackQuery):
    markup = user_kb
    await call.message.delete()
    await call.message.answer('Выберите нужный вам пункт', reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def show_closest_barbers(message: types.Message):
    my_location = message.location
    my_long = my_location.longitude
    my_lat = my_location.latitude
    db.save_location(message.from_user.id, my_long, my_lat)

    barbers = db.get_all_barbers()

    shortest_barbers = choose_shortest(my_lat, my_long, barbers)

    barber = db.get_barber(shortest_barbers[0][0])

    text = f"""
Имя: {barber[2]}
Характеристика: {barber[6]}

Контакт: {barber[3]}
"""

    markup = await move_between_barbers_kb(0)

    await message.answer_photo(caption=text, photo=barber[1], reply_markup=markup)


@dp.callback_query_handler(barbers_callback.filter(action='move'))
async def show_another_barber(call: types.CallbackQuery, callback_data: dict):
    user = db.select_user(call.message.chat.id)
    list_position = callback_data['position']
    barbers = db.get_all_barbers()
    shortest_barbers = choose_shortest(user[5], user[4], barbers)

    barber = db.get_barber(shortest_barbers[int(list_position)][0])

    text = f"""
Имя: {barber[2]}
Характеристика: {barber[6]}
Расстояние: {shortest_barbers[int(list_position)][1]} km

Контакт: {barber[3]}
"""

    markup = await move_between_barbers_kb(int(list_position))
    await call.message.delete()
    await call.message.answer_photo(caption=text, photo=barber[1], reply_markup=markup)


@dp.callback_query_handler(barbers_callback.filter(action='select'))
async def show_another_barber(call: types.CallbackQuery, callback_data: dict):
    user = db.select_user(call.message.chat.id)
    list_position = callback_data['position']
    barbers = db.get_all_barbers()
    shortest_barbers = choose_shortest(user[5], user[4], barbers)

    barber = db.get_barber(shortest_barbers[int(list_position)][0])

    services = db.get_all_services(barber[0])

    answer_text = 'Выберите услугу:\n\n'

    try:
        for index, service in enumerate(services):
            answer_text += f'{index + 1}. {service[2]} - {service[3]} rub \n\n'
    except:
        services = None

    markup = await show_services_btn(list_position, services)

    await call.message.edit_caption(caption=answer_text, reply_markup=markup)


@dp.callback_query_handler(services_callback.filter())
async def show_week_days(call: types.CallbackQuery, callback_data: dict):
    # Изменяем текст сообшение
    text = call.message.caption
    await call.message.edit_caption(caption=text + '\n\nИдет поиск свободного времени барбера(подождите) 🔍')
    service_id = callback_data['service_id']
    service = db.get_service(service_id)
    barber = db.get_barber(service[1])

    # Берем все записи барбера из гугл таблиц
    data = await get_data_time(barber[7])

    weekday_index = datetime.datetime.today().isoweekday()

    free_days = data[weekday_index:]

    # Создаем Inline клаву с дней недели
    markup = await weeks_kb(free_days, weekday_index, service_id)

    await call.message.edit_caption(caption='Выберите ваш свободный день💇🏻‍♂', reply_markup=markup)


@dp.callback_query_handler(week_day_callback.filter())
async def show_free_time(call: types.CallbackQuery, callback_data: dict):
    # Изменяем текст сообшение
    text = call.message.caption
    await call.message.edit_caption(caption=text + '\n\nИдет поиск свободного времени барбера(подождите) 🔍')
    service_id = callback_data['service_id']
    weekday_index = callback_data['day']
    service = db.get_service(service_id)
    barber = db.get_barber(service[1])
    # Берем все записи барбера из гугл таблиц
    data = await get_data_time(barber[7])

    free_times = data[int(weekday_index)]

    # Создаем Inline клаву с свободный временами
    markup = await time_kb(data[0], free_times, weekday_index, service_id)

    await call.message.edit_caption(caption='Выберите ваш свободный день💇🏻‍♂', reply_markup=markup)


@dp.callback_query_handler(time_callback.filter())
async def show_service_details(call: types.CallbackQuery, callback_data: dict):
    # Изменяем текст сообшение
    text = call.message.caption
    await call.message.edit_caption(caption=text + '\n\nИдет поиск свободного времени барбера(подождите) 🔍')
    service_id = callback_data['service_id']
    weekday_index = int(callback_data['weekday_index']) + 1
    time = callback_data['time']
    service = db.get_service(service_id)
    barber = db.get_barber(service[1])

    service_price = service[3]

    bill_url = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={NUMBER_QIWI[1:]}&amountInteger={int(service_price)}&amountFraction=0&extra%5B%27comment%27%5D={call.message.chat.id}&currency=643"

    markup = await payment_markup(bill_url, service_id, weekday_index, time)

    answer_text = f"""
Барбер: {barber[2]}
Услуга: {service[2]}
Стоимость: {service[3]}

Записали вас в {WEEKDAYS[weekday_index - 1]} в {time} 
"""

    await call.message.edit_caption(caption=answer_text, reply_markup=markup)


@dp.callback_query_handler(update_callback.filter())
async def check_payment(call: types.CallbackQuery, callback_data: dict):
    service_id = callback_data['service']
    weekday_index = int(callback_data['weekday_index'])
    time = callback_data['time']
    service = db.get_service(service_id)
    barber = db.get_barber(service[1])
    url = barber[7]
    qiwi.start()
    payments = qiwi.payments
    for payment in payments['data']:
        print(payment['date'])
        date = str(datetime.datetime.now().isoformat()).split('T')[0]
        print(date)
        if payment['comment'] == str(call.message.chat.id) and payment['date'].split('T')[0] == date:
            db.update_user(call.message.chat.id, service_id, weekday_index, time)
            await update_status(url, time, weekday_index, call.message.chat.id)
            await call.message.edit_reply_markup()
            await call.message.answer('Запись прошла успешно !!', reply_markup=user_kb)
            return

    await call.message.answer('Платеж не удался.')


# Логика возврата средства

@dp.callback_query_handler(text='cancel_zapis')
async def refounding(call: types.CallbackQuery):
    await call.message.answer('Отправьте ваш номер телефона🤳🏼, который привязан к кошельку Qiwi.\nПример: +79123456789')
    await UserStates.phone_number.set()


@dp.message_handler(state=UserStates.phone_number)
async def getting_number(message: types.Message):
    phone = message.text

    if phone[0] == '+' and len(phone) == 12:
        await message.answer('Отправьте причину отказа😰 \n(Сообщение автоматически отправится после ввода причины): ')
        await UserStates.reason.set()
        db.update_number(message.from_user.id, phone)
    else:
        await message.answer('Отправьте ваш номер телефона как в примере💁🏻 +79123456789 📞')


@dp.message_handler(state=UserStates.reason)
async def refound_req_admin(message: types.Message, state: FSMContext):
    reason = message.text
    username = message.from_user.username
    name = message.from_user.first_name
    user_id = message.from_user.id

    user = db.select_user(user_id)
    service = db.get_service(user[7])
    barber = db.get_barber(service[1])
    admin_text = """
Клиент: <a href="https://t.me/{username}">{name}</a>

Услуга: {service_name}
Цена: {service_price}

Барбер: {barber_name}

Причина отказа:
{reason}
"""

    data = {
        'service_name': service[2],
        'service_price': service[3],
        'barber_name': barber[2],
        'reason': reason,
        'username': username,
        'name': name,
    }

    admin_markup = await refounding_kb(user_id)

    await bot.send_message(chat_id=MODERATORS[0], text=admin_text.format_map(data), disable_web_page_preview=True,
                           parse_mode="HTML", reply_markup=admin_markup)

    await message.answer('Сообщение отправлено на рассмотрение. Обработка заявки займет максимум 24 ч.')
    await state.finish()
