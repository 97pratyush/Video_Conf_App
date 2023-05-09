from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PySide6.QtCore import Slot
from Home.login_page import LoginPage
from Home.signup_page import SignupPage
from Dashboard.dashboard import DashboardPage
from app_state import state
import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.parent_widget = QStackedWidget()
        state.autopersist('app_state')
        self.login_page = LoginPage()
        self.login_page.goto_dashboard_signal.connect(self.add_to_stacked_widget)
        self.sign_up_page = SignupPage()
        self.sign_up_page.goto_dashboard_signal.connect(self.add_to_stacked_widget)
        self.parent_widget.addWidget(self.login_page)
        self.parent_widget.addWidget(self.sign_up_page)

        if "is_logged_in" not in state:
            state.is_logged_in = False

        if "user_id" not in state:
            state.user_id = ""
        
        if "user_name" not in state:
            state.user_name = ""
            
        if state.is_logged_in == False:            
            self.parent_widget.setCurrentWidget(self.login_page)
        else:
            self.add_to_stacked_widget(DashboardPage(state.user_id, state.user_name))
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
