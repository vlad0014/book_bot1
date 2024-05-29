from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_books_keyboard(books: list):
   builder = InlineKeyboardBuilder()
   for index, book in enumerate(books):
       builder.button(text=book.get("title"), callback_data=f"book_{index}")
   return builder.as_markup()

def build_book_details_keyboard(url):
   builder = InlineKeyboardBuilder()
   builder.button(text="Перейти за посиланням", url=url)
   builder.button(text="Go back", callback_data="back")
   return builder.as_markup()

def build_menu_keyboard():
   builder = InlineKeyboardBuilder()
   builder.button(text="Go back", callback_data="back")
   return builder.as_markup()