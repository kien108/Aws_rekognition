import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from detectFaceUI import Ui_MainWindow
import capture
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

window2 = None


class DetectFace(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(DetectFace, self).__init__(parent)
        self.setupUi(self)

        self.btnDetect.clicked.connect(self.DetectingFace)
        self.btnInput.clicked.connect(self.OpenFileDialog)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Bạn có chắc mún tắt hông?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

    def DetectingFace(self):
        isMatch, path, name = capture.Detect(img)
        qpixmap = QPixmap(
            path)
        self.lbImg.setPixmap(qpixmap)
        status = ""
        if (isMatch):
            status = "Nhận diện thành công, đây chính là: " + name
        else:
            status = "Nhận diện thất bại"

        self.lbStatus.setText(status)

    def OpenFileDialog(self):
        self.lbStatus.setText("")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        print(filename)
        # Get path of filename
        global img
        img = filename[0]
        print(img)
        qpixmap = QPixmap(
            img)
        self.lbImg.setPixmap(qpixmap)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = DetectFace()
    w.show()
    sys.exit(app.exec_())
