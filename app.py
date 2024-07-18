import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, sesstion_maker

from middleware.db import DataBaseSession

from handlers.user_private import user_private_router
from handlers.admin_private import admin_private_router
from handlers.user_group import user_group_router
from common.cmds_list import private

bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = [5720448139,]

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_private_router)


async def on_startup(bot):
    await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=sesstion_maker))

    await bot.delete_webhook()
    await bot.set_my_commands(commands=private)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
