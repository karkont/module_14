from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
import crud_functions
from aiogram.dispatcher import FSMContext
import asyncio

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
kb1_button = KeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb1_button1 = KeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.row(kb1_button, kb1_button1)

kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn0 = KeyboardButton(text='Рассчитать')
btn1 = KeyboardButton(text='Информация')
btn2 = KeyboardButton(text='Купить')
btn3 = KeyboardButton(text='Регистрация')
kb.add(btn3)
kb.row(btn0, btn1, btn2)


inl_kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
inl_kb_button1 = KeyboardButton(text='Product1', callback_data="product_buying")
inl_kb_button2 = KeyboardButton(text='Product2', callback_data="product_buying")
inl_kb_button3 = KeyboardButton(text='Product3', callback_data="product_buying")
inl_kb_button4 = KeyboardButton(text='Product4', callback_data="product_buying")
inl_kb.add(inl_kb_button1, inl_kb_button2 ,inl_kb_button3 ,inl_kb_button4)

@dp.message_handler(commands=['start'])
async def urb_message(message):
    crud_functions.initiate_db()
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой возраст:')
    data = await state.get_data()
    add_user(data['username'], data['email'], message.text)
    await state.finish()
    await message.reply("Регистрация завершена!")


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    products = crud_functions.get_all_products()
    for i in products:
        product_id, title, description, price = i
        with open(f'imgs/{product_id}.png', 'rb') as img:
            await message.answer_photo(img)
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
    await message.answer('Выберите продукт для покупки:', reply_markup=inl_kb)


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)