from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit
from style import primary_cta_style, textbox_style


class JoinMeeting(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Join Meeting")
        self.layout = QVBoxLayout()

        self.meeting_id_textbox = QLineEdit()
        self.meeting_id_textbox.setPlaceholderText("Meeting Id")
        self.meeting_id_textbox.setStyleSheet(textbox_style)

        self.join_button = QPushButton("Join")
        self.join_button.setStyleSheet(primary_cta_style)
        self.join_button.clicked.connect(self.accept)

        self.layout.addWidget(self.meeting_id_textbox)
        self.layout.addWidget(self.join_button)
        self.setLayout(self.layout)
