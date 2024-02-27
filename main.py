import os

import requests


def download_img(url, path_name):

    response = requests.get(url)
    response.raise_for_status()

    with open(path_name, 'wb') as file:
        file.write(response.content)


def main():
    os.makedirs('books', exist_ok=True)

    start_id = 3268
    books_amount = 10
    for book_id in range(start_id, start_id + books_amount):
        url = f'https://tululu.org/txt.php?id={book_id}'
        book_path = os.path.join('books', f'book {book_id}.txt')
        download_img(url, book_path)


if __name__ == '__main__':
    main()
