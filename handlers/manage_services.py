from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import dp, db
from states.moderator_states import ModeratorStates


@dp.message_handler(text='Добавить услугу ➕')
async def show_barbers(message: types.Message):
    # берем лист барберов из базы
    barbers = db.get_all_barbers()

    answer_text = 'Лист барберов с их ид\n\n'

    for index, barber in enumerate(barbers):
        answer_text += f'{index + 1}.  {barber[2]} - id: {barber[0]} \n'

    answer_text += f'\nВведите ид барбера для добавление услугу'

    await message.answer(answer_text)
    await ModeratorStates.get_barber_id_service.set()


@dp.message_handler(state=ModeratorStates.get_barber_id_service, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    try:
        barber_id = int(message.text)

        await state.update_data(barber=barber_id)
        await message.answer('Введите описания услуги')
        await ModeratorStates.service_description.set()

    except:
        await message.answer('Вы ввели некорректную цифру')


@dp.message_handler(state=ModeratorStates.service_description, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer('Введите цену для услуг.')
    await ModeratorStates.service_price.set()


@dp.message_handler(state=ModeratorStates.service_price, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        data = await state.get_data()
        owner = data.get('barber')
        description = data.get('description')

        db.add_service(owner, description, price)

        await message.answer('Услуга добавлено успешно')
        await state.finish()

    except Exception as e:
        print(e)
        await message.answer('Вы ввели некорректную сумму !\n Отправьте ещё раз:')


@dp.message_handler(text='Удалить услугу ➖')
async def show_barbers(message: types.Message):
    # берем лист барберов из базы
    barbers = db.get_all_barbers()

    answer_text = 'Лист барберов с их ид\n\n'

    for index, barber in enumerate(barbers):
        answer_text += f'{index + 1}.  {barber[2]} - id: {barber[0]} \n'

    answer_text += f'\nВведите ид барбера для удаление его услуг'

    await message.answer(answer_text)
    await ModeratorStates.barber_id.set()


@dp.message_handler(state=ModeratorStates.barber_id, content_types=types.ContentType.TEXT)
async def show_services(message: types.Message, state: FSMContext):
    try:
        barber = db.get_barber(int(message.text))
        services = db.get_all_services(barber[0])

        answer_text = f'Ид услуг:\n\n'
        for index, service in enumerate(services):
            answer_text += f'{index + 1}. {service[2]} id : {service[0]}\n'

        await message.answer(answer_text)
        await ModeratorStates.service_id.set()

    except:
        await message.answer('Данный ид не существует!')


@dp.message_handler(state=ModeratorStates.service_id, content_types=types.ContentType.TEXT)
async def show_services(message: types.Message, state: FSMContext):
    try:
        db.delete_service(int(message.text))
        await message.answer('Сервис удален!')
        await state.finish()
    except:
        await message.answer('Ошибка!')
