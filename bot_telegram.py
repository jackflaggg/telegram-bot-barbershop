from aiogram.utils import executor
from create_bot import dp, db



from handlers import client_menu
from handlers import admin
from handlers import start
from handlers import client
from handlers import rassilka
from handlers import manage_services


async def on_startup(_):
    print('Я вышел в сеть, хозяин!')
    # Создаем базу если ещё не создана
    try:
        db.create_table_clients()
        db.create_table_barbers()
        db.create_table_uslugi()
    except:
        pass


executor.start_polling(dp, on_startup=on_startup)
