# -*- coding: utf-8 -*-

import sys
import warnings
from multiprocessing import freeze_support

from PySide2 import QtWidgets

import GUI.UI_Main

if __name__ == "__main__":
    with warnings.catch_warnings(record=True) as w:
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
