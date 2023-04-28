from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt
from style import primary_cta_style, secondary_cta_style
from Dashboard.join_meeting_dialog import JoinMeeting

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        self.welcome_label = QLabel(
            "<font size=40>Welcome, User</font>", alignment=Qt.AlignCenter
        )

        self.start_meeting = QPushButton("Create a meeting")
        self.start_meeting.setStyleSheet(primary_cta_style)

        self.join_meeting_cta = QPushButton("Join Meeting")
        self.join_meeting_cta.setStyleSheet(secondary_cta_style)
        self.join_meeting_cta.clicked.connect(self.join_meeting)
        self.layout = QVBoxLayout()
        self.widgets = [
            self.welcome_label,
            self.start_meeting,
            self.join_meeting_cta,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)

        self.setLayout(self.layout)

    def join_meeting(self):
        self.join_meeting_dialog = JoinMeeting()
        self.join_meeting_dialog.show()
