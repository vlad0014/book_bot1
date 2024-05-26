from aiogram.fsm.state import State, StatesGroup


class BookCreateForm(StatesGroup):
   title = State()
   desc = State()
   url = State()
   photo = State()
   rating = State()