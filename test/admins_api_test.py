from requests import get, post

print(get('http://localhost:5000/api/v2/admins').json())
print(get('http://localhost:5000/api/v2/admins/2').json())
print(get('http://localhost:5000/api/v2/admins/10').json())
print(get('http://localhost:5000/api/v2/admins/q').json())

print(post('http://localhost:5000/api/v2/admins',
           json={'name': 'Елена', 'surname': 'Летучая', 'keyword': 'qwerty', 'password': '663311'}).json())
print(post('http://localhost:5000/api/v2/admins',
           json={'name': 'Винтик', 'surname': 'Шпунтик', 'keyword': 'werty', 'password': '663311'}).json())
print(post('http://localhost:5000/api/v2/admins',
           json={'name': 'Капа', 'surname': 'Баба', 'keyword': 'qwerty', 'password': '663311'}).json())
print(get('http://localhost:5000/api/v2/admins').json())