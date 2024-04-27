import requests


api_url = 'https://random.imagecdn.app/v1/image?width=500&height=150&category=food&format=json'
photo = requests.get(api_url).json()['url']