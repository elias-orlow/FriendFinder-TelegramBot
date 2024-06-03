from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import PeopleSearch
from databases import get_user
from keyboards import rate_keyboard, again_keyboard


@dp.message_handler(lambda message: message.text == '👎', state=PeopleSearch.search)
@dp.message_handler(state=PeopleSearch.start)
async def start_searching(message: types.Message, state: FSMContext) -> None:
    await PeopleSearch.search.set()
    async with state.proxy() as data:
        data['offset'] += 1

        user = await get_user(offset=data['offset'])
        if len(user) != 0 and message.from_user.id == int(user[0][0]):
            data['offset'] += 1
            user = await get_user(offset=data['offset'])

    if len(user) != 0:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=user[0][5],
                             caption=f"{user[0][1]}, {user[0][2]}, {user[0][3]}:\n"
                                     f"{user[0][4]}",
                             reply_markup=rate_keyboard())
    else:
        async with state.proxy() as data:
            data['offset'] -= 1

        await PeopleSearch.start.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Unfortunately, there are no more people to search for \U0001F614\n'
                                    'Come back later and we will definitely find you friends!',
                               reply_markup=again_keyboard())


@dp.message_handler(state=PeopleSearch.search)
async def people_search(message: types.Message) -> None:
    if message.text == '❤️':
        await bot.send_message(chat_id=message.from_user.id,
                               text='You liked profile!')
    elif message.text == '💌':
        await bot.send_message(chat_id=message.from_user.id,
                               text='You want to send a message!')
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='I can not understand you...')
