import requests

url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

print("status_code: ", response.status_code)
print("response JSON: ", response.json()['id'])
print("response JSON: ", response.json()['name'])
print("response JSON: ", response.json()['email'])