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

from style import primary_cta_style, secondary_cta_style
import DashboardIcons


class DashboardPage(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n" "color: rgb(0, 0, 0);"
        )
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
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
        self.user_icon_cta = QPushButton(parent=self.centralwidget)
        self.user_icon_cta.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/Icons/DashboardIcons/user.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.user_icon_cta.setIcon(icon)
        self.user_icon_cta.setIconSize(QSize(30, 30))
        self.user_icon_cta.setFlat(True)
        self.user_icon_cta.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.user_icon_cta)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.label = QLabel(parent=self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(0, 200))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
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
        self.create_meeting_cta = QPushButton(parent=self.centralwidget)
        self.create_meeting_cta.setStyleSheet(primary_cta_style)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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
        self.create_meeting_cta.setStyleSheet(
            "background-color: rgb(0, 66, 197);\n" "color: rgb(255, 255, 255);"
        )
        self.create_meeting_cta.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.create_meeting_cta)
        self.join_meeting_cta = QPushButton(parent=self.centralwidget)
        self.join_meeting_cta.setStyleSheet(secondary_cta_style)
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
        self.user_menu_container = QWidget(parent=self.centralwidget)
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
        self.verticalLayout_4 = QVBoxLayout(self.user_menu_container)
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem5 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.verticalLayout_4.addItem(spacerItem5)
        self.user_name_label = QLabel(parent=self.user_menu_container)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.user_name_label.setFont(font)
        self.user_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_name_label.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.user_name_label)
        spacerItem6 = QSpacerItem(
            20, 470, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalLayout_4.addItem(spacerItem6)
        self.logout_cta = QPushButton(parent=self.user_menu_container)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.logout_cta.setFont(font)
        icon1 = QtGui.QIcon()
        icons = DashboardIcons
        icon1.addPixmap(
            QtGui.QPixmap(f"{icons}:log-out.svg"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.logout_cta.setIcon(icon1)
        self.logout_cta.setIconSize(QSize(20, 20))
        self.logout_cta.setFlat(True)
        self.logout_cta.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.logout_cta)
        self.horizontalLayout.addWidget(self.user_menu_container)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome, User_Name"))
        self.create_meeting_cta.setText(_translate("MainWindow", "Create a meeting"))
        self.join_meeting_cta.setText(_translate("MainWindow", "Join meeting"))
        self.user_name_label.setText(_translate("MainWindow", "User_Name"))
        self.logout_cta.setText(_translate("MainWindow", "Log Out"))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = DashboardPage()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
