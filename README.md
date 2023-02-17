# vk_auto_publisher

The program downloads random meme from [xkcd](https://xkcd.com/) site with its comment and publish them on
your [vk](https://vk.com/) public wall.

## Environment

### Requirements

Python3(python 3.11 is recommended) should be already installed. Then use pip3 to install dependencies:

```bash
pip3 install -r requirements.txt
```

### Environment variables

- VK_APP_CLIENT_ID
- VK_GROUP_ID
- VK_ACCESS_TOKEN
- VK_USER_ID

1. Put `.env` file near `requirements.txt`.
2. `.env` contains text data without quotes.

For example, if you print `.env` content, you will see:

```bash
$ cat .env
VK_APP_CLIENT_ID=your_vk_client_id
VK_GROUP_ID=your_vk_group_id
VK_ACCESS_TOKEN=your_vk_access_token
VK_USER_ID=your_vk_user_id
```

#### How to get

* Register on vk service [vk](https://vk.com/) and copy your `vk_user_id` which you can receive from the address bar on
  your vk account page
* Create a group on vk service [vk](https://vk.com/) and copy your `vk_group_id` which you can receive from the address
  bar on your vk group page
* Create a standalone vk app on vk service [vk_dev](https://vk.com/dev) and if you click on the “Edit” button for a new
  application, you will see its `vk_app_client_id` in the address bar
* Get your `vk_access_token` following instruction from [here](https://vk.com/dev/access_token)

## Run

Launch on Linux(Python 3) or Windows:

```bash
$(venv) python3 main.py
```