import requests

response = requests.get(
    url='https://gist.githubusercontent.com/coleifer/9899de010c647823a14f'
        '/raw/b5886f430414993f8f6e9ae1d587793b8f1e1d4c/analytics.py')

with open('close.py', 'wb') as opener:
    opener.write(response.content)
