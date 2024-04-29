from requests import get, post, delete

print(get('https://serg.space/api/v2/orders').json())
print(get('https://serg.space/api/v2/orders/4').json())
print(get('https://serg.space/api/v2/orders/10').json())
print(get('https://serg.space/api/v2/orders/q').json())
print(post('https://serg.space/api/v2/orders', json={'person': 1, 'pause': 3, 'meal': 'макароны-3, кола-8'}).json())
print(post('https://serg.space/api/v2/orders', json={'person': 2, 'pause': 3, 'meal': 'макароны-3'}).json())
print(post('https://serg.space/api/v2/orders',
           json={'person': 1, 'pause': 3, 'meal': 'макароны-3, котлета-3'}).json())
print(post('https://serg.space/api/v2/orders',
           json={'person': 1, 'pause': 3, 'meal': 'макароны-3, котлета-3', 'status': True}).json())
print(get('https://serg.space/api/v2/orders').json())
print(delete('https://serg.space/api/v2/orders/6').json())
print(get('https://serg.space/api/v2/orders').json())