# -*- coding: utf-8 -*-

import sys
from multiprocessing import freeze_support
from PySide2 import QtWidgets
import time

import GUI.UI_Main

if __name__ == "__main__":
    freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUI.UI_Main.Ui_MainWindow()
    # if ui.outputFile.exists():
    #     ui.outputFile.copy(
    #         ui.outputfilePath.replace(".txt", "")
    #         + time.asctime(time.localtime()).replace(" ", "_").replace(":", "")
    #         + ".txt"
    #     )
    #     ui.outputFile.remove()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
