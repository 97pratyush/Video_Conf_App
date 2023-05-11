from PySide6 import QtGui
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from Meeting.chat import ChatScreen
from Meeting.participants import ParticipantScreen
from Meeting.socket_client import SocketClient
from constant import *
from ffpyplayer.player import MediaPlayer
from Streaming.receive_stream import ReceiveStream
import time, json
import Meeting.resources

user_stream_player : MediaPlayer = None

class MeetingPage(object):
    def __init__(self, user_details, meeting_id) -> None:
        self.user_details = user_details
        self.user_id = user_details['id']
        self.user_name = user_details['name']
        self.meeting_id = int(meeting_id)
        self.participants_info = dict()
        self.positions = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
    
        self.socket_client = SocketClient(meeting_id, user_details['id'], user_details['name'])
        self.socket_client.message_received.connect(self.receive_participants)
        self.subscribeToParticpants()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1191, 691)        
        MainWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n" "color: rgb(255, 255, 255);"
        )
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.meeting_layout = QHBoxLayout(self.centralwidget)
        self.meeting_layout.setContentsMargins(0, 0, 0, 0)
        self.meeting_layout.setSpacing(0)
        self.meeting_layout.setObjectName("horizontalLayout")

        self.video_container = QWidget(parent=self.centralwidget)
        # self.video_container.setGeometry(QRect(0, 0, 951, 621))
        self.video_container.setStyleSheet("background-color: blue;")
        self.video_container.setObjectName("video_container")

        self.video_tiles_layout = QGridLayout(self.video_container)
        self.video_tiles_layout.setContentsMargins(0, 0, 0, 0)
        self.video_tiles_layout.setObjectName("video_tiles_layout")

        ########################## Video Labels ##########################
        self.self_video = QLabel(parent=self.video_container)
        self.self_video.setScaledContents(True)
        self.self_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.self_video.setObjectName("self_video")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_video.sizePolicy().hasHeightForWidth()
        )                                    
        self.video_tiles_layout.addWidget(self.self_video)
        self.participants_info[str(self.user_id)] = {'label': self.self_video, 'name': self.user_name}
        
        # self.label_5 = QLabel("Label 2",parent=self.centralwidget)
        # self.label_5.setScaledContents(False)
        # self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_5.setObjectName("label_5")
        # self.label_5.setStyleSheet(
        #     "border-color: rgb(255, 255, 255);\n" 
        #     "background-color: rgb(255, 255, 255);"
        # )
        # self.video_tiles_layout.addWidget(self.label_5, 0, 1, 1, 1)

        # self.label_6 = QLabel(parent=self.centralwidget)
        # self.label_6.setScaledContents(False)
        # self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_6.setObjectName("label_6")
        # self.video_tiles_layout.addWidget(self.label_6, 0, 3, 1, 1)

        # self.label_4 = QLabel(parent=self.centralwidget)
        # self.label_4.setScaledContents(False)
        # self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_4.setObjectName("label_4")
        # self.video_tiles_layout.addWidget(self.label_4, 1, 1, 1, 1)        
        
        # self.label_3 = QLabel(parent=self.centralwidget)
        # self.label_3.setScaledContents(False)
        # self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label_3.setObjectName("label_3")
        # self.video_tiles_layout.addWidget(self.label_3, 1, 2, 1, 1)
        
        # self.label = QLabel(parent=self.centralwidget)
        # self.label.setScaledContents(False)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label.setObjectName("label")
        # self.video_tiles_layout.addWidget(self.label, 1, 3, 1, 1)
        ##################################################################

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
        self.participants_cta.clicked.connect(self.show_participants)
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
        self.chat_cta.clicked.connect(self.show_chat)
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
        self.end_meeting_cta.setMinimumSize(QSize(110, 0))
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
        self.video_tiles_layout.addLayout(self.button_control_layout, 3, 1, 1, 3)
        # self.meeting_layout.addLayout(self.video_tiles_layout)
        self.meeting_layout.addWidget(self.video_container)

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
        
        self.participants_page = ParticipantScreen()
        self.participants_page.setObjectName("Participants")
        # self.participants_page_title = QLabel(parent=self.participants_page)
        # self.participants_page_title.setGeometry(QRect(20, 30, 161, 16))
        # self.participants_page_title.setObjectName("participants_page_title")
        self.stackedWidget.addWidget(self.participants_page)
        
        self.chat_page = ChatScreen(self.user_details, self.meeting_id, self.socket_client)
        self.chat_page.setObjectName("Chat")
        # self.chat_page_title = QLabel(parent=self.chat_page)
        # self.chat_page_title.setGeometry(QRect(10, 20, 181, 16))
        # self.chat_page_title.setObjectName("chat_page_title")
        self.stackedWidget.addWidget(self.chat_page)

        self.meeting_layout.addWidget(self.stackedWidget)        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.end_meeting_cta.clicked.connect(MainWindow.close)  # type: ignore
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"{self.user_name} - Meeting ({self.meeting_id})"))
        self.self_video.setText(_translate("MainWindow", f"{self.user_name}"))
        # self.label_6.setText(_translate("MainWindow", "Participant_Video"))
        # self.label_3.setText(_translate("MainWindow", "Participant_Video"))
        # self.label_5.setText(_translate("MainWindow", "Participant_Video"))
        # self.label.setText(_translate("MainWindow", "Participant_Video"))        
        # self.label_4.setText(_translate("MainWindow", "Participant_Video"))
        self.participants_cta.setText(_translate("MainWindow", "Participants"))
        self.chat_cta.setText(_translate("MainWindow", "Chat"))
        self.end_meeting_cta.setText(_translate("MainWindow", "End Meeting"))

    def show_participants(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_chat(self):
        self.stackedWidget.setCurrentIndex(1)

    def subscribeToParticpants(self):
        time.sleep(2)
        if self.socket_client.get_connection_state():
            print("Connected to participants list")
            subscriptionInfo = {"type": f'{PARTICIPANTS_TOPIC}'}
            self.socket_client.send_message(subscriptionInfo)
        else:
            print("Not connected to participants list")
        
    def receive_participants(self, data):
        try:
            if data["type"] == "participantListUpdated":
                self.check_updated_participants(data["participantList"])
                pass
        except Exception as e:
            print(e)

    def check_updated_participants(self, participant_list):
        
            print("Checking updated participants", participant_list)
            print("Participant info", self.participants_info)
            try:
                # Add new participants
                for data in participant_list:
                    participant = json.loads(data)
                    id = participant["id"]
                    name = participant["name"]
                    if not self.participants_info.keys().__contains__(id):
                        print("New participant found", id, name)
                        self.participants_info[id] = {}
                        self.participants_info[id]["name"] = name
                        print("pos", len(self.participants_info)-2)
                        self.addLabel(id, len(self.participants_info)-2)
                        self.display_stream(id)
            except Exception as e:
                print("Exception occured while adding participants :", e)

            # Remove participants
            try:
                print('here1')
                existing_ids = self.getParticipantIds(participant_list)
                user_to_remove = []
                print('existing_ids', existing_ids)
                print('self.participants_info.keys()', self.participants_info.keys())
                for id in self.participants_info.keys():
                    print('id', id)
                    if not existing_ids.__contains__(id):
                        print("Participant left", id)
                        self.participants_info[id]["stream"].stop()
                        self.participants_info[id]["label"].hide()
                        user_to_remove.append(id)
                print('here2')

                for id in user_to_remove:
                    self.participants_info.pop(id)

            except Exception as e:
                print("Exception occured while removing participants :", e)

    
    def getParticipantIds(self, participantList):
        participantIds = []
        for data in participantList:
            participant = json.loads(data)
            participantIds.append(participant["id"])
        return participantIds

    def display_stream(self, user_id):
        try:
            url = f'{RTMP_URL}/{self.meeting_id}_{user_id}'
            self.participants_info[user_id]["stream"] = ReceiveStream(url, user_id)
            self.participants_info[user_id]["stream"].participant_frame_changed.connect(self.on_frame_changed)
            self.participants_info[user_id]["stream"].start()

        except Exception as e:
            print("Exception occured while receiving stream :", e)

    def on_frame_changed(self, pixmap, id):
        # print("pixmap",pixmap)
        # print("id",id)
        # # Change label for each participant
        self.participants_info[id]["label"].setPixmap(pixmap)
        

    def addLabel(self, id, pos):
        self.participants_info[id]["label"] = QLabel(self.participants_info[id]["name"], parent=self.centralwidget)
        # self.participants_info[id]["label"].setStyleSheet(
        #     "color: rgb(255, 255, 255);"
        # )
        self.participants_info[id]["label"].setScaledContents(True)
        self.participants_info[id]["label"].setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_position = self.positions[pos]
        self.video_tiles_layout.addWidget(self.participants_info[id]["label"], video_position[0], video_position[1], video_position[2], video_position[3])


# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = MeetingPage()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec())
