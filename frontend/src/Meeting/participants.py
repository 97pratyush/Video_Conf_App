from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QListView, QVBoxLayout, QListWidget

class ParticipantScreen(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.page_title = QLabel(
            f"<font size=5>Participants</font>", alignment=Qt.AlignCenter
        )
        # Create a QListWidget for displaying the chat messages
        self.participant_display = QListWidget()
        self.participant_display.setViewMode(QListView.ViewMode.ListMode)
        layout.addWidget(self.page_title)
        layout.addWidget(self.participant_display)
        self.participant_display.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
                margin: 0px;
            }
        """)
