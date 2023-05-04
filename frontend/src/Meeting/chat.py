from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QWidget, QListView, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton
from PySide6.QtGui import QColor, QBrush
import json
from socket_client import SocketClient
import time
app = QApplication()


# Prototype from chatgpt

class ChatScreen(QWidget):

    user_id = "1"
    meeting_id = "1"
    user_name = "krishna"

    def __init__(self):
        super().__init__()

        self.socket_client = SocketClient()
        self.socket_client.message_received.connect(self.receive_messages)

        self.setWindowTitle("Chat")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QListWidget for displaying the chat messages
        self.chat_display = QListWidget()
        self.chat_display.setViewMode(QListView.ViewMode.ListMode)
        layout.addWidget(self.chat_display)
        self.chat_display.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        # Create a QLineEdit for entering new messages
        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        # Create a QPushButton for sending messages
        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)

        # Connect the send_button clicked signal to the send_message method
        self.send_button.clicked.connect(self.send_new_chat_message)
        time.sleep(2)
        if self.socket_client.get_connection_state():
            print("Connected")
            self.subscribeToChat()
        else:
            print("Not connected")
        # self.chat_display.append(data)

    def subscribeToChat(self):
        subscriptionInfo = {"type": "getChatMessages",
                            "meetingId": self.meeting_id, "userId": self.user_id}
        self.socket_client.send_message(json.dumps(subscriptionInfo))

    def send_new_chat_message(self):
        messageText = self.message_input.text()
        self.message_input.clear()
        newChatMessageText = {"type": "sendChatMessage",
                              "meetingId": self.meeting_id, "userName": self.user_name, "message": messageText}
        self.socket_client.send_message(json.dumps(newChatMessageText))

    def receive_messages(self, data):
        try:
            if data["type"] == "chatMessageHistory":
                self.loadChatMessagehistory(data["history"])
            elif data["type"] == "newChatMessage":
                self.addNewChatMessage(data["sender"], data["message"])
        except Exception as e:
            print(e)

    def loadChatMessagehistory(self, chatHistory):
        for message in chatHistory:
            self.addNewChatMessage(message["sender"], message["message"])

    def addNewChatMessage(self, username, message):
        item = QListWidgetItem(f"{username}: {message}")
        item.setTextAlignment(Qt.AlignRight if username ==
                              self.user_name else Qt.AlignLeft)
        item.setBackground(
            QBrush(QColor("#0084ff") if username == self.user_name else QColor("#f2f2f2")))
        item.setForeground(QBrush(Qt.white) if username ==
                           self.user_name else QBrush(Qt.black))
        sizeHint = QSize(item.sizeHint().width(), item.sizeHint().height()+5)
        item.setSizeHint(sizeHint)

        # Add the item to the QListWidget
        self.chat_display.addItem(item)


# Create a ChatScreen widget and show it
chat_screen = ChatScreen()
chat_screen.show()

app.exec()
