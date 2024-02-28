import os

from bs4 import BeautifulSoup
import requests
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, params, filename, folder='books/'):
    response = requests.get(url, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def pars_book_title(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('td', class_="ow_px_td").find('h1')
    return title_tag.text.split('   ::   ')


def main():
    start_id = 1
    books_amount = 10
    for book_id in range(start_id, start_id + books_amount):
        url = 'https://tululu.org/txt.php'
        params = {"id": book_id}
        title = pars_book_title(book_id)
        try:
            download_txt(url, params, f'{book_id}.{title[0]}', folder='books')
        except requests.exceptions.HTTPError:
            print(f'Не удалось загрузить книгу с ID {book_id}:')


if __name__ == '__main__':
    main()
