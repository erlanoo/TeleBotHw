import asyncio

from aiogram.utils import executor
from config import dp
from handlers import client, callback, admin, FSMAdmin, extra, notifiation
import logging
from handlers.FSMAdmin import sql_create
async def on_startup(_):
    asyncio.create_task(notifiation.scheduler())
    sql_create()


notifiation.register_handler_notifiation(dp)
FSMAdmin.register_handler_fsm_dish(dp)
client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
admin.register_hundler_admin(dp)
extra.register_handlers_extra(dp)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)
