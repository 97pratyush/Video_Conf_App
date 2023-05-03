from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from style import primary_cta_style
from Meeting.start_meeting import StartMeeting

class MeetingInfoDialog(QDialog):
    def __init__(self, user_details, meeting_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Meeting Info")

        self.layout = QVBoxLayout()

        self.user_details = user_details
        self.user_id = user_details['id']
        self.user_name = user_details['name']
        self.meeting_id = meeting_id

        self.meeting_info_label = QLabel(f"<font size=5>Hi {self.user_name}, share this meeting id with your attendees. <br/> Meeting Id: {self.meeting_id}</font>",
                                         alignment = Qt.AlignCenter)
        self.meeting_info_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.meeting_info_label.setStyleSheet(
            "QLabel"
            "{"
            "color : black;"
            'font-family : "Georgia", monospace;'
            "margin-left : 100px;"
            "margin-right : 100px;"
            "}"
        )


        self.start_button = QPushButton("Start Meeting")
        self.start_button.setStyleSheet(primary_cta_style)
        self.start_button.clicked.connect(self.accept)

        
        self.layout.addWidget(self.meeting_info_label)
        self.layout.addWidget(self.start_button)
        
        self.setLayout(self.layout)

    def accept(self) -> None:
        self.start_meeting = StartMeeting(self.user_details, self.meeting_id)
        self.start_meeting.show()
        return super().accept()
