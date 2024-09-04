from aiogram.fsm.context import FSMContext

from config import TOKEN, APIKEY, JAKEY
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import keyboard as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

@dp.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/Weather")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какой ты группы?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state:FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()
    await message.answer("Данные добавлены в БД")
    await state.clear()

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer(text='_________', reply_markup=kb.main)

@dp.message(F.text == "Привет")
async def test_button(message: Message):
   await message.answer(f'Привет, {message.from_user.first_name}!')
@dp.message(F.text == "Пока")
async def test_button(message: Message):
   await message.answer(f'До свидания, {message.from_user.first_name}!')

@dp.message(Command('links'))
async def help(message: Message, state: FSMContext):
    await message.answer('Ссылочки:', reply_markup=kb.inline_keyboard_test)

@dp.message(Command('dynamic'))
async def help(message: Message, state: FSMContext):
    await message.answer('=====================:', reply_markup=kb.inline_keyboard_test1)

@dp.callback_query(F.data == 't1')
async def news(callback: CallbackQuery):
   await callback.answer("Новости подгружаются", show_alert=True)
   await callback.message.edit_text('=====================:', reply_markup=kb.inline_keyboard_test2)

@dp.callback_query(F.data == 't2')
async def news1(callback: CallbackQuery):
    await callback.message.answer("Выбрана опция 1")
@dp.callback_query(F.data == 't3')
async def news2(callback: CallbackQuery):
    await callback.message.answer("Выбрана опция 2")

async def main():
    await dp.start_polling(bot)


@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

if __name__ == "__main__":
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT);''')

    conn.commit()
    conn.close()
    asyncio.run(main())


    # { % if weather %}
    # < h3 > Погода
    # в
    # {{weather['name']}} < / h3 >
    # < p > Температура: {{weather['main']['temp']}}°C < / p >
    # < p > Погода: {{weather['weather'][0]['description']}} < / p >
