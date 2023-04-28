from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QListWidgetItem,
)
from style import primary_cta_style


class MeetingPage(QMainWindow):
    def __init__(self, parent=None):
        super(MeetingPage, self).__init__(parent)

        self.setWindowTitle("Meeting")

        self.parent_layout = QVBoxLayout()
        self.meeting_layout = QHBoxLayout()
        self.video_layout = QGridLayout()

        # self.video_label1 = QLabel("Video Tile 1")
        # self.video_label2 = QLabel("Video Tile 2")
        # self.video_label3 = QLabel("Video Tile 3")
        # self.video_label4 = QLabel("Video Tile 4")
        labels = []

        # Create 4 Labels and add them to a list
        for i in range(5):
            label = QLabel(f"Attendee {str(i + 1)}")
            label.setStyleSheet(
                "QLabel"
                "{"
                "font-weight : bold;"
                'font-family : "Georgia", monospace;'
                "font-style : italic;"
                "border-style: solid;"
                "border-width : 1px;"
                "border-color : black;"
                "}"
            )
            labels.append(label)

        # Video Container: Grid layout of video tiles

        row = 0
        col = 0
        for label in labels:
            self.video_layout.addWidget(label, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # self.video_layout.addWidget(self.video_label1)
        # self.video_layout.addWidget(self.video_label2)
        # self.video_layout.addWidget(self.video_label3)
        # self.video_layout.addWidget(self.video_label4)

        self.video_container = QWidget()
        self.video_container.setLayout(self.video_layout)
        # self.video_container.setFixedSize(400, 300)

        # self.attendee_labe1 = QLabel("Attendee 1")
        # self.attendee_labe2 = QLabel("Attendee 2")
        # newItem = QListWidgetItem()
        # newItem.setText("Attendee 1")

        self.attendees_list = QListWidget()
        self.attendees_list.addItem("Attendee 1")
        self.attendees_list.addItem("Attendee 2")
        self.attendees_list.setFixedSize(100, self.height())

        # Meeting Container: HLayout with Video Container and Attendees List
        self.meeting_layout.addWidget(self.video_container)
        self.meeting_layout.addWidget(self.attendees_list)

        self.meeting_container = QWidget()
        self.meeting_container.setLayout(self.meeting_layout)

        self.end_call_button = QPushButton("End Call")
        self.end_call_button.setStyleSheet(primary_cta_style)
        self.end_call_button.clicked.connect(self.end_call)
        # VBoxLayout: HBoxLayout Widget + End call button
        self.parent_layout.addWidget(self.meeting_container)
        self.parent_layout.addWidget(self.end_call_button)

        self.parent_container = QWidget()
        self.parent_container.setLayout(self.parent_layout)

        self.setCentralWidget(self.parent_container)
        self.resize(700, 500)
        self.setAutoFillBackground(True)
        self.setStyleSheet("QMainWindow" "{" "background : white;" "}")

    def end_call(self):
        self.close()
