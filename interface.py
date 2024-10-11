# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(640, 794)
        self.MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel, QTextEdit, QLineEdit, QPushButton {
                border: none;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
            QLabel {
                background-color: #e0e0e0;
            }
            QTextEdit {
                background-color: #f5f5f5;
            }
            QLineEdit {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        font = QtGui.QFont("Segoe UI", 10)

        # Set window flags to make it always on top
        self.MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(20)

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setMinimumSize(QtCore.QSize(400, 400))
        self.image_label.setStyleSheet("border-radius: 10px;")
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        self.conversation = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conversation.sizePolicy().hasHeightForWidth())
        self.conversation.setSizePolicy(sizePolicy)
        self.conversation.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.conversation.setStyleSheet("border-radius: 10px;")
        self.conversation.setMinimumSize(QtCore.QSize(0, 100))
        self.conversation.setReadOnly(True)
        self.conversation.setObjectName("conversation")
        self.verticalLayout.addWidget(self.conversation)

        self.entry = QtWidgets.QLineEdit(self.centralwidget)
        self.entry.setMinimumSize(QtCore.QSize(0, 50))
        self.entry.setStyleSheet("border-radius: 10px;")
        self.entry.setObjectName("entry")
        self.entry.setPlaceholderText("Type your message here...")
        self.entry.setFocus()
        self.entry.setFont(font)
        self.verticalLayout.addWidget(self.entry)

        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setObjectName("send_button")
        
        self.verticalLayout.addWidget(self.send_button)
        # Set font to Segoe UI, 10pt
        self.conversation.setFont(font)
        self.loading_label = QtWidgets.QLabel(self.centralwidget)
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text
        self.loading_label.setText("")
        self.loading_label.setObjectName("loading_label")
        self.loading_label.setStyleSheet("color: #007BFF;")
        self.loading_label.setFont(font)    
        
        
        self.verticalLayout.addWidget(self.loading_label)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set default position to top-right corner of the screen
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        x = screen_geometry.width() - self.MainWindow.width()
        y = 0
        self.MainWindow.move(x, y)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "sHashtagAI"))
        self.send_button.setText(_translate("MainWindow", "Send"))

