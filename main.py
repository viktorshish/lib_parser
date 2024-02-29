import os
from urllib.parse import urljoin

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


def pars_book(book_id):
    url = f'https://tululu.org/b{book_id}/'

    response = requests.get(url)
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('td', class_="ow_px_td").find('h1')
    img_tag = soup.find('div', class_="bookimage").find('img')['src']
    img_url = urljoin(url, img_tag)

    return {
        'title': title_tag.text.split('   ::   ')[0],
        'img_url': img_url,
    }


def main():
    start_id = 1
    books_amount = 10
    for book_id in range(start_id, start_id + books_amount):
        url = 'https://tululu.org/txt.php'
        # TODO: Сделать одну общуюю ссылку(уменьшить количество запросов)
        params = {"id": book_id}

        try:
            book = pars_book(book_id)
            title = book['title']
            download_txt(url, params, f'{book_id}. {title}', folder='books')
            print(f'Заголовок: {book['title']}')
            print(book['img_url'], '\n')

        except requests.exceptions.HTTPError:
            print(f'Не удалось загрузить книгу с ID {book_id}:\n')


if __name__ == '__main__':
    main()
