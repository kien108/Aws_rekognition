from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from ConvertUIToPython import addImageUI
import capture as capture
from PyQt5.QtGui import QPixmap
window2 = None


class AddImage(QtWidgets.QMainWindow, addImageUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AddImage, self).__init__(parent)
        self.setupUi(self)

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
        self.lbStatus.setText("")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        # Get path of filename
        global img
        img = filename[0]
        qpixmap = QPixmap(
            img)
        self.lbImg.setPixmap(qpixmap)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Bạn có chắc mún tắt hông?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

    def Close(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = AddImage()
    w.show()
    sys.exit(app.exec_())
