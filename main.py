import glob
import os
import random
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

XKCD_URL_BASE = 'https://xkcd.com/'
VK_URL_BASE = 'https://api.vk.com/method/'

vk_group_id = os.getenv('VK_GROUP_ID')
vk_user_id = os.getenv('VK_USER_ID')
vk_access_token = os.getenv('VK_ACCESS_TOKEN')


def get_number_of_comic():
    url = os.path.join(XKCD_URL_BASE, 'info.0.json')
    response = requests.get(url)
    response.raise_for_status()
    number = response.json()["num"]

    return number


def download_pic_from_xkcd(pic_name, url):
    pic_name = f"{pic_name}{get_file_extension(url)}"
    filename = pic_name

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_file_extension(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext


def get_random_comic_from_xkcd():
    comics_number = random.randint(1, get_number_of_comic())
    url = os.path.join(XKCD_URL_BASE, str(comics_number), 'info.0.json')

    response = requests.get(url)
    response.raise_for_status()

    response_from_xkcd = response.json()
    image_url = response_from_xkcd['img']
    comment = response_from_xkcd['alt']
    download_pic_from_xkcd('random_image', image_url)

    return comment


def get_vk_upload_address():
    method = 'photos.getWallUploadServer'
    url = os.path.join(VK_URL_BASE, method)
    params = {
        'access_token': vk_access_token,
        'v': 5.131,
    }
    response = requests.post(url=url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']

    return upload_url


def upload_comic_on_server():
    with open('random_image.png', 'rb') as file:
        url = get_vk_upload_address()
        files = {
            'file': file,
        }
        response = requests.post(url=url, files=files)
        response.raise_for_status()
        server = response.json()["server"]
        photo = response.json()["photo"]
        hash_ = response.json()["hash"]

    return server, photo, hash_


def save_comics_on_server():
    method = 'photos.saveWallPhoto'
    url = os.path.join(VK_URL_BASE, method)
    uploaded_items = upload_comic_on_server()
    server = uploaded_items[0]
    photo = uploaded_items[1]
    hash_ = uploaded_items[2]
    params = {
        'access_token': vk_access_token,
        'v': 5.131,
        'server': server,
        'photo': photo,
        'hash': hash_,
    }
    response = requests.post(url=url, params=params)
    response.raise_for_status()
    media_id = response.json()['response'][0]['id']

    return media_id


def publish_comic(comment):
    method = 'wall.post'
    url = os.path.join(VK_URL_BASE, method)
    owner_id = vk_user_id
    media_id = save_comics_on_server()
    params = {
        'access_token': vk_access_token,
        'v': 5.131,
        'owner_id': vk_app_group_id,
        'from_group': 1,
        'attachments': f"photo{owner_id}_{media_id}",
        'message': comment,
    }
    response = requests.post(url=url, params=params)
    response.raise_for_status()

    return response


def remove_comic_file():
    for filename in glob.glob("random_image.*"):
        os.remove(filename)


def main():
    load_dotenv()
    comment = get_random_comic_from_xkcd()
    publish_comic(comment)
    remove_comic_file()


if __name__ == '__main__':
    main()
