from Meeting.meeting_page import MeetingPage
from PySide6.QtWidgets import QMainWindow


class StartMeeting:
    def __init__(self) -> None:
        self.start_meeting = MeetingPage()
        self.mainWindow = QMainWindow()
        self.start_meeting.setupUi(self.mainWindow)
        self.mainWindow.show()
