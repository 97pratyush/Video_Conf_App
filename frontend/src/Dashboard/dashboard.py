from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton, 
)
from PySide6.QtCore import Qt
from style import primary_cta_style, secondary_cta_style
from Dashboard.join_meeting import JoinMeetingDialog
from Dashboard.meeting_info import MeetingInfoDialog
from api_requests import create_meeting
from app_state import state, on

class DashboardPage(QWidget):
    def __init__(self, user_id, name, parent=None):
        super(DashboardPage, self).__init__(parent)

        self.user_details = {"id": user_id, "name": name}

        self.welcome_label = QLabel(
            f"<font size=40>Welcome, {self.user_details['name']}</font>", alignment=Qt.AlignCenter
        )

        self.create_meeting_cta = QPushButton("Create a meeting")
        self.create_meeting_cta.setStyleSheet(primary_cta_style)
        self.create_meeting_cta.clicked.connect(self.start_meeting)

        self.join_meeting_cta = QPushButton("Join Meeting")
        self.join_meeting_cta.setStyleSheet(secondary_cta_style)
        self.join_meeting_cta.clicked.connect(self.join_meeting)

        self.layout = QVBoxLayout()
        self.widgets = [
            self.welcome_label,
            self.create_meeting_cta,
            self.join_meeting_cta,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)
        self.setLayout(self.layout)               
        state.in_meeting = False 

    def start_meeting(self):
        response = create_meeting(self.user_details['id'])
        
        if response.status_code == 200:
            state.in_meeting = True
            meeting_id = response.json()['meetingId']
            print("Meeting Id: ", meeting_id)
            self.meeting_dialog = MeetingInfoDialog(self.user_details, meeting_id)
            self.meeting_dialog.show()

    def join_meeting(self):
        self.join_meeting_dialog = JoinMeetingDialog(self.user_details)
        self.join_meeting_dialog.show()

    @on('state.in_meeting')
    def on_meeting_status_change(self):
        print(f"Is user in meeting: {state.in_meeting}")
        self.join_meeting_cta.setDisabled(state.in_meeting)