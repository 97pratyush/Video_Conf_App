from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QSizePolicy
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

        self.error_label = QLabel()
        self.error_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.error_label.setStyleSheet(
            "QLabel"
            "{"
            "color : red;"
            "font-weight : bold;"
            "margin-left : 100px;"
            "margin-right : 100px;"
            "}"
        )

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
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.signin_button)
        self.layout.addWidget(self.signup_button)
        self.setLayout(self.layout)

    def navigate_signup(self):
        # Get the index of the next page
        index = self.parent().currentIndex() + 1
        # Show the next page
        self.parent().setCurrentIndex(index)

    def navigate_dashboard(self):
        self.error_label.setText("")
        self.email = self.email_textbox.text().strip()
        self.password = self.password_textbox.text().strip()
        if self.email and self.password:
            self.response = self.sign_in(self.email, self.password)
            # print(self.response['message'])
            self.data = self.response.json()
            if self.response.status_code == 200 and self.data['id'] == 0:
                self.error_label.setText("Invalid Credentials.")
            elif self.response.status_code == 200:
                self.user_id = self.data['id']
                # Get the index of the next page
                index = self.parent().currentIndex() + 2
                # Show the next page
                self.parent().setCurrentIndex(index)
            else:
                self.error_label.setText("Something went wrong.")
        else:
            self.error_label.setText("Please Enter Email/Password.")      

    def sign_in(self, email, password):
        payload = {"email": email, "password": password}
        return post("login", payload)
