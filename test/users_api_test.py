from requests import get, post, delete

print(get('https://serg.space/api/v2/users').json())
print(get('https://serg.space/api/v2/users/1').json())
print(get('https://serg.space/api/v2/users/10').json())
print(get('https://serg.space/api/v2/users/q').json())

print(post('https://serg.space/api/v2/users', json={'surname': 'Архип', 'name': 'Ежов', 'grade': '10м'}).json())
print(post('https://serg.space/api/v2/users', json={'surname': 'Виталий', 'name': 'Краснов', 'grade': '10м'}).json())
print(post('https://serg.space/api/v2/users',
           json={'surname': 'Виталий', 'name': 'Краснов', 'grade': '10м', 'password': '663311'}).json())
print(get('https://serg.space/api/v2/users').json())
print(delete('https://serg.space/api/v2/users/4').json())
print(get('https://serg.space/api/v2/users').json())