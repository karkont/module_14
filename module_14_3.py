from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.dispatcher import FSMContext
import asyncio

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


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
kb.row(btn0, btn1)
kb.add(btn2)

inl_kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
inl_kb_button1 = KeyboardButton(text='Product1', callback_data="product_buying")
inl_kb_button2 = KeyboardButton(text='Product2', callback_data="product_buying")
inl_kb_button3 = KeyboardButton(text='Product3', callback_data="product_buying")
inl_kb_button4 = KeyboardButton(text='Product4', callback_data="product_buying")
inl_kb.add(inl_kb_button1, inl_kb_button2 ,inl_kb_button3 ,inl_kb_button4)

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    await message.answer(f'Название: Product1 | Описание: описание 1 | Цена: 100')
    with open('imgs/1.png', 'rb') as img:
        await message.answer_photo(img)

    await message.answer(f'Название: Product2 | Описание: описание 2 | Цена: 200')
    with open('imgs/2.jpg', 'rb') as img:
        await message.answer_photo(img)

    await message.answer(f'Название: Product3 | Описание: описание 3 | Цена: 300')
    with open('imgs/3.png', 'rb') as img:
        await message.answer_photo(img)

    await message.answer(f'Название: Product4 | Описание: описание 4 | Цена: 400')
    with open('imgs/4.jpg', 'rb') as img:
        await message.answer_photo(img, 'Выберите продукт для покупки:', reply_markup=inl_kb)



@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('10 * weight + 6.25 * growth - 5 * age + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def urb_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваше количество калорий для поддержания веса: {calories}')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)