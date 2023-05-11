from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QSize
from style import primary_cta_style
from Meeting.meeting_page import MeetingPage
from api_requests import end_meeting
from app_state import state

class MeetingInfoDialog(QDialog):
    def __init__(self, user_details, meeting_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Meeting Info")

        self.layout = QVBoxLayout()

        self.user_details = user_details
        self.user_id = user_details["id"]
        self.user_name = user_details["name"]
        self.meeting_id = int(meeting_id)

        self.meeting_info_label = QLabel(
            f"<font size=5>Hi {self.user_name}, share this meeting id with your attendees. <br/> Meeting Id: {self.meeting_id}</font>",
            alignment=Qt.AlignCenter,
        )
        self.meeting_info_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.meeting_info_label.setStyleSheet(
            "QLabel"
            "{"
            "color : black;"
            "margin-left : 100px;"
            "margin-right : 100px;"
            "}"
        )

        self.start_button = QPushButton("Start Meeting")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_button.sizePolicy().hasHeightForWidth()
        )
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setMinimumSize(QSize(110, 0))
        self.start_button.setStyleSheet(primary_cta_style)
        self.start_button.clicked.connect(self.accept)

        self.layout.addWidget(self.meeting_info_label)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def accept(self) -> None:
        try:
            self.meeting_page = MeetingPage(self.user_details, self.meeting_id)
            self.meeting_page.show()
            return super().accept()
        except Exception as e:
            print("Exception occured rendering Meeting Page:", e)
            return super().reject()
        
    def closeEvent(self, event):
        state.in_meeting = False
        try:
            end_meeting(self.user_id, self.meeting_id)            
            print("Ending call and closing streams")
        except Exception as e:
            print("Exception occured during end meeting :", e)
        finally:
            self.close()

        super().closeEvent(event)