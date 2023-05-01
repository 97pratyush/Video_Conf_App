import requests
import json

url = "https://31c9-2601-646-9d01-1da0-306f-58d9-970e-e48.ngrok-free.app"


def post(endpoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{url}/{endpoint}", data=json.dumps(payload), headers=headers
    )

    if response.status_code == 200:
        data = response
        print(data.json())
    else:
        data = response
        print("Error:", response.status_code)

    return data
