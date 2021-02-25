import requests

from config import LINE_NOTIFY_API


def pushImage(token, msg, image_path):
    headers = {"Authorization": "Bearer " + token}

    payload = {'message': msg}
    files = {'imageFile': open(image_path, 'rb')}
    r = requests.post(LINE_NOTIFY_API,
                      headers=headers,
                      params=payload,
                      files=files)

    return r.status_code


def pushMessage(token, msg):
    headers = {"Authorization": "Bearer " + token}

    payload = {'message': msg}
    r = requests.post(LINE_NOTIFY_API,
                      headers=headers,
                      params=payload)

    return r.status_code
