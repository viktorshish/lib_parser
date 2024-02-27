import os

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    os.makedirs('books', exist_ok=True)

    start_id = 1
    books_amount = 10
    for book_id in range(start_id, start_id + books_amount):
        url = f'https://tululu.org/txt.php'
        params = {"id": book_id}
        book_path = os.path.join('books', f'book {book_id}.txt')

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            with open(book_path, 'wb') as file:
                file.write(response.content)

        except requests.exceptions.HTTPError:
            print(f'Не удалось загрузить книгу с ID {book_id}:')


if __name__ == '__main__':
    main()
