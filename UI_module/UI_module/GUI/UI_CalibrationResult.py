# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\04_CalibrationResult.ui',
# licensing of 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\04_CalibrationResult.ui' applies.
#
# Created: Fri Jun 12 14:41:10 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_CalibrationResult(object):
    def setupUi(self, CalibrationResult):
        CalibrationResult.setObjectName("CalibrationResult")
        CalibrationResult.resize(1000, 750)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalibrationResult.sizePolicy().hasHeightForWidth())
        CalibrationResult.setSizePolicy(sizePolicy)
        CalibrationResult.setMinimumSize(QtCore.QSize(1000, 750))
        self.gridLayout = QtWidgets.QGridLayout(CalibrationResult)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 0, 2, 3, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(60, 15, 60, 15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(CalibrationResult)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 120))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_undo = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_undo.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_undo.setSizePolicy(sizePolicy)
        self.pushButton_undo.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_undo.setObjectName("pushButton_undo")
        self.gridLayout_3.addWidget(self.pushButton_undo, 1, 1, 1, 1)
        self.pushButton_save = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_save.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout_3.addWidget(self.pushButton_save, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 1, 4, 2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_4.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_4.addItem(spacerItem2, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(CalibrationResult)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(0, 5))
        self.line.setMaximumSize(QtCore.QSize(16777215, 5))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 0, 1, 1, 1)
        self.plot_Histogram = QtWidgets.QLabel(CalibrationResult)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_Histogram.sizePolicy().hasHeightForWidth()
        )
        self.plot_Histogram.setSizePolicy(sizePolicy)
        self.plot_Histogram.setMinimumSize(QtCore.QSize(600, 150))
        self.plot_Histogram.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_Histogram.setObjectName("plot_Histogram")
        self.gridLayout_4.addWidget(self.plot_Histogram, 1, 0, 1, 3)
        self.gridLayout.addLayout(self.gridLayout_4, 4, 0, 4, 1)
        self.tableView_Results = QtWidgets.QTableView(CalibrationResult)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableView_Results.sizePolicy().hasHeightForWidth()
        )
        self.tableView_Results.setSizePolicy(sizePolicy)
        self.tableView_Results.setMinimumSize(QtCore.QSize(0, 559))
        self.tableView_Results.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView_Results.setObjectName("tableView_Results")
        self.gridLayout.addWidget(self.tableView_Results, 2, 1, 1, 1)
        self.plot_Residual = QtWidgets.QLabel(CalibrationResult)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_Residual.sizePolicy().hasHeightForWidth()
        )
        self.plot_Residual.setSizePolicy(sizePolicy)
        self.plot_Residual.setMinimumSize(QtCore.QSize(600, 300))
        self.plot_Residual.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_Residual.setObjectName("plot_Residual")
        self.gridLayout.addWidget(self.plot_Residual, 0, 0, 3, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 1)

        self.retranslateUi(CalibrationResult)
        QtCore.QMetaObject.connectSlotsByName(CalibrationResult)

    def retranslateUi(self, CalibrationResult):
        CalibrationResult.setWindowTitle(
            QtWidgets.QApplication.translate("CalibrationResult", "Form", None, -1)
        )
        self.groupBox.setTitle(
            QtWidgets.QApplication.translate(
                "CalibrationResult", "Calibration", None, -1
            )
        )
        self.pushButton_undo.setText(
            QtWidgets.QApplication.translate("CalibrationResult", "Undo", None, -1)
        )
        self.pushButton_save.setText(
            QtWidgets.QApplication.translate("CalibrationResult", "Save", None, -1)
        )
        self.plot_Histogram.setText(
            QtWidgets.QApplication.translate(
                "CalibrationResult", "Placeholder_Histogram", None, -1
            )
        )
        self.plot_Residual.setText(
            QtWidgets.QApplication.translate(
                "CalibrationResult", "Placeholder_Plot", None, -1
            )
        )
