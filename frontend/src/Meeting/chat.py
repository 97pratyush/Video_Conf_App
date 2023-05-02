from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

app = QApplication()


# Prototype from chatgpt

class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QTextEdit for displaying the chat messages
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Create a QLineEdit for entering new messages
        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        # Create a QPushButton for sending messages
        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)

        # Connect the send_button clicked signal to the send_message method
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        # Get the message from the message_input and clear the input field
        message = self.message_input.text()
        self.message_input.clear()

        # Display the message in the chat_display
        if message:
            self.chat_display.append(message)

# Create a ChatScreen widget and show it
chat_screen = ChatScreen()
chat_screen.show()

app.exec()
