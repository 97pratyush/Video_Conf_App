from PySide6 import QtGui
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
)
from PySide6.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from Dashboard.join_meeting import JoinMeetingDialog
from Dashboard.meeting_info import MeetingInfoDialog
from api_requests import create_meeting
from app_state import state, on
from style import create_meeting_cta_style, join_meeting_cta_style
import Dashboard.resources

class DashboardPage(QWidget):
    def __init__(self, user_id, name, parent=None):
        super(DashboardPage, self).__init__(parent)

        self.user_details = {"id": user_id, "name": name}

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem)
        
        self.user_icon_cta = QPushButton(parent=self)
        self.user_icon_cta.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/Icons/DashboardIcons/user.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.user_icon_cta.clicked.connect(self.change_user_menu_visibility)
        self.user_icon_cta.setIcon(icon)
        self.user_icon_cta.setIconSize(QSize(50, 50))
        self.user_icon_cta.setFlat(True)
        self.user_icon_cta.setObjectName("user_icon_cta")
        self.horizontalLayout_2.addWidget(self.user_icon_cta)
        
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        
        self.welcome_label = QLabel(f"Welcome, {self.user_details['name']}", parent=self)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.welcome_label.sizePolicy().hasHeightForWidth())
        self.welcome_label.setSizePolicy(sizePolicy)
        self.welcome_label.setMinimumSize(QSize(0, 200))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        self.welcome_label.setFont(font)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setObjectName("label")
        self.verticalLayout.addWidget(self.welcome_label)
        
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QSpacerItem(
            100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.create_meeting_cta = QPushButton("Create a meeting", parent=self)
        self.create_meeting_cta.setStyleSheet(create_meeting_cta_style)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.create_meeting_cta.clicked.connect(self.start_meeting)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.create_meeting_cta.sizePolicy().hasHeightForWidth()
        )
        self.create_meeting_cta.setSizePolicy(sizePolicy)
        self.create_meeting_cta.setMinimumSize(QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.create_meeting_cta.setFont(font)
        self.create_meeting_cta.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.create_meeting_cta)
        
        self.join_meeting_cta = QPushButton("Join meeting", parent=self)
        self.join_meeting_cta.clicked.connect(self.join_meeting)
        self.join_meeting_cta.setStyleSheet(join_meeting_cta_style)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.join_meeting_cta.sizePolicy().hasHeightForWidth()
        )
        self.join_meeting_cta.setSizePolicy(sizePolicy)
        self.join_meeting_cta.setMinimumSize(QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.join_meeting_cta.setFont(font)
        self.join_meeting_cta.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.join_meeting_cta)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        
        spacerItem3 = QSpacerItem(
            100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        
        self.user_menu_container = QWidget(parent=self)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.user_menu_container.sizePolicy().hasHeightForWidth()
        )
        self.user_menu_container.setSizePolicy(sizePolicy)
        self.user_menu_container.setMinimumSize(QSize(200, 0))
        self.user_menu_container.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.user_menu_container.setObjectName("user_menu_container")
        state.is_user_menu_visible = False
        self.verticalLayout_4 = QVBoxLayout(self.user_menu_container)
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        spacerItem5 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.verticalLayout_4.addItem(spacerItem5)
        
        self.user_name_label = QLabel(f"{self.user_details['name']}", parent=self.user_menu_container)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        self.user_name_label.setFont(font)
        self.user_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_name_label.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.user_name_label)
        
        spacerItem6 = QSpacerItem(
            20, 470, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout_4.addItem(spacerItem6)
        
        self.logout_cta = QPushButton("Logout", parent=self.user_menu_container)
        self.logout_cta.clicked.connect(lambda: state.update(is_logged_in=False))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.logout_cta.setFont(font)
        icon1 = QtGui.QIcon()
        
        icon1.addPixmap(
            QtGui.QPixmap(":/Icons/DashboardIcons/log-out.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.logout_cta.setIcon(icon1)
        self.logout_cta.setIconSize(QSize(20, 20))
        self.logout_cta.setFlat(True)
        self.logout_cta.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.logout_cta)
        self.horizontalLayout.addWidget(self.user_menu_container)

    def change_user_menu_visibility(self):
        state.is_user_menu_visible = not state.is_user_menu_visible

    @on('state.is_user_menu_visible')
    def on_user_menu_visibility_change(self):
        self.user_menu_container.setVisible(state.is_user_menu_visible)

    def start_meeting(self):
        response = create_meeting(self.user_details['id'])
        
        if response.status_code == 200:
            state.in_meeting = True
            meeting_id = response.json()['meetingId']
            print("Meeting Id: ", meeting_id)
            self.meeting_dialog = MeetingInfoDialog(self.user_details, meeting_id)
            self.meeting_dialog.show()

    def join_meeting(self):
        self.join_meeting_dialog = JoinMeetingDialog(self.user_details)
        self.join_meeting_dialog.show()

    @on('state.in_meeting')
    def on_meeting_status_change(self):
        print(f"Is user in meeting: {state.in_meeting}")
        self.create_meeting_cta.setDisabled(state.in_meeting)
        self.join_meeting_cta.setDisabled(state.in_meeting)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = DashboardPage()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
