import requests

url = 'http://127.0.0.1:8000/session/stand/'
header = {'sid': 'a2faf5a510c44bcc867310ac0859a846',
          'gid': "5",
          }


response = requests.get(url, headers=header)
print(response.json())