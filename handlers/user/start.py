from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.states import StartUserStatesGroup
from keyboards.user import start_keyboard


@dp.message_handler(commands=['start'], state='*')
async def cmd_start_user(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await StartUserStatesGroup.start.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Welcome! \U00002600 \n"
                                "It is difficult to find friends today... \n"
                                "I'll help you with it! \U0001F46B",
                           reply_markup=start_keyboard())
