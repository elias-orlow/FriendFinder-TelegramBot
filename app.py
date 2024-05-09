from aiogram import executor

from databases import create_db
from utils import set_default_commands, on_startup_notify, on_shutdown_notify
from loader import dp
import handlers


async def on_startup(dispatcher) -> None:
    await create_db()
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher):
    await on_shutdown_notify(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
