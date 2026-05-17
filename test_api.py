import requests

url = "http://127.0.0.1:5000/api/vehicles"

data = {

    "vehicle_number": "MH40TEST",

    "expiry_date": "2026-06-10",

    "phone": "919999999999",

    "owner": "Ratnesh"
}

response = requests.post(
    url,
    json=data
)

print(response.json())