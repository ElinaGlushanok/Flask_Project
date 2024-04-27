from requests import get, post, delete

print(get('https://serg.space/api/v2/users').json())
print(get('https://serg.space/api/v2/users/1').json())
print(get('https://serg.space/api/v2/users/10').json())
print(get('https://serg.space/api/v2/users/q').json())

print(post('https://serg.space/api/v2/users', json={'surname': 'Виталий', 'name': 'Краснов', 'grade': '10м'}).json())
print(get('https://serg.space/api/v2/users').json())
print(delete('https://serg.space/api/v2/users/9').json())
print(get('https://serg.space/api/v2/users').json())