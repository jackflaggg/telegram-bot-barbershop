from aiogram import types

from create_bot import dp


@dp.message_handler(text='О нас🧐', state='*')
async def get_location(message: types.Message):
    text = "Gentleman’s Barbershop - это больше, чем просто мужская парикмахерская. Мы возрождаем традиции настоящего классического барбершопа. Здесь вы не увидите мужчин, стригущих женщин и женщин, стригущих мужчин! Идеальные стрижки, бритьё, оформление бороды, бодрящий кофе, крепкий виски и душевные откровенные разговоры под звуки классического джаза и рока - это атмосфера настоящих Джентльменов!"
    await message.answer(text)


@dp.message_handler(text='Наши услуги💅🏼', state='*')
async def get_location(message: types.Message):
    text = """В хорошем мужском салоне выполняют:
- мужскую стрижку и коррекцию прически;
- укладку;
- маскировку седины, окраску;
- стрижку и укладку усов и бороды;
- моделирование усов и бороды;
- королевское бритье;
- уход за волосами, бородой, усами, кожей лица.
"""

    await message.answer(text)


@dp.message_handler(text='Местоположение🌍', state='*')
async def get_location(message: types.Message):
    text = "Мы находимся по адресу: г. Стерлитамак, ул. Худайбердина, д. 27 Gentleman Barbershop"

    await message.answer(text)


@dp.message_handler(text='Контакты☎', state='*')
async def get_location(message: types.Message):
    text = "Мы работаем с пн-вс 11:00–20:00. Звоните по номеру: +7 (986) 700-40-40. Пишите в группу: https://vk.com/gentlemans_barbershop_str по всем интересующим вам вопросам"

    await message.answer(text)
