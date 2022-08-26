from aiogram.dispatcher.filters.state import StatesGroup, State


class ModeratorStates(StatesGroup):
    get_name = State()
    get_phone = State()
    get_location = State()
    get_opisaniya = State()
    get_photo = State()
    get_barber_id = State()
    get_barber_id_service = State()
    service_description = State()
    service_price = State()
    barber_id = State()
    service_id = State()
    get_url = State()
    text = State()
    next_stage = State()
    get_img = State()
    get_video = State()
    finishpost = State()
    publish = State()
    reason = State()
