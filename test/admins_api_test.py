from requests import get, post

print(get('https://serg.space/api/v2/admins').json())
print(get('https://serg.space/api/v2/admins/2').json())
print(get('https://serg.space/api/v2/admins/10').json())
print(get('https://serg.space/api/v2/admins/q').json())

print(post('https://serg.space/api/v2/admins',
           json={'name': 'Елена', 'surname': 'Летучая', 'keyword': 'qwerty', 'password': '663311'}).json())
print(post('https://serg.space/api/v2/admins',
           json={'name': 'Винтик', 'surname': 'Шпунтик', 'keyword': 'werty', 'password': '663311'}).json())
print(post('https://serg.space/api/v2/admins',
           json={'name': 'Капа', 'surname': 'Баба', 'keyword': 'qwerty', 'password': '663311'}).json())
print(get('https://serg.space/api/v2/admins').json())