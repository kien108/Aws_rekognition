from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import sys
import capture


class FaceDetect(QtWidgets.QMainWindow):
    def __init__(self):
        super(FaceDetect, self).__init__()
        loadUi('facedetect.ui', self)
        self.btnDetect.clicked.connect(self.DetectFace)
        self.btnInput.clicked.connect(self.OpenFileDialog)

    def DetectFace(self):
        isMatch, path, name = capture.Authen(img)
        qpixmap = QPixmap(
            path)
        self.lbImg.setPixmap(qpixmap)

    def OpenFileDialog(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        # Get path of filename
        global img
        img = filename[0]
        qpixmap = QPixmap(
            img)
        self.lbImg.setPixmap(qpixmap)


# Mở form
app = QtWidgets.QApplication(sys.argv)
fFaceDetect = FaceDetect()
fFaceDetect.show()
app.exec()
