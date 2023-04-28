from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from style import textbox_style, primary_cta_style, secondary_cta_style
from api_requests import post


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.title = QLabel(
            "<font size=40 color=#3477eb>Cloud Meetings</font>",
            alignment=Qt.AlignCenter,
        )

        self.title.setStyleSheet(
            "QLabel"
            "{"
            "height: 500px;"
            "font-weight : bold;"
            'font-family : "Georgia", monospace;'
            "font-style : italic"
            "}"
        )

        self.email_textbox = QLineEdit()
        self.email_textbox.setProperty("mandatoryField", True)
        self.email_textbox.setPlaceholderText("Enter Email")
        self.email_textbox.setStyleSheet(textbox_style)

        self.password_textbox = QLineEdit()
        self.password_textbox.setProperty("mandatoryField", True)
        self.password_textbox.setPlaceholderText("Enter Password")
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_textbox.setStyleSheet(textbox_style)

        self.signin_button = QPushButton("Sign In")
        self.signin_button.setStyleSheet(primary_cta_style)
        self.signin_button.clicked.connect(self.navigate_dashboard)

        self.signup_button = QPushButton("Create Account")
        self.signup_button.setStyleSheet(secondary_cta_style)
        self.signup_button.clicked.connect(self.navigate_signup)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.email_textbox)
        self.layout.addWidget(self.password_textbox)
        self.layout.addWidget(self.signin_button)
        self.layout.addWidget(self.signup_button)
        self.setLayout(self.layout)

    def navigate_signup(self):
        # Get the index of the next page
        index = self.parent().currentIndex() + 1
        # Show the next page
        self.parent().setCurrentIndex(index)

    def navigate_dashboard(self):
        payload = {"email": "krishna.gupta@sjsu.edu", "password": "password"}
        post("login", payload)
        # Get the index of the next page
        index = self.parent().currentIndex() + 2
        # Show the next page
        self.parent().setCurrentIndex(index)
