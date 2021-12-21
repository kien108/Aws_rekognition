# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'facedetect.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(837, 675)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbImg = QtWidgets.QLabel(self.centralwidget)
        self.lbImg.setGeometry(QtCore.QRect(30, 50, 771, 461))
        self.lbImg.setStyleSheet("text-align: center")
        self.lbImg.setText("")
        self.lbImg.setScaledContents(True)
        self.lbImg.setObjectName("lbImg")
        self.btnInput = QtWidgets.QPushButton(self.centralwidget)
        self.btnInput.setGeometry(QtCore.QRect(30, 10, 131, 31))
        self.btnInput.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnInput.setObjectName("btnInput")
        self.lbStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbStatus.setGeometry(QtCore.QRect(230, 10, 551, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lbStatus.setFont(font)
        self.lbStatus.setStyleSheet("color: green;\n"
"font-size: 20px;")
        self.lbStatus.setText("")
        self.lbStatus.setObjectName("lbStatus")
        self.btnDetect = QtWidgets.QPushButton(self.centralwidget)
        self.btnDetect.setGeometry(QtCore.QRect(250, 550, 311, 41))
        self.btnDetect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDetect.setStyleSheet("background-color: #fa5230;\n"
"border: 1px solid #ccc;\n"
"color: #fff;\n"
"font-size: 18px;\n"
"border-radius: 6px;")
        self.btnDetect.setObjectName("btnDetect")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 837, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnInput.setText(_translate("MainWindow", "Choose File:"))
        self.btnDetect.setText(_translate("MainWindow", "FACE DETECTION"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())