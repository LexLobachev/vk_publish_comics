import glob
import os
import random
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

XKCD_URL_BASE = 'https://xkcd.com/'
VK_URL_BASE = 'https://api.vk.com/method/'


def get_number_of_comic():
    url = os.path.join(XKCD_URL_BASE, 'info.0.json')
    response = requests.get(url)
    response.raise_for_status()
    number = response.json()["num"]

    return number


def download_pic_from_xkcd(pic_name, url):
    filename = pic_name

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_random_comic_from_xkcd():
    comics_number = random.randint(1, get_number_of_comic())
    url = os.path.join(XKCD_URL_BASE, str(comics_number), 'info.0.json')

    response = requests.get(url)
    response.raise_for_status()

    response_from_xkcd = response.json()
    image_url = response_from_xkcd['img']
    path = urlparse(image_url).path
    image_name = os.path.basename(path)
    comment = response_from_xkcd['alt']
    download_pic_from_xkcd(image_name, image_url)

    return comment, image_name


def get_vk_upload_address(vk_access_token):
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


def upload_comic_on_server(upload_url, image_name):
    with open(image_name, 'rb') as file:
        url = upload_url
        files = {
            'file': file,
        }
        response = requests.post(url=url, files=files)
    response.raise_for_status()

    return response


def save_comics_on_server(server, photo, hash_, vk_access_token):
    method = 'photos.saveWallPhoto'
    url = os.path.join(VK_URL_BASE, method)
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


def publish_comic(comment, vk_media_id, vk_group_id, vk_user_id, vk_access_token):
    method = 'wall.post'
    url = os.path.join(VK_URL_BASE, method)
    params = {
        'access_token': vk_access_token,
        'v': 5.131,
        'owner_id': vk_group_id,
        'from_group': 1,
        'attachments': f"photo{vk_user_id}_{vk_media_id}",
        'message': comment,
    }
    response = requests.post(url=url, params=params)
    response.raise_for_status()

    return response


def main():
    load_dotenv()
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_user_id = os.environ['VK_USER_ID']
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    comment, image_name = get_random_comic_from_xkcd()
    upload_url = get_vk_upload_address(vk_access_token)
    upload_items_response = upload_comic_on_server(upload_url, image_name)
    uploaded_items = upload_items_response.json()
    server, photo, hash_ = uploaded_items.items()
    media_id = save_comics_on_server(server, photo, hash_, vk_access_token)
    try:
        publish_comic(comment, media_id, vk_group_id, vk_user_id, vk_access_token)
    finally:
        os.remove(image_name)


if __name__ == '__main__':
    main()
