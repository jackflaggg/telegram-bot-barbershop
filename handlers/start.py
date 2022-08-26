from aiogram import types

from create_bot import dp, db
from data import MODERATORS
from keyboards.admin_kb import moderator_kb
from keyboards.client_kb import user_kb

@dp.message_handler(commands='start')
async def show_mainmenu(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name

    try:
        db.add_user(user_id, username, name)
    except:
        pass
    if message.from_user.id in MODERATORS:
        markup = moderator_kb
    else:
        markup = user_kb

    await message.answer('Выберите нужный вам пункт', reply_markup=markup)
