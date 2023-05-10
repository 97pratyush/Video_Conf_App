import websocket
from PySide6.QtCore import QObject, Signal
import threading
import json

from constant import WS_URL

# Define a global variable to hold the socket object
ws = None

class SocketClient(QObject):
    message_received = Signal(dict)

    def __init__(self, meeting_id, user_id, user_name):
        super().__init__()
        self.meeting_id = meeting_id
        self.user_id = user_id
        self.user_name = user_name

        conn_status = self.get_connection_state()
        if conn_status == False or conn_status is None:
            self.connect_to_socket()

    def connect_to_socket(self):
        try:
            global ws
            ws = websocket.WebSocketApp(WS_URL,
                                        on_open=self.on_open,
                                        on_error=self.on_error,
                                        on_message=self.receive_messages,
                                        on_close=self.on_close)
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
        except Exception as e:
            print(e)

    def on_open(self, ws):
        print("Opened connection")
        # self.subscribeToChat()
        # self.subscribeToMeetingParticipant

    # def subscribeToChat(self):
    #     subscriptionInfo = {"type": "getChatMessages",
    #                         "meetingId": "1", "userId": "1"}
    #     self.send_message(json.dumps(subscriptionInfo))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###", close_status_code, close_msg)

    def receive_messages(self, ws, data):
        # print(type(data))
        # print(data)
        try:
            data = json.loads(data)
            self.message_received.emit(data)
            # if data["type"] == "chatMessageHistory":
            #     self.loadChatMessagehistory(data["history"])
            # elif data["type"] == "newChatMessage":
            #     self.addNewChatMessage(data["sender"], data["message"])
        except Exception as e:
            print(e)

    def send_message(self, message):
        message["userId"] = str(self.user_id)
        message["userName"] = self.user_name
        message["meetingId"] = str(self.meeting_id)
        print("here in send_message", message)

        message_str = json.dumps(message)
        # Send the message to the server
        if message:
            global ws
            ws.send(message_str)

    def get_connection_state(self):
        global ws
        if ws:
            return ws.sock and ws.sock.connected
        else:
            return False
        
    def close_socket(self):
        print("closing")
        try:
            global ws
            ws.close()
        except Exception as e:
            print(e)
