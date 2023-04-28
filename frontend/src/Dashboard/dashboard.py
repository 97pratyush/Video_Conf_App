from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt
from style import primary_cta_style, secondary_cta_style
from Dashboard.join_meeting_dialog import JoinMeeting
from Meeting.meeting import MeetingPage


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        self.welcome_label = QLabel(
            "<font size=40>Welcome, User</font>", alignment=Qt.AlignCenter
        )

        self.create_meeting = QPushButton("Create a meeting")
        self.create_meeting.setStyleSheet(primary_cta_style)
        self.create_meeting.clicked.connect(self.start_meeting)

        self.join_meeting_cta = QPushButton("Join Meeting")
        self.join_meeting_cta.setStyleSheet(secondary_cta_style)
        self.join_meeting_cta.clicked.connect(self.join_meeting)

        self.layout = QVBoxLayout()
        self.widgets = [
            self.welcome_label,
            self.create_meeting,
            self.join_meeting_cta,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)

        self.setLayout(self.layout)

    def start_meeting(self):    
        self.meeting_page = MeetingPage()
        self.meeting_page.show()

    def join_meeting(self):
        self.join_meeting_dialog = JoinMeeting()
        self.join_meeting_dialog.show()

        # self.meeting_page = MeetingPage()
        # self.meeting_page.show()///
