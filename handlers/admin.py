from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp, db, qiwi, bot
from googleapi.googledocs import remove_from_table
from keyboards.admin_kb import refound_callback
from states.moderator_states import ModeratorStates


@dp.message_handler(text='Добавить барбера ➕', state='*')
async def create_barber(message: types.Message):
    await message.answer('Отправьте имя барбера')
    await ModeratorStates.get_name.set()


@dp.message_handler(text='Удалить барбера ➖', state='*')
async def create_barber(message: types.Message):
    # берем лист барберов из базы
    barbers = db.get_all_barbers()

    answer_text = 'Лист барберов с их ид\n\n'

    for index, barber in enumerate(barbers):
        answer_text += f'{index+1}.  {barber[2]} - id: {barber[0]} \n'

    answer_text += f'\nВведите ид барбера для удаления'

    await message.answer(answer_text)
    await ModeratorStates.get_barber_id.set()


@dp.message_handler(state=ModeratorStates.get_name, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer('Отправьте контактный номер телефона барбера')
    await ModeratorStates.get_phone.set()
    await state.update_data(name=name)


@dp.message_handler(state=ModeratorStates.get_phone, content_types=types.ContentType.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await message.answer('Отправьте ссылку на google-таблицу барбера с записями:')
    await ModeratorStates.get_url.set()
    await state.update_data(phone=phone)


@dp.message_handler(state=ModeratorStates.get_url, content_types=types.ContentType.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    url = message.text
    await message.answer('Отправьте характеристику барбера')
    await ModeratorStates.get_opisaniya.set()
    await state.update_data(url=url)


@dp.message_handler(state=ModeratorStates.get_opisaniya, content_types=types.ContentType.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    opisaniya = message.text
    await message.answer('Отправьте фото барбера')
    await ModeratorStates.get_photo.set()
    await state.update_data(opisaniya=opisaniya)


@dp.message_handler(state=ModeratorStates.get_photo, content_types=types.ContentType.PHOTO)
async def get_phone(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await message.answer('Отправьте локацию барбера')
    await ModeratorStates.get_location.set()
    await state.update_data(photo_id=photo_id)


@dp.message_handler(state=ModeratorStates.get_location, content_types=types.ContentType.LOCATION)
async def get_phone(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')
    opisaniya = data.get('opisaniya')
    photo_id = data.get('photo_id')

    db.add_barber(photo_id, name, phone, longitude, latitude, opisaniya)

    await message.answer('барбер успешно добавлен')

    await state.finish()


# Сенария удаления барберов
@dp.message_handler(state=ModeratorStates.get_barber_id)
async def get_phone(message: types.Message, state: FSMContext):
    try:
        barber_id = int(message.text)

        try:
            db.delete_barber(barber_id)
            await message.answer('Барбер успешно удален!')
            await state.finish()
        except Exception as e:
            print(e)

    except:
        await message.answer('Вы ввели некорректную цифру. Попробуйте ещё раз!')


@dp.callback_query_handler(refound_callback.filter(action='accept'))
async def accept_refound(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data['user']
    user = db.select_user(user_id)
    service = db.get_service(user[7])
    barber = db.get_barber(service[1])
    try:
        paying = qiwi.pay(user[3], amount=service[3], comment='Возврат средств')
    except Exception as e:
        return await call.message.answer(f'Ошибка при возврате, причина: `{e}`')
    await remove_from_table(barber[7], user_id)
    await bot.send_message(chat_id=user_id, text='Возврат средств одобрен ✅')
    db.reset_user_zapis(user_id)

    text = call.message.text + '\n\nОдобрено ✅'
    await call.message.edit_text(text=text, reply_markup=None)


@dp.callback_query_handler(refound_callback.filter(action='ignore'))
async def ignoredrefound(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data['user']
    await state.update_data(user_id=user_id)
    await call.message.answer('Отправьте причину отказа :')
    await ModeratorStates.reason.set()
    await call.message.edit_reply_markup()


@dp.message_handler(state=ModeratorStates.reason)
async def send_to_user(message: types.Message, state:FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    reason = 'Заявка отклонена ❌\nПричина: {}'.format(message.text)

    await bot.send_message(chat_id=user_id, text=reason)
    await message.answer('Сообщение отправлено!')
    await state.finish()
