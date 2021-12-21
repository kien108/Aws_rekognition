from PyQt5 import QtCore, QtGui, QtWidgets
from ConvertUIToPython import menuUI
import addImage
import detectFace

addForm = None
detectForm = None


class Menu(QtWidgets.QMainWindow, menuUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.setupUi(self)
        self.btnAddFace.clicked.connect(self.OpenAddFaceForm)

        self.btnDetect.clicked.connect(self.OpenDetectForm)

    def OpenDetectForm(self):
        global detectForm
        if detectForm is None:
            detectForm = detectFace.DetectFace()
        detectForm.show()

    def OpenAddFaceForm(self):
        global addForm
        if addForm is None:
            addForm = addImage.AddImage()
        addForm.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Menu()
    w.show()
    sys.exit(app.exec_())
