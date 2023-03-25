import os
import django
from aiogram import Bot, Dispatcher
import logging
# from send_keyboard import customer


async def on_startup(dp):
    from utils.set_bot_commands import set_default_commands
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "core.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    # customer()
