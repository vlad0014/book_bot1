from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from ..data import get_books, get_book, save_book

from ..keyboards import build_books_keyboard, build_book_details_keyboard

from ..fsm import BookCreateForm

book_router = Router()


@book_router.message(Command("books"))
@book_router.message(F.text.casefold() == "show_books")
async def show_books_command(message: Message, state: FSMContext) -> None:
    books = get_books()
    if books:
        keyboard = build_books_keyboard(books)
        await message.answer(
            text="Виберіть будь-яку книжку",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text="Книжку не знайдено :( \nДодайте нову книжку")


@book_router.callback_query(F.data.startswith("book_"))
async def show_book_details(callback: CallbackQuery, state: FSMContext) -> None:
    book_id = int(callback.data.split("_")[-1])
    book = get_book(book_id)
    text = f"Назва:{hbold(book.get('title'))}\nОпис:{hbold(book.get('desc'))}\nРейтинг:{hbold(book.get('rating'))}"
    photo_id = book.get('photo')
    url = book.get('url')
    print(photo_id)
    print(url)
    await callback.message.answer_photo(photo_id)
    await edit_or_answer(callback.message, text, build_book_details_keyboard(url))

@book_router.message(Command("bookcreate"))
@book_router.message(F.text.casefold() == "bookcreate")
@book_router.message(F.text.casefold() == "create book")
async def create_book_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(BookCreateForm.title)
    await edit_or_answer(message, "Яка назва книжки?", ReplyKeyboardRemove())


@book_router.message(BookCreateForm.title)
async def procees_title(message: Message, state: FSMContext) -> None:
   await state.update_data(title=message.text)
   await state.set_state(BookCreateForm.desc)
   await edit_or_answer(message, "Який опис книжки?", ReplyKeyboardRemove())




@book_router.message(BookCreateForm.desc)
async def procees_desctription(message: Message, state: FSMContext) -> None:
   data = await state.update_data(desc=message.text)
   await state.set_state(BookCreateForm.url)
   await edit_or_answer(
       message,
       f"Введіть посилання на книжку: {hbold(data.get('title'))}",
       ReplyKeyboardRemove(),
   )


@book_router.message(BookCreateForm.url)
@book_router.message(F.text.contains('http'))
async def procees_url(message: Message, state: FSMContext) -> None:
   data = await state.update_data(url=message.text)
   await state.set_state(BookCreateForm.photo)
   await edit_or_answer(
       message,
       f"Надайте фото для афіші книжки: {hbold(data.get('title'))}",
       ReplyKeyboardRemove(),
   )


@book_router.message(BookCreateForm.photo)
@book_router.message(F.photo)
async def procees_photo_binary(message: Message, state: FSMContext) -> None:
   photo = message.photo[-1]
   photo_id = photo.file_id


   data = await state.update_data(photo=photo_id)
   await state.set_state(BookCreateForm.rating)
   await edit_or_answer(
       message,
       f"Надайте рейтинг книжки: {hbold(data.get('title'))}",
       ReplyKeyboardRemove(),
   )


@book_router.message(BookCreateForm.rating)
async def procees_rating(message: Message, state: FSMContext) -> None:
   data = await state.update_data(rating=message.text)
   await state.clear()
   save_book(data)
   return await show_books_command(message, state)


@book_router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext) -> None:
    return await show_books_command(callback.message, state)

async def edit_or_answer(message: Message, text: str, keyboard, *args, **kwargs):
    if message.from_user.is_bot:
        await message.edit_text(text=text, reply_markup=keyboard, **kwargs)
    else:
        await message.answer(text=text, reply_markup=keyboard, **kwargs)