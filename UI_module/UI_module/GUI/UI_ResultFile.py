# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\02_ResultsDatabase.ui',
# licensing of 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\02_ResultsDatabase.ui' applies.
#
# Created: Thu Apr  2 12:28:00 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_ResultForm(object):
    def setupUi(self, ResultForm):
        ResultForm.setObjectName("ResultForm")
        ResultForm.resize(850, 670)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ResultForm.sizePolicy().hasHeightForWidth())
        ResultForm.setSizePolicy(sizePolicy)
        ResultForm.setMinimumSize(QtCore.QSize(850, 670))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ResultForm)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.results_listParts = QtWidgets.QListView(ResultForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.results_listParts.sizePolicy().hasHeightForWidth()
        )
        self.results_listParts.setSizePolicy(sizePolicy)
        self.results_listParts.setMinimumSize(QtCore.QSize(170, 0))
        self.results_listParts.setMaximumSize(QtCore.QSize(170, 16777215))
        self.results_listParts.setFrameShadow(QtWidgets.QFrame.Raised)
        self.results_listParts.setLineWidth(0)
        self.results_listParts.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.results_listParts.setAutoScrollMargin(0)
        self.results_listParts.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.results_listParts.setProperty("showDropIndicator", False)
        self.results_listParts.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.results_listParts.setIconSize(QtCore.QSize(150, 150))
        self.results_listParts.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.results_listParts.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerItem
        )
        self.results_listParts.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.results_listParts.setSpacing(0)
        self.results_listParts.setGridSize(QtCore.QSize(150, 150))
        self.results_listParts.setViewMode(QtWidgets.QListView.IconMode)
        self.results_listParts.setItemAlignment(QtCore.Qt.AlignCenter)
        self.results_listParts.setObjectName("results_listParts")
        self.verticalLayout.addWidget(self.results_listParts)
        self.results_PageBox = QtWidgets.QGroupBox(ResultForm)
        self.results_PageBox.setMaximumSize(QtCore.QSize(170, 20))
        self.results_PageBox.setTitle("")
        self.results_PageBox.setFlat(True)
        self.results_PageBox.setObjectName("results_PageBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.results_PageBox)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 3, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.results_PageLabel = QtWidgets.QLabel(self.results_PageBox)
        self.results_PageLabel.setMinimumSize(QtCore.QSize(25, 0))
        self.results_PageLabel.setMaximumSize(QtCore.QSize(25, 16777215))
        self.results_PageLabel.setObjectName("results_PageLabel")
        self.horizontalLayout.addWidget(self.results_PageLabel)
        self.results_PageCountLabel = QtWidgets.QLabel(self.results_PageBox)
        self.results_PageCountLabel.setMinimumSize(QtCore.QSize(15, 0))
        self.results_PageCountLabel.setMaximumSize(QtCore.QSize(15, 16777215))
        self.results_PageCountLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.results_PageCountLabel.setObjectName("results_PageCountLabel")
        self.horizontalLayout.addWidget(self.results_PageCountLabel)
        self.results_PageOfLabel = QtWidgets.QLabel(self.results_PageBox)
        self.results_PageOfLabel.setMinimumSize(QtCore.QSize(15, 0))
        self.results_PageOfLabel.setMaximumSize(QtCore.QSize(15, 16777215))
        self.results_PageOfLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.results_PageOfLabel.setObjectName("results_PageOfLabel")
        self.horizontalLayout.addWidget(self.results_PageOfLabel)
        self.results_PageMaxLabel = QtWidgets.QLabel(self.results_PageBox)
        self.results_PageMaxLabel.setMinimumSize(QtCore.QSize(15, 0))
        self.results_PageMaxLabel.setMaximumSize(QtCore.QSize(15, 16777215))
        self.results_PageMaxLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.results_PageMaxLabel.setObjectName("results_PageMaxLabel")
        self.horizontalLayout.addWidget(self.results_PageMaxLabel)
        spacerItem = QtWidgets.QSpacerItem(
            10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.results_PageScroll = QtWidgets.QScrollBar(self.results_PageBox)
        self.results_PageScroll.setMinimumSize(QtCore.QSize(88, 0))
        self.results_PageScroll.setMaximumSize(QtCore.QSize(150, 16777215))
        self.results_PageScroll.setMinimum(1)
        self.results_PageScroll.setPageStep(1)
        self.results_PageScroll.setOrientation(QtCore.Qt.Horizontal)
        self.results_PageScroll.setInvertedControls(True)
        self.results_PageScroll.setObjectName("results_PageScroll")
        self.horizontalLayout.addWidget(self.results_PageScroll)
        self.verticalLayout.addWidget(self.results_PageBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_TopX = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_TopX.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_TopX.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_TopX.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.groupBox_TopX.setFlat(True)
        self.groupBox_TopX.setObjectName("groupBox_TopX")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_TopX)
        self.gridLayout_5.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_TopX = QtWidgets.QLabel(self.groupBox_TopX)
        self.label_TopX.setMinimumSize(QtCore.QSize(100, 100))
        self.label_TopX.setText("")
        self.label_TopX.setAlignment(QtCore.Qt.AlignCenter)
        self.label_TopX.setOpenExternalLinks(False)
        self.label_TopX.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_TopX.setObjectName("label_TopX")
        self.gridLayout_5.addWidget(self.label_TopX, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_TopX, 2, 1, 1, 1)
        self.groupBox_Right = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_Right.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_Right.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_Right.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.groupBox_Right.setFlat(True)
        self.groupBox_Right.setObjectName("groupBox_Right")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_Right)
        self.gridLayout_9.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_Right = QtWidgets.QLabel(self.groupBox_Right)
        self.label_Right.setMinimumSize(QtCore.QSize(100, 100))
        self.label_Right.setText("")
        self.label_Right.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Right.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Right.setObjectName("label_Right")
        self.gridLayout_9.addWidget(self.label_Right, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_Right, 3, 3, 1, 1)
        self.groupBox_LeftX = QtWidgets.QGroupBox(ResultForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_LeftX.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_LeftX.setSizePolicy(sizePolicy)
        self.groupBox_LeftX.setMinimumSize(QtCore.QSize(100, 150))
        self.groupBox_LeftX.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_LeftX.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.groupBox_LeftX.setFlat(True)
        self.groupBox_LeftX.setObjectName("groupBox_LeftX")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_LeftX)
        self.gridLayout_3.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_LeftX = QtWidgets.QLabel(self.groupBox_LeftX)
        self.label_LeftX.setMinimumSize(QtCore.QSize(100, 100))
        self.label_LeftX.setText("")
        self.label_LeftX.setAlignment(QtCore.Qt.AlignCenter)
        self.label_LeftX.setOpenExternalLinks(False)
        self.label_LeftX.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_LeftX.setObjectName("label_LeftX")
        self.gridLayout_3.addWidget(self.label_LeftX, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_LeftX, 3, 0, 1, 1)
        self.groupBox_Trimetric = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_Trimetric.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_Trimetric.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_Trimetric.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter
        )
        self.groupBox_Trimetric.setFlat(True)
        self.groupBox_Trimetric.setObjectName("groupBox_Trimetric")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_Trimetric)
        self.gridLayout_6.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_Trimetric = QtWidgets.QLabel(self.groupBox_Trimetric)
        self.label_Trimetric.setMinimumSize(QtCore.QSize(100, 100))
        self.label_Trimetric.setText("")
        self.label_Trimetric.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Trimetric.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Trimetric.setObjectName("label_Trimetric")
        self.gridLayout_6.addWidget(self.label_Trimetric, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_Trimetric, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(ResultForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(300, 20))
        self.label.setMaximumSize(QtCore.QSize(300, 20))
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.groupBox_Top = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_Top.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_Top.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_Top.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.groupBox_Top.setFlat(True)
        self.groupBox_Top.setObjectName("groupBox_Top")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_Top)
        self.gridLayout_7.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_Top = QtWidgets.QLabel(self.groupBox_Top)
        self.label_Top.setMinimumSize(QtCore.QSize(100, 100))
        self.label_Top.setText("")
        self.label_Top.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Top.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Top.setObjectName("label_Top")
        self.gridLayout_7.addWidget(self.label_Top, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_Top, 2, 3, 1, 1)
        self.groupBox_TrimetricX = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_TrimetricX.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_TrimetricX.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_TrimetricX.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter
        )
        self.groupBox_TrimetricX.setFlat(True)
        self.groupBox_TrimetricX.setObjectName("groupBox_TrimetricX")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_TrimetricX)
        self.gridLayout_2.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_TrimetricX = QtWidgets.QLabel(self.groupBox_TrimetricX)
        self.label_TrimetricX.setMinimumSize(QtCore.QSize(100, 100))
        self.label_TrimetricX.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_TrimetricX.setText("")
        self.label_TrimetricX.setAlignment(QtCore.Qt.AlignCenter)
        self.label_TrimetricX.setOpenExternalLinks(False)
        self.label_TrimetricX.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_TrimetricX.setObjectName("label_TrimetricX")
        self.gridLayout_2.addWidget(self.label_TrimetricX, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_TrimetricX, 2, 0, 1, 1)
        self.groupBox_RightX = QtWidgets.QGroupBox(ResultForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_RightX.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_RightX.setSizePolicy(sizePolicy)
        self.groupBox_RightX.setMinimumSize(QtCore.QSize(100, 150))
        self.groupBox_RightX.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_RightX.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter
        )
        self.groupBox_RightX.setFlat(True)
        self.groupBox_RightX.setObjectName("groupBox_RightX")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_RightX)
        self.gridLayout_4.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_RightX = QtWidgets.QLabel(self.groupBox_RightX)
        self.label_RightX.setMinimumSize(QtCore.QSize(100, 100))
        self.label_RightX.setText("")
        self.label_RightX.setAlignment(QtCore.Qt.AlignCenter)
        self.label_RightX.setOpenExternalLinks(False)
        self.label_RightX.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_RightX.setObjectName("label_RightX")
        self.gridLayout_4.addWidget(self.label_RightX, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_RightX, 3, 1, 1, 1)
        self.groupBox_Left = QtWidgets.QGroupBox(ResultForm)
        self.groupBox_Left.setMinimumSize(QtCore.QSize(150, 150))
        self.groupBox_Left.setMaximumSize(QtCore.QSize(150, 150))
        self.groupBox_Left.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.groupBox_Left.setFlat(True)
        self.groupBox_Left.setObjectName("groupBox_Left")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_Left)
        self.gridLayout_8.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_Left = QtWidgets.QLabel(self.groupBox_Left)
        self.label_Left.setMinimumSize(QtCore.QSize(100, 100))
        self.label_Left.setText("")
        self.label_Left.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Left.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Left.setObjectName("label_Left")
        self.gridLayout_8.addWidget(self.label_Left, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_Left, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(ResultForm)
        self.label_2.setMinimumSize(QtCore.QSize(300, 20))
        self.label_2.setMaximumSize(QtCore.QSize(300, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 2)
        self.pushButton_3DX = QtWidgets.QPushButton(ResultForm)
        self.pushButton_3DX.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3DX.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_3DX.setFlat(False)
        self.pushButton_3DX.setObjectName("pushButton_3DX")
        self.gridLayout.addWidget(self.pushButton_3DX, 5, 0, 1, 1)
        self.pushButton_3D = QtWidgets.QPushButton(ResultForm)
        self.pushButton_3D.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3D.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_3D.setFlat(False)
        self.pushButton_3D.setObjectName("pushButton_3D")
        self.gridLayout.addWidget(self.pushButton_3D, 5, 3, 1, 1)
        self.pushButton_ComparedView = QtWidgets.QPushButton(ResultForm)
        self.pushButton_ComparedView.setEnabled(False)
        self.pushButton_ComparedView.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_ComparedView.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_ComparedView.setFlat(False)
        self.pushButton_ComparedView.setObjectName("pushButton_ComparedView")
        self.gridLayout.addWidget(self.pushButton_ComparedView, 5, 1, 1, 1)
        self.pushButton_DebugComparedView = QtWidgets.QPushButton(ResultForm)
        self.pushButton_DebugComparedView.setEnabled(False)
        self.pushButton_DebugComparedView.setObjectName("pushButton_DebugComparedView")
        self.gridLayout.addWidget(self.pushButton_DebugComparedView, 5, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.results_dataParts = QtWidgets.QTableView(ResultForm)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.results_dataParts.sizePolicy().hasHeightForWidth()
        )
        self.results_dataParts.setSizePolicy(sizePolicy)
        self.results_dataParts.setMinimumSize(QtCore.QSize(680, 330))
        self.results_dataParts.setFrameShadow(QtWidgets.QFrame.Raised)
        self.results_dataParts.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.results_dataParts.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.results_dataParts.setProperty("showDropIndicator", False)
        self.results_dataParts.setDragDropOverwriteMode(False)
        self.results_dataParts.setAlternatingRowColors(True)
        self.results_dataParts.setShowGrid(False)
        self.results_dataParts.setWordWrap(False)
        self.results_dataParts.setCornerButtonEnabled(False)
        self.results_dataParts.setObjectName("results_dataParts")
        self.verticalLayout_2.addWidget(self.results_dataParts)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem1)

        self.retranslateUi(ResultForm)
        QtCore.QMetaObject.connectSlotsByName(ResultForm)

    def retranslateUi(self, ResultForm):
        ResultForm.setWindowTitle(
            QtWidgets.QApplication.translate("ResultForm", "Form", None, -1)
        )
        self.results_PageLabel.setText(
            QtWidgets.QApplication.translate("ResultForm", "Page", None, -1)
        )
        self.results_PageCountLabel.setText(
            QtWidgets.QApplication.translate("ResultForm", "1", None, -1)
        )
        self.results_PageOfLabel.setText(
            QtWidgets.QApplication.translate("ResultForm", "of", None, -1)
        )
        self.results_PageMaxLabel.setText(
            QtWidgets.QApplication.translate("ResultForm", "10", None, -1)
        )
        self.groupBox_TopX.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Top", None, -1)
        )
        self.groupBox_Right.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Right", None, -1)
        )
        self.groupBox_LeftX.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Left", None, -1)
        )
        self.groupBox_Trimetric.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Trimetric", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("ResultForm", "Database", None, -1)
        )
        self.groupBox_Top.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Top", None, -1)
        )
        self.groupBox_TrimetricX.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Trimetric", None, -1)
        )
        self.groupBox_RightX.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Right", None, -1)
        )
        self.groupBox_Left.setTitle(
            QtWidgets.QApplication.translate("ResultForm", "Left", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("ResultForm", " Imported", None, -1)
        )
        self.pushButton_3DX.setText(
            QtWidgets.QApplication.translate("ResultForm", "3D - View", None, -1)
        )
        self.pushButton_3D.setText(
            QtWidgets.QApplication.translate("ResultForm", "3D - View", None, -1)
        )
        self.pushButton_ComparedView.setText(
            QtWidgets.QApplication.translate(
                "ResultForm", "Show Compared View", None, -1
            )
        )
        self.pushButton_DebugComparedView.setText(
            QtWidgets.QApplication.translate(
                "ResultForm", "Debug Compared View", None, -1
            )
        )
