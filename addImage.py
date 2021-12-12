from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import sys

from skimage.util.dtype import img_as_bool
import capture


class AddImage(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddImage, self).__init__()
        loadUi('addImage.ui', self)
        self.btnInput.clicked.connect(self.OpenFileDialog)
        self.txtLabel.setPlaceholderText("Nhap cac ky tu lien ke")
        self.btnAdd.clicked.connect(self.Add)

    def Add(self):
        label = self.txtLabel.toPlainText()
        if(capture.AddFace(img, label)):
            self.lbStatus.setText("Thêm hình ảnh thành công!")
        else:
            self.lbStatus.setText("Thêm hình ảnh thất bại!")

    def OpenFileDialog(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        # Get path of filename
        global img
        img = filename[0]
        qpixmap = QPixmap(
            img)
        self.lbImg.setPixmap(qpixmap)


app = QtWidgets.QApplication(sys.argv)
fAddImage = AddImage()
fAddImage.show()
app.exec()
