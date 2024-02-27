import requests


def download_img():
    url = "https://dvmn.org/filer/canonical/1542890876/16/"

    response = requests.get(url)
    response.raise_for_status()

    file_name = 'dvmn.svg'
    with open(file_name, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    download_img()