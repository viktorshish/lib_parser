import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import click
import requests
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def dowload_img(img_url, filename, folder='img/'):
    response = requests.get(img_url)
    response.raise_for_status()

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_txt(url, params, filename, folder='books/'):
    response = requests.get(url, params=params)
    response.raise_for_status()

    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'w') as file:
        file.write(response.text)


def get_book_response(url):
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)
    return response


def pars_book_page(response, url):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('td', class_="ow_px_td").find('h1')

    genres_tag = soup.find('span', class_='d_book').find_all('a')

    comments_tag = soup.find_all('div', class_='texts')

    img_tag = soup.find('div', class_="bookimage").find('img')['src']
    return {
        'title': title_tag.text.split('   ::   ')[0],
        'author': title_tag.text.split('   ::   ')[1],
        'genres': [tag.text for tag in genres_tag],
        'comments': comments_tag,
        'img_url': urljoin(url, img_tag),
    }

@click.command()
@click.argument('id', type=click.INT)
@click.argument('count', type=click.INT)
def main(id, count):
    """Скрипт скачивает заданное количество книг с сайта tululu.org.

        id (int): ID книги с которой начнется скачиваение книг.

        count (int): Количество скачиваемых книг.
    """
    for book_id in range(id, id + count):
        url = f'https://tululu.org/b{book_id}/'
        txt_url = 'https://tululu.org/txt.php'
        params = {"id": book_id}

        try:
            book_response = get_book_response(url)
            book = pars_book_page(book_response, url)

            download_txt(txt_url, params, f'{book_id}. {book['title']}', folder='books/')

            print(f'Заголовок: {book['title']}')
            print(f'Автор: {book['author']}')
            print(f'Жанры: {book['genres']}')
            comments = [comment.find('span').text for comment in book['comments']]
            if comments:
                print(f'Комментарии: {comments} \n')
            else:
                print('Без комментариев \n')

            filename = urlparse(book['img_url']).path.split('/')[-1]
            dowload_img(book['img_url'], filename, folder='images/')

        except requests.exceptions.HTTPError:
            print(f'Не удалось загрузить книгу с ID {book_id}\n')


if __name__ == '__main__':
    main()
