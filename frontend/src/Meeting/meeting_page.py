# Form implementation generated from reading ui file 'meeting_design.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtGui
from PySide6.QtCore import Qt, QRect, QCoreApplication, QMetaObject
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QFrame,
    QStackedWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QSpacerItem
)
from Meeting.chat import ChatScreen
from Meeting.socket_client import SocketClient
from constant import PARTICIPANTS_TOPIC
import time, json

class MeetingPage(object):
    def __init__(self, user_details, meeting_id) -> None:
        self.user_details = user_details
        self.user_id = user_details['id']
        self.user_name = user_details['name']
        self.meeting_id = int(meeting_id)

        self.socket_client = SocketClient(meeting_id, user_details['id'], user_details['name'])
        self.socket_client.message_received.connect(self.receive_participants)
        self.subscribeToParticpants()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1191, 691)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
            "background-color: #313a46;\n" "color: rgb(255, 255, 255);"
        )
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.meeting_container = QWidget(parent=self.centralwidget)
        self.meeting_container.setGeometry(QRect(0, 0, 951, 691))
        self.meeting_container.setStyleSheet("")
        self.meeting_container.setObjectName("meeting_container")
        
        self.video_container = QWidget(parent=self.meeting_container)
        self.video_container.setGeometry(QRect(0, 0, 951, 621))
        self.video_container.setStyleSheet("")
        self.video_container.setObjectName("video_container")
        self.gridLayout = QGridLayout(self.video_container)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        # Video Display labels
        self.self_video = QLabel(parent=self.video_container)
        self.self_video.setStyleSheet(
            "border-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);"
        )
        self.self_video.setFrameShape(QFrame.Shape.Box)
        self.self_video.setScaledContents(True)
        self.self_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.self_video.setObjectName("self")
        self.gridLayout.addWidget(self.self_video, 0, 0, 2, 1)
        self.participant_1 = QLabel(parent=self.video_container)
        self.participant_1.setStyleSheet(
            "border-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);"
        )
        self.participant_1.setFrameShape(QFrame.Shape.Box)
        self.participant_1.setScaledContents(True)
        self.participant_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.participant_1.setObjectName("participant_1")
        self.gridLayout.addWidget(self.participant_1, 0, 1, 1, 1)
        self.participant_2 = QLabel(parent=self.video_container)
        self.participant_2.setStyleSheet(
            "border-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);"
        )
        self.participant_2.setFrameShape(QFrame.Shape.Box)
        self.participant_2.setScaledContents(True)
        self.participant_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.participant_2.setObjectName("participant_2")
        self.gridLayout.addWidget(self.participant_2, 1, 1, 1, 1)
        
        self.control_container = QWidget(parent=self.meeting_container)
        self.control_container.setGeometry(QRect(0, 620, 961, 71))
        self.control_container.setStyleSheet("")
        self.control_container.setObjectName("control_container")
        self.horizontalLayout = QHBoxLayout(self.control_container)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(
            358,
            38,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem)
        self.participants_cta = QPushButton(parent=self.control_container)
        self.participants_cta.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);"
        )
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/Icons/conference-multi-size.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.participants_cta.setIcon(icon)
        self.participants_cta.setObjectName("participants_cta")
        self.horizontalLayout.addWidget(self.participants_cta)
        spacerItem1 = QSpacerItem(
            115,
            38,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.chat_cta = QPushButton(parent=self.control_container)
        self.chat_cta.setStyleSheet(
            "color: rgb(0, 0, 0);\n" "background-color: rgb(255, 255, 255);"
        )
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/Icons/chat-4-multi-size.ico"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.chat_cta.setIcon(icon1)
        self.chat_cta.setObjectName("chat_cta")
        self.horizontalLayout.addWidget(self.chat_cta)
        spacerItem2 = QSpacerItem(
            148,
            38,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem2)
        self.end_meeting = QPushButton(parent=self.control_container)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_meeting.sizePolicy().hasHeightForWidth())
        self.end_meeting.setSizePolicy(sizePolicy)
        self.end_meeting.setStyleSheet(
            "color: rgb(255, 255, 255);\n" "background-color: rgb(170, 0, 0);"
        )
        self.end_meeting.setObjectName("end_meeting")
        self.horizontalLayout.addWidget(self.end_meeting)
        self.stackedWidget = QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setGeometry(QRect(960, 0, 231, 691))
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stackedWidget.sizePolicy().hasHeightForWidth()
        )
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n" "color: rgb(0, 0, 0);"
        )
        self.stackedWidget.setObjectName("stackedWidget")
        self.chat_page = ChatScreen(self.user_details, self.meeting_id, self.socket_client)
        self.chat_page.setObjectName("chat_page")
        # self.chat_page_title = QLabel(parent=self.chat_page)
        # self.chat_page_title.setGeometry(QRect(38, 40, 151, 61))
        # self.chat_page_title.setObjectName("label")
        self.stackedWidget.addWidget(self.chat_page)
        self.participants_page = QWidget()
        self.participants_page.setObjectName("participants_page")
        self.participants_page_title = QLabel(parent=self.participants_page)
        self.participants_page_title.setGeometry(QRect(40, 30, 161, 71))
        self.participants_page_title.setObjectName("participants_page_title")
        self.stackedWidget.addWidget(self.participants_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
          # type: ignore
        self.chat_cta.clicked.connect(self.show_chat)
        self.participants_cta.clicked.connect(self.show_participants)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"{self.user_name} - Meeting ({self.meeting_id})"))
        self.self_video.setText(_translate("MainWindow", f"{self.user_name}"))
        self.participant_1.setText(_translate("MainWindow", "Participant 1"))
        self.participant_2.setText(_translate("MainWindow", "Participant 2"))
        self.participants_cta.setText(_translate("MainWindow", "Participants"))
        self.chat_cta.setText(_translate("MainWindow", "Chat"))
        self.end_meeting.setText(_translate("MainWindow", "End Meeting"))
        self.participants_page_title.setText(_translate("MainWindow", "Participants"))

    def show_participants(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_chat(self):
        self.stackedWidget.setCurrentIndex(0)

    def receive_participants(self, data):
        try:
            if data["type"] == "participantListUpdated":
                print(data)
            elif data["type"] == "newChatMessage":
                self.addNewChatMessage(data["sender"], data["message"])
        except Exception as e:
            print(e)

    def subscribeToParticpants(self):
        time.sleep(1)
        if self.socket_client.get_connection_state():
            print("Connected to participants list")
            subscriptionInfo = {"type": f'{PARTICIPANTS_TOPIC}'}
            self.socket_client.send_message(subscriptionInfo)
        else:
            print("Not connected to participants list")
        