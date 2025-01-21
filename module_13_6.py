from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = 'your api'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton('Рассчитать'),
    types.KeyboardButton('Информация')
]
keyboard.add(*buttons)

inline_keyboard = types.InlineKeyboardMarkup()
inline_buttons = [
    types.InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
    types.InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
]
inline_keyboard.add(*inline_buttons)


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=keyboard)


@dp.message_handler(Text(equals='Рассчитать'))
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)


@dp.callback_query_handler(Text(equals='formulas'))
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: BMR = (10 * вес в кг) + (6.25 * рост в см) - (5 * возраст в годах) + 5\n"
        "Для женщин: BMR = (10 * вес в кг) + (6.25 * рост в см) - (5 * возраст в годах) - 161"
    )
    await call.message.answer(formula_message)
    await call.answer()


@dp.callback_query_handler(Text(equals='calories'))
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.answer('Введите свой возраст:')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост:')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес:')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5

    await message.answer(f'Ваша норма калорий: {calories:.2f}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)