from PySide6 import QtGui
from PySide6.QtCore import Qt, QRect, QCoreApplication, QMetaObject, QSize
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLayout,
    QStackedWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QListWidgetItem
)
from Meeting.chat import ChatScreen
from Meeting.participants import ParticipantScreen
from Meeting.socket_client import SocketClient
from constant import *
from style import end_meeting_cta_style
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

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("verticalLayout")


        self.meeting_layout = QHBoxLayout(self.centralwidget)
        self.meeting_layout.setContentsMargins(0, 0, 0, 0)
        self.meeting_layout.setSpacing(0)
        self.meeting_layout.setObjectName("horizontalLayout")
        
        self.video_container = QWidget(self.centralwidget)
        self.video_container.setStyleSheet("")
        self.video_container.setObjectName("video_container")
        self.meeting_layout.addWidget(self.video_container)

        self.video_tiles_layout = QGridLayout(self.video_container)
        self.video_tiles_layout.setContentsMargins(0, 0, 0, 0)
        self.meeting_layout.setSpacing(0)
        self.video_tiles_layout.setObjectName("gridLayout")
        
        # Video Display labels
        self.self_video = QLabel(f"{self.user_name}", parent=self.video_container)
        self.self_video.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.self_video.setScaledContents(True)
        self.self_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.self_video.setObjectName("self")
        # self.video_tiles_layout.addWidget(self.self_video, 0, 0, 1, 1)
        self.participants_info[str(self.user_id)] = {'label': self.self_video, 'name': self.user_name}
        self.self_name_label = QLabel(f"{self.user_name}", parent=self.video_container)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_name_label.sizePolicy().hasHeightForWidth()
        )
        self.self_name_label.setSizePolicy(sizePolicy)

        self.participant_video_tile_layout = QVBoxLayout()
        self.participant_video_tile_layout.setContentsMargins(0, 0, 0, 0)
        self.participant_video_tile_layout.setSpacing(0)
        self.participant_video_tile_layout.setObjectName("video_tiles_vertical_layout")
        self.participant_video_tile_layout.addWidget(self.self_video)
        self.participant_video_tile_layout.addWidget(self.self_name_label)
        self.video_tiles_layout.addLayout(self.participant_video_tile_layout, 0, 0, 1, 1)
        
        self.control_container = QWidget(parent=self.centralwidget)
        self.control_container.setGeometry(QRect(0, 620, 961, 71))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.control_container.sizePolicy().hasHeightForWidth()
        )
        self.control_container.setSizePolicy(sizePolicy)
        self.control_container.setStyleSheet("")
        self.control_container.setObjectName("control_container")
        
        self.button_control_layout = QHBoxLayout(self.control_container)
        self.button_control_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.button_control_layout.setContentsMargins(10, 10, 10, 10)
        self.button_control_layout.setSpacing(10)
        self.button_control_layout.setObjectName("button_control_layout")
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.button_control_layout.addItem(spacerItem)

        #  Show participant page CTA
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

        self.vertical_layout.addWidget(self.video_container)
        self.vertical_layout.addWidget(self.control_container)
        self.meeting_layout.addLayout(self.vertical_layout)

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
        self.participants_page.participant_display.addItem(self.user_name)
        self.stackedWidget.addWidget(self.participants_page)
        
        self.chat_page = ChatScreen(self.user_details, self.meeting_id, self.socket_client)
        self.chat_page.setObjectName("Chat")
        self.stackedWidget.addWidget(self.chat_page)

        self.meeting_layout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.chat_cta.clicked.connect(self.show_chat)
        self.participants_cta.clicked.connect(self.show_participants)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"{self.user_name} - Meeting ({self.meeting_id})"))
        self.self_video.setText(_translate("MainWindow", f"{self.user_name}"))
        
        self.participants_cta.setText(_translate("MainWindow", "Participants"))
        self.chat_cta.setText(_translate("MainWindow", "Chat"))
        self.end_meeting_cta.setText(_translate("MainWindow", "End Meeting"))

    def show_participants(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_chat(self):
        self.stackedWidget.setCurrentIndex(1)

    def subscribeToParticpants(self):
        time.sleep(2)
        try:
            if self.socket_client.get_connection_state():
                subscriptionInfo = {"type": f'{PARTICIPANTS_TOPIC}'}
                self.socket_client.send_message(subscriptionInfo)
            else:
                print("Not connected to participants list")
        except Exception as e:
            print(e)
        
    def receive_participants(self, data):
        try:
            if data["type"] == "participantListUpdated":
                self.check_updated_participants(data["participantList"])
                pass
        except Exception as e:
            print(e)

    def check_updated_participants(self, participant_list):
        
            # print("Checking updated participants", participant_list)
            # print("Participant info", self.participants_info)
            try:
                # Add new participants
                for data in participant_list:
                    participant = json.loads(data)
                    id = participant["id"]
                    name = participant["name"]
                    if not self.participants_info.keys().__contains__(id):
                        # print("New participant found", id, name)
                        self.participants_info[id] = {}
                        self.participants_info[id]["name"] = name
                        # print("pos", len(self.participants_info)-2)
                        self.addLabel(id, len(self.participants_info)-2)

                        item = QListWidgetItem(f"{name}")
                        item.setTextAlignment(Qt.AlignLeft)                                            
                        sizeHint = QSize(item.sizeHint().width(), item.sizeHint().height()+5)
                        item.setSizeHint(sizeHint)
                        self.participants_page.participant_display.addItem(item)

                        self.display_stream(id)
            except Exception as e:
                print("Exception occured while adding participants :", e)

            # Remove participants
            try:
                existing_ids = self.getParticipantIds(participant_list)
                user_to_remove = []
                # print('existing_ids', existing_ids)
                # print('self.participants_info.keys()', self.participants_info.keys())
                for id in self.participants_info.keys():
                    # print('id', id)
                    if not existing_ids.__contains__(id):
                        # print("Participant left", id)
                        self.participants_page.participant_display.takeItem(self.participants_page.participant_display.row(self.participants_page.participant_display.findItems(self.participants_info[id]["name"], Qt.MatchExactly)[0]))
                        self.participants_info[id]["stream"].stop()
                        self.participants_info[id]["label"].hide()
                        user_to_remove.append(id)

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

        # Participant video label
        self.participants_info[id]["label"] = QLabel(self.participants_info[id]["name"], parent=self.video_container)
        self.participants_info[id]["label"].setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.participants_info[id]["label"].setScaledContents(True)
        self.participants_info[id]["label"].setObjectName(self.participants_info[id]["name"])
        self.participants_info[id]["label"].setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_positioon = self.positions[pos]
        
        # Participant name label
        self.participant_name_label = QLabel(self.participants_info[id]["name"], parent=self.video_container)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.participant_name_label.sizePolicy().hasHeightForWidth()
        )
        self.participant_name_label.setSizePolicy(sizePolicy)

        # Participant Video tile layout
        self.participant_video_tile_layout = QVBoxLayout()
        self.participant_video_tile_layout.setContentsMargins(0, 0, 0, 0)
        self.participant_video_tile_layout.setSpacing(0)
        self.participant_video_tile_layout.setObjectName("video_tiles_vertical_layout")
        self.participant_video_tile_layout.addWidget(self.participants_info[id]["label"])
        self.participant_video_tile_layout.addWidget(self.participant_name_label)
        self.video_tiles_layout.addLayout(self.participant_video_tile_layout, video_positioon[0], video_positioon[1], video_positioon[2], video_positioon[3])

        