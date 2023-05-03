from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy
from PySide6.QtGui import QIntValidator
from style import primary_cta_style, textbox_style
from api_requests import join_meeting
from Meeting.start_meeting import StartMeeting

class JoinMeetingDialog(QDialog):
    def __init__(self, user_details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Join Meeting")
        self.layout = QVBoxLayout()
        self.user_details = user_details
        self.user_id = user_details['id']
        self.meeting_id_textbox = QLineEdit()
        self.meeting_id_textbox.setPlaceholderText("Meeting Id")
        self.meeting_id_textbox.setStyleSheet(textbox_style)
        validator = QIntValidator()
        self.meeting_id_textbox.setValidator(validator)

        self.join_button = QPushButton("Join")
        self.join_button.setStyleSheet(primary_cta_style)
        self.join_button.clicked.connect(self.accept)

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

        self.layout.addWidget(self.meeting_id_textbox)
        self.layout.addWidget(self.join_button)
        self.layout.addWidget(self.error_label)
        self.setLayout(self.layout)

    def accept(self) -> None:
        meeting_id = self.meeting_id_textbox.text().strip()
        if meeting_id:
            meeting_id = int(meeting_id)
            response = join_meeting(self.user_id, meeting_id)
            if response.status_code == 200:
                self.start_meeting = StartMeeting(self.user_details, meeting_id)
                self.start_meeting.show()
                return super().accept()
            else:
                self.error_label.setText("Incorrect meeting id.")
        else:
            self.error_label.setText("Enter meeting id.")
