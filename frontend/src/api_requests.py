import requests
import json
from constant import URL

def post(endpoint, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{URL}/{endpoint}", data=json.dumps(payload), headers=headers
    )

    if response.status_code in [200, 201, 401, 403]:
        print(f"{response.status_code}:{response.json()}")
    elif response.status_code in [404, 500]:
        print(f"Error:\n Url:{URL}/{endpoint} || Payload:{payload}.\n Response:\n", response.status_code , response.json())
    else:
        print(f"Check the request again. Something went wrong. Url:{URL}/{endpoint} || Payload:{payload}. || Status Code: {response.status_code}")

    return response

def sign_in(email, password):
    payload = {"email": email, "password": password}
    return post("login", payload)

def sign_up(name, email, password):
    payload = {"name": name, "email": email, "password": password}    
    return post("createUser", payload)

def create_meeting(user_id):
    payload = {"userId": int(user_id)}
    print(payload)
    return post("createMeeting", payload)

def join_meeting(user_id, meeting_id):
    payload = {"userId": int(user_id), "meetingId": int(meeting_id)}
    print(payload)
    return post("joinMeeting", payload)

def end_meeting(user_id, meeting_id):
    payload = {"userId": int(user_id), "meetingId": int(meeting_id)}
    return post("endMeeting", payload)