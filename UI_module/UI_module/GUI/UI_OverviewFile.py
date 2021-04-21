# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\04_Arbeitsordner_lokal_sync\feasibility_analysis_integrateBokeh\feasibility_analysis\UI_module\UI_module\01_DatabaseOverview.ui',
# licensing of 'd:\04_Arbeitsordner_lokal_sync\feasibility_analysis_integrateBokeh\feasibility_analysis\UI_module\UI_module\01_DatabaseOverview.ui' applies.
#
# Created: Fri Mar 27 12:44:55 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_OverviewForm(object):
    def setupUi(self, OverviewForm):
        OverviewForm.setObjectName("OverviewForm")
        OverviewForm.resize(850, 670)
        OverviewForm.setMinimumSize(QtCore.QSize(850, 670))
        self.gridLayout_2 = QtWidgets.QGridLayout(OverviewForm)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_Trimetric = QtWidgets.QGroupBox(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_Trimetric.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_Trimetric.setSizePolicy(sizePolicy)
        self.groupBox_Trimetric.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_Trimetric.setFlat(True)
        self.groupBox_Trimetric.setObjectName("groupBox_Trimetric")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_Trimetric)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_Trimetric = QtWidgets.QLabel(self.groupBox_Trimetric)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_Trimetric.sizePolicy().hasHeightForWidth()
        )
        self.label_Trimetric.setSizePolicy(sizePolicy)
        self.label_Trimetric.setMinimumSize(QtCore.QSize(220, 220))
        self.label_Trimetric.setMaximumSize(QtCore.QSize(220, 220))
        self.label_Trimetric.setText("")
        self.label_Trimetric.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Trimetric.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Trimetric.setObjectName("label_Trimetric")
        self.gridLayout_4.addWidget(self.label_Trimetric, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_Trimetric, 0, 0, 1, 1)
        self.groupBox_Right = QtWidgets.QGroupBox(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_Right.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_Right.setSizePolicy(sizePolicy)
        self.groupBox_Right.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_Right.setFlat(True)
        self.groupBox_Right.setObjectName("groupBox_Right")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_Right)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_Right = QtWidgets.QLabel(self.groupBox_Right)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Right.sizePolicy().hasHeightForWidth())
        self.label_Right.setSizePolicy(sizePolicy)
        self.label_Right.setMinimumSize(QtCore.QSize(220, 220))
        self.label_Right.setMaximumSize(QtCore.QSize(220, 220))
        self.label_Right.setText("")
        self.label_Right.setObjectName("label_Right")
        self.gridLayout_7.addWidget(self.label_Right, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_Right, 1, 1, 1, 1)
        self.groupBox_Left = QtWidgets.QGroupBox(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_Left.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_Left.setSizePolicy(sizePolicy)
        self.groupBox_Left.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_Left.setFlat(True)
        self.groupBox_Left.setObjectName("groupBox_Left")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_Left)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_Left = QtWidgets.QLabel(self.groupBox_Left)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Left.sizePolicy().hasHeightForWidth())
        self.label_Left.setSizePolicy(sizePolicy)
        self.label_Left.setMinimumSize(QtCore.QSize(220, 220))
        self.label_Left.setMaximumSize(QtCore.QSize(220, 220))
        self.label_Left.setText("")
        self.label_Left.setObjectName("label_Left")
        self.gridLayout_6.addWidget(self.label_Left, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_Left, 1, 0, 1, 1)
        self.groupBox_Top = QtWidgets.QGroupBox(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Top.sizePolicy().hasHeightForWidth())
        self.groupBox_Top.setSizePolicy(sizePolicy)
        self.groupBox_Top.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_Top.setFlat(True)
        self.groupBox_Top.setObjectName("groupBox_Top")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_Top)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_Top = QtWidgets.QLabel(self.groupBox_Top)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Top.sizePolicy().hasHeightForWidth())
        self.label_Top.setSizePolicy(sizePolicy)
        self.label_Top.setMinimumSize(QtCore.QSize(220, 220))
        self.label_Top.setMaximumSize(QtCore.QSize(220, 220))
        self.label_Top.setText("")
        self.label_Top.setObjectName("label_Top")
        self.gridLayout_5.addWidget(self.label_Top, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_Top, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.label_histograms = QtWidgets.QLabel(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_histograms.sizePolicy().hasHeightForWidth()
        )
        self.label_histograms.setSizePolicy(sizePolicy)
        self.label_histograms.setMinimumSize(QtCore.QSize(600, 100))
        self.label_histograms.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_histograms.setAlignment(QtCore.Qt.AlignCenter)
        self.label_histograms.setObjectName("label_histograms")
        self.gridLayout.addWidget(self.label_histograms, 1, 0, 1, 1)
        self.label_xHistogram = QtWidgets.QLabel(OverviewForm)
        self.label_xHistogram.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter
        )
        self.label_xHistogram.setObjectName("label_xHistogram")
        self.gridLayout.addWidget(self.label_xHistogram, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.tableView_partData = QtWidgets.QTableView(OverviewForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableView_partData.sizePolicy().hasHeightForWidth()
        )
        self.tableView_partData.setSizePolicy(sizePolicy)
        self.tableView_partData.setMinimumSize(QtCore.QSize(200, 500))
        self.tableView_partData.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableView_partData.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView_partData.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )
        self.tableView_partData.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.tableView_partData.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tableView_partData.setProperty("showDropIndicator", False)
        self.tableView_partData.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableView_partData.setAlternatingRowColors(True)
        self.tableView_partData.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableView_partData.setShowGrid(False)
        self.tableView_partData.setGridStyle(QtCore.Qt.NoPen)
        self.tableView_partData.setWordWrap(False)
        self.tableView_partData.setCornerButtonEnabled(False)
        self.tableView_partData.setObjectName("tableView_partData")
        self.gridLayout.addWidget(self.tableView_partData, 0, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(OverviewForm)
        QtCore.QMetaObject.connectSlotsByName(OverviewForm)

    def retranslateUi(self, OverviewForm):
        OverviewForm.setWindowTitle(
            QtWidgets.QApplication.translate("OverviewForm", "Form", None, -1)
        )
        self.groupBox_Trimetric.setTitle(
            QtWidgets.QApplication.translate("OverviewForm", "Trimetric", None, -1)
        )
        self.groupBox_Right.setTitle(
            QtWidgets.QApplication.translate("OverviewForm", "Right", None, -1)
        )
        self.groupBox_Left.setTitle(
            QtWidgets.QApplication.translate("OverviewForm", "Left", None, -1)
        )
        self.groupBox_Top.setTitle(
            QtWidgets.QApplication.translate("OverviewForm", "Top", None, -1)
        )
        self.label_histograms.setText(
            QtWidgets.QApplication.translate("OverviewForm", "TextLabel", None, -1)
        )
        self.label_xHistogram.setText(
            QtWidgets.QApplication.translate(
                "OverviewForm",
                "Distribution of feature similar parts in database",
                None,
                -1,
            )
        )
