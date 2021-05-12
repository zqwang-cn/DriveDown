import re
import base64
import requests


def get_googledrive(url):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    URL = "https://drive.google.com/uc?export=download"
    id = re.search('/d/(.*)/', url).group(1)
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        response.close()
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    return response


def get_onedrive(url):
    def get_direct_url(url):
        data_bytes64 = base64.b64encode(bytes(url, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/', '_').replace('+', '-').rstrip("=")
        direct = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return direct

    direct = get_direct_url(url)
    response = requests.get(direct, stream=True)
    return response


def get_dropbox(url):
    url = url.replace("www.dropbox.com", "dl.dropbox.com")
    response = requests.get(url, stream=True)
    return response


def get_response(drivetype, url):
    try:
        if drivetype == 'googledrive':
            return get_googledrive(url)
        elif drivetype == 'onedrive':
            return get_onedrive(url)
        elif drivetype == 'dropbox':
            return get_dropbox(url)
        else:
            return None
    except:
        return None
