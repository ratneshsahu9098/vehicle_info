import requests

url = "http://127.0.0.1:5000/api/login"

data = {

    "username": "admin",

    "password": "admin123"
}

response = requests.post(
    url,
    json=data
)

print(response.json())