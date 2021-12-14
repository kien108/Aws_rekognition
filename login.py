from PyQt5.QtGui import QPixmap
import capture
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import captureUI
import menu
from unidecode import unidecode


window2 = None


def Login():

    global window2
    print(unidecode("Xác thực danh tính thành công"))
    if (unidecode(fLogin.lbStatus.text()) == unidecode("Xác thực danh tính thành công")):
        MainWindow.close()
        if window2 is None:
            window2 = menu.Menu()
        window2.show()
    else:
        status = 'Vui lòng chụp lại ảnh khác'
        fLogin.lbStatus.setText(status)


def ReCapture():
    isCapture, isMatch, img, label = LoadCamera()
    LoadForm(isCapture, isMatch, img, label)


def LoadCamera():
    isCapture = True
    isMatch = False
    # Default not capture
    img = "D:\HK1-Năm 3\Cloud Computing\Capture\imgs\error.jpg"
    label = ""

    path_img = capture.Capture()
    if (path_img == ""):
        isCapture = False
    else:
        isMatch, img, label = capture.Authen(path_img)
    return isCapture, isMatch, img, label


def LoadForm(isCapture, isMatch, img, label):
    global status
    if (isCapture):
        status = 'Xác thực danh tính thành công' if isMatch else 'Xác thực danh tính không thành công'
    else:
        status = 'Oops! Vui lòng chụp ảnh để xác thực'

    name = 'Xin chào ' + label if label != "" else ""

    fLogin.lbStatus.setText(status)
    fLogin.lbName.setText(name)

    print(fLogin.btnReCapture.text)

    qpixmap = QPixmap(
        img)
    fLogin.lbImg.setPixmap(qpixmap)


# Open form
isCapture, isMatch, img, label = LoadCamera()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
fLogin = captureUI.Ui_MainWindow()
fLogin.setupUi(MainWindow)
LoadForm(isCapture, isMatch, img, label)
# Open Add Face form
fLogin.btnReCapture.clicked.connect(ReCapture)
# Open Detect Face form
fLogin.btnLogin.clicked.connect(Login)
MainWindow.show()
sys.exit(app.exec_())
