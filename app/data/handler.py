import json
from json import JSONDecodeError


def get_books(f_path: str = "app/data/books.json") -> list:
    with open(f_path) as file_json:
        try:
            data = json.load(file_json)
            books = data.get("books")
            return books
        except JSONDecodeError:
            return None


def get_book(id: int = 0, f_path: str = "app/data/books.json") -> dict:
    return get_books(f_path)[id]


def save_book(film: dict = {}, f_path: str = "app/data/books.json") -> bool:
    with open(f_path) as file_json:
        data = json.load(file_json)
        books = data.get("books")
        books.append(book)
    with open(f_path, "w") as file_json:
        json.dump(data, file_json, indent=4)
    return True