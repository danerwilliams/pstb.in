import requests

tructus = {'type': 'text/plain', 'name': 'test'}
response = requests.post('https://ez02ob0o22.execute-api.us-west-1.amazonaws.com/api/upload', json=tructus)
guy = response.json()
print(guy)

headers = {'Content-Type': 'text/plain'}
f = open('./test', 'rb')
result = requests.put(guy['body']['signed_url'], headers=headers, data=f)