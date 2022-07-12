import requests
from pprint import pprint

url = 'http://localhost:8000/api/'
headers = {'Authorization': "Token 0b331f7f013bb660100f47140afc4a09d7c697a5"}
body = {
    'title': "testuoajm per Python",
    'content': "sauletas antradienis, dziaugiames tyla... kol galim"
}

result = requests.post(url+'posts/', data=body, headers=headers)

if result.status_code >= 200 and result.status_code < 204:
    pprint(result.json())
print(result.status_code)
