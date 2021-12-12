from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import sys
import capture


class AddImage(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddImage, self).__init__()
        loadUi('menu.ui', self)
        self.btnAddFace.clicked.connect(self.OpenAddFaceForm)
        self.btnDetect.clicked.connect(self.OpenDetectForm)

    def OpenAddFaceForm(self):
        import addImage

    def OpenDetectForm(self):
        import faceDetect

        # Mở form
app = QtWidgets.QApplication(sys.argv)
fMenu = AddImage()
fMenu.show()
app.exec()
