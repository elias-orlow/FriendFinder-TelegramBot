from aiogram import types
from aiogram.types.message import ContentTypes
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import StartUserStatesGroup, CreateUserProfileStatesGroup, PeopleSearch
from keyboards import warning_keyboard, cancel_keyboard, yes_keyboard, yes_no_keyboard, start_search_keyboard
from databases import edit_user_id, edit_user_profile


# Sending a warning message
@dp.message_handler(state=StartUserStatesGroup.start)
async def warning_message(message: types.Message) -> None:
    await CreateUserProfileStatesGroup.create_init.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="\U00002757 Remember that on the internet people can impersonate others. \n \n"
                                "\U00002757 The bot does not identify users by any documents. \n \n"
                                "\U00002757 Be careful!",
                           reply_markup=warning_keyboard())


# Cancel button
@dp.message_handler(commands=['cancel'], state='*')
async def break_creating(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await StartUserStatesGroup.start.set()
    await message.reply(text="You stopped creating a profile. Repeat it?",
                        reply_markup=yes_keyboard())


# Asking for user's name
@dp.message_handler(state=CreateUserProfileStatesGroup.create_init)
async def name_request(message: types.Message) -> None:
    await CreateUserProfileStatesGroup.name.set()
    await edit_user_id(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id,
                           reply_markup=cancel_keyboard(),
                           text="What is your name?")


# Asking for user's age and getting user's name
@dp.message_handler(state=CreateUserProfileStatesGroup.name)
async def age_request(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await CreateUserProfileStatesGroup.age.set()
    await bot.send_message(chat_id=message.from_user.id,
                           reply_markup=cancel_keyboard(),
                           text='How old are you?')


# Asking for user's location and getting user's age
@dp.message_handler(state=CreateUserProfileStatesGroup.age)
async def location_request(message: types.Message, state: FSMContext) -> None:
    if not message.text.isnumeric():
        await message.answer(text='It is not an age!')
    else:
        match int(message.text):
            case age if age < 10:
                await message.answer(text='You are not allowed to use my bot! '
                                          'You are too young!')
            case age if age > 130:
                await message.answer(text='Please, be realistic, okay?')
            case _:
                async with state.proxy() as data:
                    data['age'] = message.text

                await CreateUserProfileStatesGroup.city.set()
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Your city?',
                                       reply_markup=cancel_keyboard())


# Asking for user's description and getting user's location
@dp.message_handler(state=CreateUserProfileStatesGroup.city)
async def description_request(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['location'] = message.text

    await CreateUserProfileStatesGroup.description.set()
    await bot.send_message(chat_id=message.from_user.id,
                           reply_markup=cancel_keyboard(),
                           text='Tell more about yourself! '
                                'Who are you looking for? '
                                'What do you want to do?')


# Asking for the user's photo and getting user's description
@dp.message_handler(state=CreateUserProfileStatesGroup.description)
async def photo_request(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
    await CreateUserProfileStatesGroup.photo.set()
    await bot.send_message(chat_id=message.from_user.id,
                           reply_markup=cancel_keyboard(),
                           text='Photo?')


# Photo check
@dp.message_handler(state=CreateUserProfileStatesGroup.photo)
async def photo(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           reply_markup=cancel_keyboard(),
                           text='It is not a photo!')


# Getting user's photo and sending the profile
@dp.message_handler(content_types=ContentTypes.PHOTO, state=CreateUserProfileStatesGroup.photo)
async def profile_create(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=f"{data['name']}, {data['age']}, {data['location']}:\n"
                                     f"{data['description']}")

        await CreateUserProfileStatesGroup.agreement.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Correct? (Yes/No)",
                               reply_markup=yes_no_keyboard())


# TODO: Create people search
@dp.message_handler(state=CreateUserProfileStatesGroup.agreement)
async def people_search(message: types.Message, state: FSMContext) -> None:
    if message.text == "Yes":
        await edit_user_profile(state, user_id=message.from_user.id)
        await PeopleSearch.start.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text='How to interact with bot: \n\n'
                                    '\U00002764 - like profile \n'
                                    '\U0001F48C - send a message to profile \n'
                                    '\U0001F44E - skip \n',
                               reply_markup=start_search_keyboard())
        async with state.proxy() as data:
            data['offset'] = -1

    elif message.text == "No":
        current_state = await state.get_state()
        if current_state is None:
            return
        await CreateUserProfileStatesGroup.create_init.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Ok, let's make it again! Repeat?",
                               reply_markup=yes_keyboard())
