import requests

url = 'http://127.0.0.1:8000/playground/header/'
header = {'test': 'ahoj'}


response = requests.get(url, headers=header)
print(response.json())