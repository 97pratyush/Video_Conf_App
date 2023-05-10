from PySide6 import QtGui
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLayout,
    QPushButton,
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt, QSize, QMetaObject, QCoreApplication, QRect
import resources


class MeetingPage(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 554)
        MainWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n" "color: rgb(255, 255, 255);"
        )
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.meeting_layout = QHBoxLayout(self.centralwidget)
        self.meeting_layout.setContentsMargins(0, 0, 0, 0)
        self.meeting_layout.setSpacing(0)
        self.meeting_layout.setObjectName("horizontalLayout")
        self.video_layout = QGridLayout()
        self.video_layout.setObjectName("gridLayout")


        ########################## Video Labels ##########################
        self.label_6 = QLabel(parent=self.centralwidget)
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.video_layout.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_3 = QLabel(parent=self.centralwidget)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.video_layout.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_5 = QLabel(parent=self.centralwidget)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.video_layout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label = QLabel(parent=self.centralwidget)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.video_layout.addWidget(self.label, 1, 3, 1, 1)
        self.label_2 = QLabel(parent=self.centralwidget)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.video_layout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_4 = QLabel(parent=self.centralwidget)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.video_layout.addWidget(self.label_4, 1, 1, 1, 1)

        ########################################################

        self.button_control_layout = QHBoxLayout()
        self.button_control_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.button_control_layout.setContentsMargins(10, 10, 10, 10)
        self.button_control_layout.setSpacing(10)
        self.button_control_layout.setObjectName("button_control_layout")
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.button_control_layout.addItem(spacerItem)
        self.participants_cta = QPushButton(parent=self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.participants_cta.sizePolicy().hasHeightForWidth()
        )
        self.participants_cta.setSizePolicy(sizePolicy)
        self.participants_cta.setMinimumSize(QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.participants_cta.setFont(font)
        self.participants_cta.setCursor(
            QtGui.QCursor(Qt.CursorShape.PointingHandCursor)
        )
        self.participants_cta.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.participants_cta.setAutoFillBackground(False)
        self.participants_cta.setStyleSheet("padding:5px;\n" "border-radius:5px;")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/Icons/Icons/conference-multi-size.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.participants_cta.setIcon(icon)
        self.participants_cta.setIconSize(QSize(30, 30))
        self.participants_cta.setFlat(True)
        self.participants_cta.setObjectName("participants_cta")
        self.button_control_layout.addWidget(self.participants_cta)
        self.chat_cta = QPushButton(parent=self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chat_cta.sizePolicy().hasHeightForWidth())
        self.chat_cta.setSizePolicy(sizePolicy)
        self.chat_cta.setMinimumSize(QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.chat_cta.setFont(font)
        self.chat_cta.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.chat_cta.setStyleSheet("padding:5px;\n" "border-radius:5px;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/Icons/Icons/chat-2-multi-size.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.chat_cta.setIcon(icon1)
        self.chat_cta.setIconSize(QSize(30, 30))
        self.chat_cta.setFlat(True)
        self.chat_cta.setObjectName("chat_cta")
        self.button_control_layout.addWidget(self.chat_cta)
        self.end_meeting_cta = QPushButton(parent=self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.end_meeting_cta.sizePolicy().hasHeightForWidth()
        )
        self.end_meeting_cta.setSizePolicy(sizePolicy)
        self.end_meeting_cta.setMinimumSize(QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.end_meeting_cta.setFont(font)
        self.end_meeting_cta.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.end_meeting_cta.setStyleSheet(
            "padding:5px;\n"
            "border-radius:5px;\n"
            "background-color: rgb(170, 0, 0);\n"
            "color: rgb(255, 255, 255);"
        )
        self.end_meeting_cta.setObjectName("end_meeting_cta")
        self.button_control_layout.addWidget(self.end_meeting_cta)
        self.video_layout.addLayout(self.button_control_layout, 3, 1, 1, 3)
        self.meeting_layout.addLayout(self.video_layout)
        self.stackedWidget = QStackedWidget(parent=self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stackedWidget.sizePolicy().hasHeightForWidth()
        )
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QSize(200, 0))
        self.stackedWidget.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n" "color: rgb(0, 0, 0);"
        )
        self.stackedWidget.setObjectName("stackedWidget")
        self.Participants = QWidget()
        self.Participants.setObjectName("Participants")
        self.participants_page_title = QLabel(parent=self.Participants)
        self.participants_page_title.setGeometry(QRect(20, 30, 161, 16))
        self.participants_page_title.setObjectName("participants_page_title")
        self.stackedWidget.addWidget(self.Participants)
        self.Chat = QWidget()
        self.Chat.setObjectName("Chat")
        self.chat_page_title = QLabel(parent=self.Chat)
        self.chat_page_title.setGeometry(QRect(10, 20, 181, 16))
        self.chat_page_title.setObjectName("chat_page_title")
        self.stackedWidget.addWidget(self.Chat)
        self.meeting_layout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.end_meeting_cta.clicked.connect(MainWindow.close)  # type: ignore
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Participant_Video"))
        self.label_3.setText(_translate("MainWindow", "Participant_Video"))
        self.label_5.setText(_translate("MainWindow", "Participant_Video"))
        self.label.setText(_translate("MainWindow", "Participant_Video"))
        self.label_2.setText(_translate("MainWindow", "Participant_Video"))
        self.label_4.setText(_translate("MainWindow", "Participant_Video"))
        self.participants_cta.setText(_translate("MainWindow", "Participants"))
        self.chat_cta.setText(_translate("MainWindow", "Chat"))
        self.end_meeting_cta.setText(_translate("MainWindow", "End Meeting"))
        self.participants_page_title.setText(_translate("MainWindow", "Participants"))
        self.chat_page_title.setText(_translate("MainWindow", "Chat"))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MeetingPage()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
