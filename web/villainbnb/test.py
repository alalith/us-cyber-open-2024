import requests

def validate_image_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        if content_type and 'image' in content_type:
            return True
        else:
            return response.text
    except requests.exceptions.RequestException:
        return False


if validate_image_url('https://google.com') != True:
    print("fuck")
else:
    print("true")
