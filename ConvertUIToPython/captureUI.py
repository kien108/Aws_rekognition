# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'capture.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 776)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbImg = QtWidgets.QLabel(self.centralwidget)
        self.lbImg.setGeometry(QtCore.QRect(20, 100, 741, 541))
        self.lbImg.setText("")
        self.lbImg.setPixmap(QtGui.QPixmap("imgs/error.jpg"))
        self.lbImg.setScaledContents(True)
        self.lbImg.setObjectName("lbImg")
        self.lbStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbStatus.setGeometry(QtCore.QRect(170, 10, 511, 41))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbStatus.setFont(font)
        self.lbStatus.setText("")
        self.lbStatus.setObjectName("lbStatus")
        self.lbName = QtWidgets.QLabel(self.centralwidget)
        self.lbName.setGeometry(QtCore.QRect(260, 50, 511, 41))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbName.setFont(font)
        self.lbName.setText("")
        self.lbName.setObjectName("lbName")
        self.btnLogin = QtWidgets.QPushButton(self.centralwidget)
        self.btnLogin.setGeometry(QtCore.QRect(380, 660, 181, 51))
        self.btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLogin.setObjectName("btnLogin")
        self.btnReCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnReCapture.setGeometry(QtCore.QRect(180, 660, 181, 51))
        self.btnReCapture.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReCapture.setAutoFillBackground(False)
        self.btnReCapture.setObjectName("btnReCapture")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 26))
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
        self.btnLogin.setText(_translate("MainWindow", "????NG NH???P"))
        self.btnReCapture.setText(_translate("MainWindow", "CH???P ???NH L???I"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
