from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Signal
from style import textbox_style, primary_cta_style, secondary_cta_style
from Dashboard.dashboard_page import DashboardPage
from api_requests import sign_up
from app_state import state

class SignupPage(QWidget):
    goto_dashboard_signal = Signal(QWidget)
    def __init__(self, parent=None):
        super(SignupPage, self).__init__(parent)

        self.layout = QVBoxLayout()
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

        self.setWindowTitle("Cloud Meetings - Create account")

        self.name_textbox = QLineEdit()
        self.name_textbox.setPlaceholderText("Enter Full Name")
        self.name_textbox.setProperty("mandatoryField", True)
        
        self.email_textbox = QLineEdit()
        self.email_textbox.setPlaceholderText("Enter Email")
        self.email_textbox.setProperty("mandatoryField", True)

        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_textbox.setPlaceholderText("Enter Password")
        self.password_textbox.setProperty("mandatoryField", True)

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

        self.signup_button = QPushButton("Create Account")
        self.signup_button.setStyleSheet(primary_cta_style)
        self.signup_button.clicked.connect(self.navigate_to_dashboard)

        self.login_label = QLabel("Already have an account?", alignment=Qt.AlignCenter)
        self.login_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.login_label.setStyleSheet(
            "QLabel"
            "{"
            "color : black;"
            "font-weight : bold;"
            "margin-left : 60px;"
            "margin-right : 60px;"
            "}"
        )

        self.signin_button = QPushButton("Sign In")
        self.signin_button.setStyleSheet(secondary_cta_style)
        self.signin_button.clicked.connect(self.navigate_to_signin)
        self.widgets = [
            self.title,
            self.name_textbox,
            self.email_textbox,
            self.password_textbox,
            self.error_label,
            self.signup_button,
            self.login_label,
            self.signin_button,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)

        self.setStyleSheet(textbox_style)
        self.setLayout(self.layout)

    def navigate_to_dashboard(self):
        self.error_label.setText("")
        self.name = self.name_textbox.text().strip()
        self.email = self.email_textbox.text().strip()
        self.password = self.password_textbox.text().strip()

        if self.email and self.password and self.name:            
            self.response = sign_up(self.name, self.email, self.password)
            # print(self.response['message'])
            self.data = self.response.json()
            if self.response.status_code == 200 and self.data['userId']:

                self.user_id = self.data['userId']
                self.user_name = self.data['name']
                state.user_id = self.user_id
                state.user_name = self.user_name
                state.is_logged_in = True

                self.error_label.setText("")
                self.name_textbox.setText("")
                self.email_textbox.setText("")
                self.password_textbox.setText("")

                dashboard = DashboardPage(self.user_id, self.user_name)
                self.goto_dashboard_signal.emit(dashboard)

            elif self.response.status_code == 403:
                self.error_label.setText("This email already exists. Try login.")
            else:
                self.error_label.setText("Something went wrong.")
        else:
            self.error_label.setText("Please enter all details.")
    
    def navigate_to_signin(self):
        self.error_label.setText("")
        self.name_textbox.setText("")
        self.email_textbox.setText("")
        self.password_textbox.setText("")

        # Get the index of the next page
        index = self.parent().currentIndex() - 1
        # Show the next page
        self.parent().setCurrentIndex(index)
