# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meeting_pageui.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QWidget)
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(748, 554)
        MainWindow.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 3, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.participants_cta = QPushButton(self.centralwidget)
        self.participants_cta.setObjectName(u"participants_cta")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.participants_cta.sizePolicy().hasHeightForWidth())
        self.participants_cta.setSizePolicy(sizePolicy)
        self.participants_cta.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.participants_cta.setFont(font)
        self.participants_cta.setCursor(QCursor(Qt.PointingHandCursor))
        self.participants_cta.setLayoutDirection(Qt.LeftToRight)
        self.participants_cta.setAutoFillBackground(False)
        self.participants_cta.setStyleSheet(u"padding:5px;\n"
"border-radius:5px;")
        icon = QIcon()
        icon.addFile(u":/Icons/Icons/conference-multi-size.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.participants_cta.setIcon(icon)
        self.participants_cta.setIconSize(QSize(30, 30))
        self.participants_cta.setFlat(True)

        self.horizontalLayout_3.addWidget(self.participants_cta)

        self.chat_cta = QPushButton(self.centralwidget)
        self.chat_cta.setObjectName(u"chat_cta")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chat_cta.sizePolicy().hasHeightForWidth())
        self.chat_cta.setSizePolicy(sizePolicy1)
        self.chat_cta.setMinimumSize(QSize(100, 0))
        self.chat_cta.setFont(font)
        self.chat_cta.setCursor(QCursor(Qt.PointingHandCursor))
        self.chat_cta.setStyleSheet(u"padding:5px;\n"
"border-radius:5px;")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/Icons/chat-2-multi-size.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.chat_cta.setIcon(icon1)
        self.chat_cta.setIconSize(QSize(30, 30))
        self.chat_cta.setFlat(True)

        self.horizontalLayout_3.addWidget(self.chat_cta)

        self.end_meeting_cta = QPushButton(self.centralwidget)
        self.end_meeting_cta.setObjectName(u"end_meeting_cta")
        sizePolicy1.setHeightForWidth(self.end_meeting_cta.sizePolicy().hasHeightForWidth())
        self.end_meeting_cta.setSizePolicy(sizePolicy1)
        self.end_meeting_cta.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.end_meeting_cta.setFont(font1)
        self.end_meeting_cta.setCursor(QCursor(Qt.PointingHandCursor))
        self.end_meeting_cta.setStyleSheet(u"padding:5px;\n"
"border-radius:5px;\n"
"background-color: rgb(170, 0, 0);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.end_meeting_cta)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 1, 1, 3)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy2)
        self.stackedWidget.setMinimumSize(QSize(200, 0))
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.Participants = QWidget()
        self.Participants.setObjectName(u"Participants")
        self.participants_page_title = QLabel(self.Participants)
        self.participants_page_title.setObjectName(u"participants_page_title")
        self.participants_page_title.setGeometry(QRect(20, 30, 161, 16))
        self.stackedWidget.addWidget(self.Participants)
        self.Chat = QWidget()
        self.Chat.setObjectName(u"Chat")
        self.chat_page_title = QLabel(self.Chat)
        self.chat_page_title.setObjectName(u"chat_page_title")
        self.chat_page_title.setGeometry(QRect(10, 20, 181, 16))
        self.stackedWidget.addWidget(self.Chat)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.end_meeting_cta.clicked.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Participant_Video", None))
        self.participants_cta.setText(QCoreApplication.translate("MainWindow", u"Participants", None))
        self.chat_cta.setText(QCoreApplication.translate("MainWindow", u"Chat", None))
        self.end_meeting_cta.setText(QCoreApplication.translate("MainWindow", u"End Meeting", None))
        self.participants_page_title.setText(QCoreApplication.translate("MainWindow", u"Participants", None))
        self.chat_page_title.setText(QCoreApplication.translate("MainWindow", u"Chat", None))
    # retranslateUi

