from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QSizePolicy
from PySide6.QtCore import QSize
from PySide6.QtGui import QIntValidator
from style import primary_cta_style, textbox_style
from api_requests import join_meeting
from Meeting.meeting_page import MeetingPage

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

        self.join_button = QPushButton("Join Meeting")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.join_button.sizePolicy().hasHeightForWidth()
        )
        self.join_button.setSizePolicy(sizePolicy)
        self.join_button.setMinimumSize(QSize(110, 0))
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
                try:
                    self.meeting_page = MeetingPage(self.user_details, meeting_id)
                    self.meeting_page.show()
                    return super().accept()
                except Exception as e:
                    print("Exception occured during Meeting Page, :", e)
                    return super().reject()
            else:
                self.error_label.setText("Incorrect meeting id.")
        else:
            self.error_label.setText("Enter meeting id.")
