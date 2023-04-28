from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QGridLayout,
)
from PySide6.QtCore import Qt
from style import textbox_style, primary_cta_style, secondary_cta_style
from Dashboard.dashboard import Dashboard


class SignupPage(QWidget):
    def __init__(self, parent=None):
        super(SignupPage, self).__init__(parent)

        self.layout = QGridLayout()

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
            self.name_textbox,
            self.email_textbox,
            self.password_textbox,
            self.signup_button,
            self.login_label,
            self.signin_button,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)

        self.setStyleSheet(textbox_style)
        self.setLayout(self.layout)

    def navigate_to_dashboard(self):
        # Get the index of the next page
        index = self.parent().currentIndex() + 1
        # Show the next page
        self.parent().setCurrentIndex(index)

    def navigate_to_signin(self):
        # Get the index of the next page
        index = self.parent().currentIndex() - 1
        # Show the next page
        self.parent().setCurrentIndex(index)
