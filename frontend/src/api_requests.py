import requests
import json

url = "https://aa6e-2601-642-4c05-7588-b2c7-47b2-7d3e-f8d0.ngrok-free.app"


def post(endpoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{url}/{endpoint}", data=json.dumps(payload), headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        data = response
        print("Error:", response.status_code)

    return data
