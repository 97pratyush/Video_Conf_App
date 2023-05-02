import requests
import json

url = "https://31c9-2601-646-9d01-1da0-306f-58d9-970e-e48.ngrok-free.app"


def post(endpoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{url}/{endpoint}", data=json.dumps(payload), headers=headers
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response.status_code)

    return response

def sign_in(email, password):
    payload = {"email": email, "password": password}
    return post("login", payload)

def sign_up(name, email, password):
    payload = {"name": name, "email": email, "password": password}
    return post("createUser", payload)