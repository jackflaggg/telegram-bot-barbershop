from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from create_bot import dp, bot, db
from keyboards.adminbuttons import adminpanelcontinue, startposting, adminpanelmenu
from states.moderator_states import ModeratorStates


@dp.message_handler(Command('rassilka'))
async def show_rassilka(message: types.Message):
    await message.answer('Введите текст поста:', reply_markup=ReplyKeyboardRemove())
    await ModeratorStates.text.set()


@dp.message_handler(state=ModeratorStates.text)
async def get_posttext(message: types.Message, state: FSMContext):
    textpost = message.text

    await state.update_data(textpost=textpost)
    await message.answer('Выберите то, что вам нужно :', reply_markup=adminpanelmenu)
    await ModeratorStates.next_stage.set()


@dp.message_handler(state=ModeratorStates.next_stage, text='С фото 🏞')
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer('Отправьте фото 🏞 :')
    await ModeratorStates.get_img.set()


@dp.message_handler(state=ModeratorStates.get_img, content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message, state: FSMContext):
    fileid = message.photo[0].file_id
    await state.update_data(photoid=fileid)
    await ModeratorStates.finishpost.set()
    await message.answer('✅ Данные получены нажмите - продолжить', reply_markup=adminpanelcontinue)


@dp.message_handler(state=ModeratorStates.next_stage, text='С видео 🎥')
async def get_video(message: types.Message, state: FSMContext):
    await message.answer('Отправьте видео 🎥 :')
    await ModeratorStates.get_video.set()


@dp.message_handler(state=ModeratorStates.get_video, content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message, state: FSMContext):
    fileid = message.video.file_id
    await state.update_data(videoid=fileid)
    await ModeratorStates.finishpost.set()
    await message.answer('✅ Данные получены нажмите - продолжить', reply_markup=adminpanelcontinue)


@dp.message_handler(state=ModeratorStates.next_stage, text='Пропустить ➡️')
@dp.message_handler(state=ModeratorStates.finishpost)
async def get_testpost(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_text = data.get('textpost')
    photoid = data.get('photoid')
    videoid = data.get('videoid')
    user = message.from_user.id
    try:
        if photoid:
            await bot.send_photo(user, photo=photoid, caption=post_text,
                                 parse_mode='HTML', reply_markup=startposting)
        elif videoid:
            await bot.send_video(user, video=videoid, caption=post_text,
                                 parse_mode='HTML', reply_markup=startposting)
        else:
            await bot.send_message(user, disable_web_page_preview=True, text=post_text, parse_mode='HTML',
                                   reply_markup=startposting)
        await ModeratorStates.publish.set()
    except Exception as e:
        print(e)
        await bot.send_message(user,
                               text=f'Введенный текст не правильно форматирован! Убедитесь, что все теги закрыты.\n Начните всё заного : /rassilka')
        await state.finish()
        await state.reset_data()


@dp.callback_query_handler(state=ModeratorStates.publish, text='startposting')
async def sendposts(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_text = data.get('textpost')
    photoid = data.get('photoid')
    videoid = data.get('videoid')
    senpostcol = 0
    users = db.get_all_users()
    user_ids = []
    for user in users:
        user_ids.append(user[0])

    for user in set(user_ids):
        try:
            if photoid:
                await bot.send_photo(user, photo=photoid, caption=post_text,
                                     parse_mode='HTML')
            elif videoid:
                await bot.send_video(user, video=videoid, caption=post_text,
                                     parse_mode='HTML')
            else:
                await bot.send_message(chat_id=user, disable_web_page_preview=True, text=post_text, parse_mode='HTML')
            senpostcol += 1
        except Exception as e:
            print(e)
    await call.message.answer(f'✅ Пост успешно отправлен {senpostcol} пользователям \n',
                              reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(state=ModeratorStates.publish, text='cancelposting')
async def cancel_post(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'✅ Данные удалены.\n Начните всё заново : /rassilka', reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await state.reset_data()
