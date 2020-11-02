import requests

res = requests.post('http://13.209.217.37/api', data={'location': 280}).json()

print(res['location'])