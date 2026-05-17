import requests

url = "http://127.0.0.1:5000/api/vehicles"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3OTAwMTYxOCwianRpIjoiZjIxZTkyNTctZjRiYy00YmExLThmYzgtMzUwZTU4YjFmZTJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzc5MDAxNjE4LCJjc3JmIjoiOTgxNjYxYWYtMmJkZi00N2RkLTkyOTQtYWQ4YTgwMjc0YWNiIiwiZXhwIjoxNzc5MDAyNTE4fQ.vAx9U2CZNU-mppGezFrnkEhGy7PvspmHXHrWRk9zkZc"

headers = {

    "Authorization":
    f"Bearer {token}"
}

response = requests.get(
    url,
    headers=headers
)

print(response.json())