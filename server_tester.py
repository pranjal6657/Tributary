import requests as requests

data = {
    "engine_temperature": 0.3,
}

response = requests.post("http://0.0.0.0:8000/record", json=data)
print(response.content)
