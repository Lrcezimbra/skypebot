import io
from datetime import datetime

import requests
from decouple import config


FACEBOOK_APP_ID = config('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = config('FACEBOOK_APP_SECRET')

FACEBOOK_TOKEN = '{}|{}'.format(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
FACEBOOK_URL = 'https://graph.facebook.com/v2.12/'
PARAMS = {'access_token': FACEBOOK_TOKEN}
ALLEGRO_PHOTOS_URL = FACEBOOK_URL + '1723142844399679/photos/'
IMAGES_URL_FORMAT = FACEBOOK_URL + '{id}?fields=images'


def get_menu_image_url():
    photos = requests.get(ALLEGRO_PHOTOS_URL, params=PARAMS).json()
    last_photo = photos['data'][0]
    last_photo_date, _ = last_photo['created_time'].split('T')
    last_photo_date = datetime.strptime(last_photo_date, '%Y-%m-%d')

    if last_photo_date.date() < datetime.today().date():
        return last_photo_date, ''

    last_photo_informations = IMAGES_URL_FORMAT.format(id=last_photo['id'])

    last_photo_images = requests.get(
        last_photo_informations,
        params=PARAMS
    ).json()
    last_image_url = last_photo_images['images'][0]['source']
    return last_photo_date, last_image_url


def get_menu_image_content():
    date_posted, image_url = get_menu_image_url()
    if not image_url:
        return date_posted, False

    response = requests.get(image_url)
    return date_posted, io.BytesIO(response.content)
