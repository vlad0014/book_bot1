from aiogram.fsm.context import FSMContext
from aiogram.types.dice import DiceEmoji
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.markdown import hbold

from routers import book_router
from routers.book import edit_or_answer, show_books_command

load_dotenv()

root_router = Router()
root_router.include_routers(book_router)


@root_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {hbold(message.from_user.full_name)}!\n Команди:\n books - список книжок \n "
                         f"bookcreate - додати книжку")


@root_router.message(Command("dice"))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)



async def main() -> None:
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(root_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)