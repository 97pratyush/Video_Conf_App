import requests
import json

url = "https://31c9-2601-646-9d01-1da0-306f-58d9-970e-e48.ngrok-free.app"

def post(endpoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{url}/{endpoint}", data=json.dumps(payload), headers=headers
    )

    if response.status_code in [200, 201, 401, 403]:
        print(response.json())
    elif response.status_code in [404, 500]:
        print(f"Error:\n Url:{url}/{endpoint} || Payload:{payload}.\n Response:\n", response.status_code , response.json())
    else:
        print(f"Check the request again. Something went wrong. Url:{url}/{endpoint} || Payload:{payload}.")

    return response

def sign_in(email, password):
    payload = {"email": email, "password": password}
    return post("login", payload)

def sign_up(name, email, password):
    payload = {"name": name, "email": email, "password": password}    
    return post("createUser", payload)

def create_meeting(user_id):
    payload = {"userId": user_id}
    return post("createMeeting", payload)

def join_meeting(user_id, meeting_id):
    payload = {"userId": user_id, "meetingId": meeting_id}
    return post("joinMeeting", payload)

def end_meeting(user_id, meeting_id):
    payload = {"userId": user_id, "meetingId": meeting_id}
    return post("endMeeting", payload)