from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PySide6.QtCore import Slot
from Home.login_page import LoginPage
from Home.signup_page import SignupPage
from Dashboard.dashboard import DashboardPage

import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.parent_widget = QStackedWidget()

        self.login_page = LoginPage()
        self.login_page.goto_dashboard_signal.connect(self.add_to_stacked_widget)
        self.sign_up_page = SignupPage()
        self.sign_up_page.goto_dashboard_signal.connect(self.add_to_stacked_widget)
        self.is_logged_in = True

        if self.is_logged_in == False:
            self.parent_widget.addWidget(self.login_page)
            self.parent_widget.addWidget(self.sign_up_page)
            self.parent_widget.setCurrentWidget(self.login_page)
        else:
            self.add_to_stacked_widget(DashboardPage(31, "Siddharth Sircar"))


        # self.parent_widget.addWidget(self.dashboard)

        self.setCentralWidget(self.parent_widget)

    def navigate(self, obj):
        self.setCentralWidget(obj)

    @Slot(QWidget)
    def add_to_stacked_widget(self, widget):
        self.parent_widget.addWidget(widget)
        self.parent_widget.setCurrentWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    home = MainWindow()
    home.setWindowTitle("Cloud Meetings")
    home.resize(650, 450)
    home.setAutoFillBackground(True)
    home.setStyleSheet("QMainWindow" "{" "background : white;" "}")
    home.show()

    sys.exit(app.exec())
