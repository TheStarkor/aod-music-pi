import requests

res = requests.post('http://localhost:7000/api', data={'location': 280}).json()

print(res['location'])