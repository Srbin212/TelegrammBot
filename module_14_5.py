from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from crud_functions2 import *
prod = get_all_products()

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup()
button = KeyboardButton(text='Регистрация')
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.row(button1, button2)
kb.add(button3)

bt_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ], resize_keyboard=True
)

bt_menu1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ], resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=bt_menu)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open('img_fruit/img1.jpg', "rb") as img:
        await message.answer_photo(img, f"Название: {prod[0][1]} | Описание: {prod[0][2]} | Цена: {prod[0][3]} ")
    with open('img_fruit/img2.jpg', "rb") as img:
        await message.answer_photo(img, f"Название: {prod[1][1]} | Описание: {prod[1][2]} | Цена: {prod[1][3]}")
    with open('img_fruit/img3.jpg', "rb") as img:
        await message.answer_photo(img, f"Название: {prod[2][1]} | Описание: {prod[2][2]} | Цена: {prod[2][3]}")
    with open('img_fruit/img4.jpg', "rb") as img:
        await message.answer_photo(img, f"Название: {prod[3][1]} | Описание: {prod[3][2]} | Цена: {prod[3][3]}")
    await message.answer('Выберите продукт для покупки:', reply_markup=bt_menu1)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer(f'(10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x 1,55')
    await call.answer()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    check_user = is_included(data['username'])
    if check_user is True:
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Регистрация пользователя {data["username"]} прошла успешно')
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def send_calories(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['age']) + 6.25 * int(data['growth']) - 5 * int(data['weight']) + 5) * 1.55
    await message.answer(f'Ваша норма калорий:{result}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


executor.start_polling(dp, skip_updates=True)