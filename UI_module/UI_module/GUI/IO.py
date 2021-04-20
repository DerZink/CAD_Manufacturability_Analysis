import sys

# ,QApplication, QWidget,
from PySide2.QtWidgets import QInputDialog, QLineEdit, QFileDialog

# from PyQt5.QtGui import QIcon


def openFileNameDialog(self):
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileNames(
        self.centralwidget,
        "QFileDialog.getOpenFileName()",
        "",
        "All Files (*);;Python Files (*.py)",
        options=options,
    )
    # if fileName:
    #     print(fileName)
    # for i in fileName:
    #     print(i)


def openFileNamesDialog(self):
    options = QFileDialog.Options()

    options |= QFileDialog.DontUseNativeDialog
    # files, _ = QFileDialog.getOpenFileNames(self.centralwidget,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
    files = str(
        QFileDialog.getExistingDirectory(self.centralwidget, "Select Directory")
    )
    # if files:
    #     print(files)


def saveFileDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(
        self.centralwidget,
        "QFileDialog.getSaveFileName()",
        "",
        "All Files (*);;Text Files (*.txt)",
        options=options,
    )
    # if fileName:
    #     print(fileName)


# test()
