from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QSizePolicy
)
from PySide6.QtCore import Qt
from style import end_meeting_cta_style

class MeetingPage(QWidget):
    def __init__(self, parent=None):
        super(MeetingPage, self).__init__(parent)

        self.setWindowTitle("Meeting")

        self.parent_layout = QVBoxLayout()
        self.meeting_layout = QHBoxLayout()
        self.video_layout = QGridLayout()

        self.labels = []

        # Create 4 Labels and add them to a list
        for i in range(1):
            label = QLabel(f"Attendee {str(i + 1)}", alignment=Qt.AlignCenter)
            label.setStyleSheet(
                "QLabel"
                "{"
                "color : white;"
                "font-weight : bold;"
                'font-family : "Georgia", monospace;'
                "font-style : italic;"
                "border-style: solid;"
                "border-width : 1px;"
                "border-color : white;"
                "}"
            )
            label.setFixedSize(640, 480)
            self.labels.append(label)

        # Video Container: Grid layout of video tiles

        row = 0
        col = 0
        for label in self.labels:
            self.video_layout.addWidget(label, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1


        self.video_container = QWidget()
        self.video_container.setLayout(self.video_layout)

        self.attendees_list = QListWidget()
        self.attendees_list.addItem("Attendee 1")
        self.attendees_list.addItem("Attendee 2")

        # Meeting Container: HLayout with Video Container and Attendees List
        self.meeting_layout.addWidget(self.video_container)
        self.meeting_layout.addWidget(self.attendees_list)

        self.meeting_container = QWidget()
        self.meeting_container.setLayout(self.meeting_layout)

        self.end_call_button = QPushButton("End Meeting")
        self.end_call_button.setFixedSize(100, 50)
        # SizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.end_call_button.setStyleSheet(end_meeting_cta_style)

        # VBoxLayout: HBoxLayout Widget + End call button
        self.parent_layout.addWidget(self.meeting_container)
        self.parent_layout.addWidget(self.end_call_button)

        # self.parent_container = QWidget()
        self.setLayout(self.parent_layout)

        # self.setCentralWidget(self.parent_container)        
