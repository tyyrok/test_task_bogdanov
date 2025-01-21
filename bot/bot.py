import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from api_request import make_request


if not load_dotenv("src/.env"):
    raise FileNotFoundError

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

kb = [
    [types.KeyboardButton(text="Получить данные по товару")],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    one_time_keyboard=True,
)


class MyForm(StatesGroup):
    waiting_for_article = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command.
    """
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard
    )


@dp.message(F.text == "Получить данные по товару")
async def send_article_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(MyForm.waiting_for_article)
    await message.answer(
        "Введите артикул:", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(MyForm.waiting_for_article)
async def article_handler(message: Message, state: FSMContext) -> None:
    user_input = message.text
    await state.clear()
    try:
        data = await make_request(user_input)
    except Exception as ex:
        return await message.answer(str(ex), reply_markup=keyboard)

    msg = (
        "По артикулу найден следующий продукт:\n"
        f"Название - {data.get('title')}\n"
        f"Артикул - {data.get('article')}\n"
        f"Цена - {data.get('price')/100} p.\n"
        f"Рейтинг - {data.get('rating')}\n"
        f"Кол-во - {data.get('total_amount')}\n"
        f"Дата обновления - {data.get('updated_at')}\n"
    )
    await message.answer(msg, reply_markup=keyboard)


@dp.message()
async def main_handler(message: Message) -> None:
    await message.answer("Используй кнопку...", reply_markup=keyboard)


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
