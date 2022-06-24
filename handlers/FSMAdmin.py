import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot


class FSMAdmin(StatesGroup):
    photo = State()
    NameOfTheDish = State()
    DescriptionOfTheDish = State()
    ThePriceOfTheDish = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await message.answer(f"здравствуйте {message.from_user.full_name},\n"
                             f"скиньте фото Блюдо")
        await FSMAdmin.photo.set()
    else:
        await message.reply("Пишите в Личку!")


async def load_photo(message: types.Message, state: FSMContext):
    print(message.photo)
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await message.answer("название Блюдо:")
    await FSMAdmin.next()



async def load_Title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Title"] = message.text
        print(data)
    await FSMAdmin.next()
    await message.answer("описание Блюдо:")


async def load_Description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Description"] = message.text
        print(data)
    await FSMAdmin.next()
    await message.answer("Стоимость Блюдо:")


async def load_Price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["Price"] = int(message.text)
            print(data)
    except:
        await message.answer("пишите числами!!")




    await state.finish()
    await bot.send_photo(
        message.from_user.id,
        data["photo"],
        caption=f"""Title: {data['Title']}
        Description: {data['Description']}
        Price: {data['Price']}""",
    )


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(id INTEGER PRIMARY KEY, Title TEXT,"
               "photo TEXT,Description TEXT,Price INTEGER,"
               "region TEXT)")
    db.commit()


def register_handler_fsm_dish(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["menu"])
    dp.register_message_handler(
        load_photo, state=FSMAdmin.photo, content_types=["photo"]
    )
    dp.register_message_handler(load_Title, state=FSMAdmin.NameOfTheDish)
    dp.register_message_handler(load_Description, state=FSMAdmin.DescriptionOfTheDish)
    dp.register_message_handler(load_Price, state=FSMAdmin.ThePriceOfTheDish)
