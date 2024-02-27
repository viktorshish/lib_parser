import requests


def download_img(url):

    response = requests.get(url)
    response.raise_for_status()

    file_name = 'book.txt'
    with open(file_name, 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://tululu.org/txt.php?id=32168'

    download_img(url)


if __name__ == '__main__':
    main()