from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет")],
   [KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://ria.ru')],
   [InlineKeyboardButton(text="Музыка", url='https://www.youtube.com')],
   [InlineKeyboardButton(text="Видео", url='https://www.youtube.com')]
])

inline_keyboard_test1 = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='t1')]
])

inline_keyboard_test2 = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Опция 1", callback_data='t2')],
   [InlineKeyboardButton(text="Опция 2", callback_data='t3')]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=HfaIcB4Ogxk'))
   return keyboard.adjust(2).as_markup()