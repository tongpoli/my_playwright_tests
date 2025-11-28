import requests

url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.delete(url)

print("status_code: ", response.status_code)