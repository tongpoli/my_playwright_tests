import requests

url = "https://jsonplaceholder.typicode.com/users"

data = {
    "name": "Jeff Li",
    "username": "jeffl",
    "email": "jeff@example.com"
}

response = requests.post(url, json=data)

print("status_code: ", response.status_code)
print("response JSON: ", response.json()['id'])
print("response JSON: ", response.json()['name'])
print("response JSON: ", response.json()['username'])
print("response JSON: ", response.json()['email'])