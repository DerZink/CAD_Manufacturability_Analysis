# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\00_MainWindow.ui',
# licensing of 'd:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\00_MainWindow.ui' applies.
#
# Created: Tue Jun  9 12:54:17 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1449, 891)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_analysis = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_analysis.sizePolicy().hasHeightForWidth())
        self.tab_analysis.setSizePolicy(sizePolicy)
        self.tab_analysis.setObjectName("tab_analysis")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_analysis)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabAnalysis_splitter = QtWidgets.QSplitter(self.tab_analysis)
        self.tabAnalysis_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.tabAnalysis_splitter.setObjectName("tabAnalysis_splitter")
        self.analysis_lhs_frame = QtWidgets.QFrame(self.tabAnalysis_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_lhs_frame.sizePolicy().hasHeightForWidth()
        )
        self.analysis_lhs_frame.setSizePolicy(sizePolicy)
        self.analysis_lhs_frame.setMinimumSize(QtCore.QSize(500, 0))
        self.analysis_lhs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.analysis_lhs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.analysis_lhs_frame.setObjectName("analysis_lhs_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.analysis_lhs_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.analysis_lhs_frame)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox.setObjectName("groupBox")
        self.selectAll_checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.selectAll_checkBox.setGeometry(QtCore.QRect(10, 20, 70, 25))
        self.selectAll_checkBox.setMinimumSize(QtCore.QSize(70, 0))
        self.selectAll_checkBox.setObjectName("selectAll_checkBox")
        self.delete_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.delete_pushButton.setGeometry(QtCore.QRect(90, 20, 100, 25))
        self.delete_pushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.verticalLayout.addWidget(self.groupBox)
        self.tableView_partsAnalysis = QtWidgets.QTableView(self.analysis_lhs_frame)
        self.tableView_partsAnalysis.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView_partsAnalysis.setObjectName("tableView_partsAnalysis")
        self.verticalLayout.addWidget(self.tableView_partsAnalysis)
        self.analysis_rhs_frame = QtWidgets.QFrame(self.tabAnalysis_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_rhs_frame.sizePolicy().hasHeightForWidth()
        )
        self.analysis_rhs_frame.setSizePolicy(sizePolicy)
        self.analysis_rhs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.analysis_rhs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.analysis_rhs_frame.setObjectName("analysis_rhs_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.analysis_rhs_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.viewer_label = QtWidgets.QLabel(self.analysis_rhs_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewer_label.sizePolicy().hasHeightForWidth())
        self.viewer_label.setSizePolicy(sizePolicy)
        self.viewer_label.setMinimumSize(QtCore.QSize(0, 15))
        self.viewer_label.setObjectName("viewer_label")
        self.verticalLayout_2.addWidget(self.viewer_label)
        self.mainWidget_analysisTab = QtWidgets.QWidget(self.analysis_rhs_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWidget_analysisTab.sizePolicy().hasHeightForWidth()
        )
        self.mainWidget_analysisTab.setSizePolicy(sizePolicy)
        self.mainWidget_analysisTab.setMinimumSize(QtCore.QSize(0, 500))
        self.mainWidget_analysisTab.setAutoFillBackground(True)
        self.mainWidget_analysisTab.setObjectName("mainWidget_analysisTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.mainWidget_analysisTab)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.mainLabel_analysisTab = QtWidgets.QLabel(self.mainWidget_analysisTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainLabel_analysisTab.sizePolicy().hasHeightForWidth()
        )
        self.mainLabel_analysisTab.setSizePolicy(sizePolicy)
        self.mainLabel_analysisTab.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainLabel_analysisTab.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLabel_analysisTab.setObjectName("mainLabel_analysisTab")
        self.gridLayout_6.addWidget(self.mainLabel_analysisTab, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.mainWidget_analysisTab)
        self.analysis_rhs_bottom_sub_frame = QtWidgets.QFrame(self.analysis_rhs_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_rhs_bottom_sub_frame.sizePolicy().hasHeightForWidth()
        )
        self.analysis_rhs_bottom_sub_frame.setSizePolicy(sizePolicy)
        self.analysis_rhs_bottom_sub_frame.setMinimumSize(QtCore.QSize(700, 100))
        self.analysis_rhs_bottom_sub_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.analysis_rhs_bottom_sub_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.analysis_rhs_bottom_sub_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.analysis_rhs_bottom_sub_frame.setObjectName(
            "analysis_rhs_bottom_sub_frame"
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.analysis_rhs_bottom_sub_frame
        )
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_groupBox = QtWidgets.QGroupBox(self.analysis_rhs_bottom_sub_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.input_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.input_groupBox.setSizePolicy(sizePolicy)
        self.input_groupBox.setMinimumSize(QtCore.QSize(125, 0))
        self.input_groupBox.setMaximumSize(QtCore.QSize(125, 16777215))
        self.input_groupBox.setObjectName("input_groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.input_groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.loadPart_pushButton = QtWidgets.QPushButton(self.input_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.loadPart_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.loadPart_pushButton.setSizePolicy(sizePolicy)
        self.loadPart_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.loadPart_pushButton.setObjectName("loadPart_pushButton")
        self.verticalLayout_3.addWidget(self.loadPart_pushButton)
        self.loadFolder_pushButton = QtWidgets.QPushButton(self.input_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.loadFolder_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.loadFolder_pushButton.setSizePolicy(sizePolicy)
        self.loadFolder_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.loadFolder_pushButton.setObjectName("loadFolder_pushButton")
        self.verticalLayout_3.addWidget(self.loadFolder_pushButton)
        self.horizontalLayout.addWidget(self.input_groupBox)
        self.analysis_groupBox = QtWidgets.QGroupBox(self.analysis_rhs_bottom_sub_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.analysis_groupBox.setSizePolicy(sizePolicy)
        self.analysis_groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.analysis_groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.analysis_groupBox.setObjectName("analysis_groupBox")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.analysis_groupBox)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.analysisTab_run_importCADData = QtWidgets.QPushButton(
            self.analysis_groupBox
        )
        self.analysisTab_run_importCADData.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysisTab_run_importCADData.sizePolicy().hasHeightForWidth()
        )
        self.analysisTab_run_importCADData.setSizePolicy(sizePolicy)
        self.analysisTab_run_importCADData.setMinimumSize(QtCore.QSize(100, 25))
        self.analysisTab_run_importCADData.setObjectName(
            "analysisTab_run_importCADData"
        )
        self.gridLayout_11.addWidget(self.analysisTab_run_importCADData, 0, 0, 1, 1)
        self.selectedPart_3D_view_pushButton = QtWidgets.QPushButton(
            self.analysis_groupBox
        )
        self.selectedPart_3D_view_pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selectedPart_3D_view_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.selectedPart_3D_view_pushButton.setSizePolicy(sizePolicy)
        self.selectedPart_3D_view_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.selectedPart_3D_view_pushButton.setObjectName(
            "selectedPart_3D_view_pushButton"
        )
        self.gridLayout_11.addWidget(self.selectedPart_3D_view_pushButton, 0, 1, 1, 1)
        self.horizontalLayout.addWidget(self.analysis_groupBox)
        spacerItem = QtWidgets.QSpacerItem(
            304, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.analysis_rhs_bottom_sub_frame)
        self.gridLayout_2.addWidget(self.tabAnalysis_splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_analysis, "")
        self.tab_database = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_database.sizePolicy().hasHeightForWidth())
        self.tab_database.setSizePolicy(sizePolicy)
        self.tab_database.setObjectName("tab_database")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_database)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabDatabase_splitter = QtWidgets.QSplitter(self.tab_database)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabDatabase_splitter.sizePolicy().hasHeightForWidth()
        )
        self.tabDatabase_splitter.setSizePolicy(sizePolicy)
        self.tabDatabase_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.tabDatabase_splitter.setObjectName("tabDatabase_splitter")
        self.database_left_frame = QtWidgets.QFrame(self.tabDatabase_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_left_frame.sizePolicy().hasHeightForWidth()
        )
        self.database_left_frame.setSizePolicy(sizePolicy)
        self.database_left_frame.setMinimumSize(QtCore.QSize(500, 0))
        self.database_left_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.database_left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.database_left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.database_left_frame.setObjectName("database_left_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.database_left_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.partsDatabase_groupBox = QtWidgets.QGroupBox(self.database_left_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_groupBox.setSizePolicy(sizePolicy)
        self.partsDatabase_groupBox.setMinimumSize(QtCore.QSize(350, 0))
        self.partsDatabase_groupBox.setObjectName("partsDatabase_groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.partsDatabase_groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.partsDatabase_selectAll = QtWidgets.QPushButton(
            self.partsDatabase_groupBox
        )
        self.partsDatabase_selectAll.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_selectAll.setObjectName("partsDatabase_selectAll")
        self.gridLayout_5.addWidget(self.partsDatabase_selectAll, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_5.addItem(spacerItem1, 0, 3, 1, 1)
        self.partsDatabase_count = QtWidgets.QLabel(self.partsDatabase_groupBox)
        self.partsDatabase_count.setObjectName("partsDatabase_count")
        self.gridLayout_5.addWidget(self.partsDatabase_count, 0, 4, 1, 1)
        self.partsDatabase_selectNone = QtWidgets.QPushButton(
            self.partsDatabase_groupBox
        )
        self.partsDatabase_selectNone.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_selectNone.setObjectName("partsDatabase_selectNone")
        self.gridLayout_5.addWidget(self.partsDatabase_selectNone, 0, 1, 1, 1)
        self.partsDatabase_editThreshold = QtWidgets.QPushButton(
            self.partsDatabase_groupBox
        )
        self.partsDatabase_editThreshold.setEnabled(False)
        self.partsDatabase_editThreshold.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_editThreshold.setObjectName("partsDatabase_editThreshold")
        self.gridLayout_5.addWidget(self.partsDatabase_editThreshold, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_5)
        self.tableView_partsDatabase = QtWidgets.QTableView(self.partsDatabase_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableView_partsDatabase.sizePolicy().hasHeightForWidth()
        )
        self.tableView_partsDatabase.setSizePolicy(sizePolicy)
        self.tableView_partsDatabase.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView_partsDatabase.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView_partsDatabase.setEditTriggers(
            QtWidgets.QAbstractItemView.AllEditTriggers
        )
        self.tableView_partsDatabase.setDragEnabled(True)
        self.tableView_partsDatabase.setDragDropOverwriteMode(False)
        self.tableView_partsDatabase.setDragDropMode(
            QtWidgets.QAbstractItemView.DragOnly
        )
        self.tableView_partsDatabase.setAlternatingRowColors(False)
        self.tableView_partsDatabase.setShowGrid(False)
        self.tableView_partsDatabase.setWordWrap(False)
        self.tableView_partsDatabase.setCornerButtonEnabled(False)
        self.tableView_partsDatabase.setObjectName("tableView_partsDatabase")
        self.tableView_partsDatabase.horizontalHeader().setVisible(False)
        self.tableView_partsDatabase.horizontalHeader().setCascadingSectionResizes(
            False
        )
        self.tableView_partsDatabase.horizontalHeader().setDefaultSectionSize(100)
        self.tableView_partsDatabase.horizontalHeader().setMinimumSectionSize(39)
        self.tableView_partsDatabase.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout_4.addWidget(self.tableView_partsDatabase)
        self.verticalLayout_6.addWidget(self.partsDatabase_groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.database_left_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_12.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.partsDatabase_filtered_count = QtWidgets.QLabel(self.groupBox_2)
        self.partsDatabase_filtered_count.setObjectName("partsDatabase_filtered_count")
        self.gridLayout_12.addWidget(self.partsDatabase_filtered_count, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_12.addItem(spacerItem2, 0, 3, 1, 1)
        self.partsDatabase_filtered_selectNone = QtWidgets.QPushButton(self.groupBox_2)
        self.partsDatabase_filtered_selectNone.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_filtered_selectNone.setObjectName(
            "partsDatabase_filtered_selectNone"
        )
        self.gridLayout_12.addWidget(self.partsDatabase_filtered_selectNone, 0, 1, 1, 1)
        self.partsDatabase_filtered_selectAll = QtWidgets.QPushButton(self.groupBox_2)
        self.partsDatabase_filtered_selectAll.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_filtered_selectAll.setObjectName(
            "partsDatabase_filtered_selectAll"
        )
        self.gridLayout_12.addWidget(self.partsDatabase_filtered_selectAll, 0, 0, 1, 1)
        self.partsDatabase_filtered_editThreshold = QtWidgets.QPushButton(
            self.groupBox_2
        )
        self.partsDatabase_filtered_editThreshold.setEnabled(False)
        self.partsDatabase_filtered_editThreshold.setMinimumSize(QtCore.QSize(0, 25))
        self.partsDatabase_filtered_editThreshold.setObjectName(
            "partsDatabase_filtered_editThreshold"
        )
        self.gridLayout_12.addWidget(
            self.partsDatabase_filtered_editThreshold, 0, 2, 1, 1
        )
        self.verticalLayout_12.addLayout(self.gridLayout_12)
        self.tableView_partsDatabase_filtered = QtWidgets.QTableView(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableView_partsDatabase_filtered.sizePolicy().hasHeightForWidth()
        )
        self.tableView_partsDatabase_filtered.setSizePolicy(sizePolicy)
        self.tableView_partsDatabase_filtered.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.tableView_partsDatabase_filtered.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView_partsDatabase_filtered.setDragDropOverwriteMode(False)
        self.tableView_partsDatabase_filtered.setAlternatingRowColors(False)
        self.tableView_partsDatabase_filtered.setShowGrid(False)
        self.tableView_partsDatabase_filtered.setWordWrap(False)
        self.tableView_partsDatabase_filtered.setCornerButtonEnabled(False)
        self.tableView_partsDatabase_filtered.setObjectName(
            "tableView_partsDatabase_filtered"
        )
        self.tableView_partsDatabase_filtered.horizontalHeader().setCascadingSectionResizes(
            False
        )
        self.tableView_partsDatabase_filtered.horizontalHeader().setDefaultSectionSize(
            100
        )
        self.tableView_partsDatabase_filtered.horizontalHeader().setMinimumSectionSize(
            39
        )
        self.tableView_partsDatabase_filtered.horizontalHeader().setStretchLastSection(
            False
        )
        self.verticalLayout_12.addWidget(self.tableView_partsDatabase_filtered)
        self.database_selectedpart_frame = QtWidgets.QFrame(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_selectedpart_frame.sizePolicy().hasHeightForWidth()
        )
        self.database_selectedpart_frame.setSizePolicy(sizePolicy)
        self.database_selectedpart_frame.setMinimumSize(QtCore.QSize(350, 50))
        self.database_selectedpart_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.database_selectedpart_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.database_selectedpart_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.database_selectedpart_frame.setObjectName("database_selectedpart_frame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.database_selectedpart_frame)
        self.gridLayout_7.setContentsMargins(9, -1, 0, -1)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.partsDatabase_filterButton = QtWidgets.QPushButton(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_filterButton.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_filterButton.setSizePolicy(sizePolicy)
        self.partsDatabase_filterButton.setMinimumSize(QtCore.QSize(50, 25))
        self.partsDatabase_filterButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.partsDatabase_filterButton.setObjectName("partsDatabase_filterButton")
        self.gridLayout_7.addWidget(self.partsDatabase_filterButton, 2, 3, 1, 1)
        self.partsDatabase_filterPatternLabel = QtWidgets.QLabel(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_filterPatternLabel.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_filterPatternLabel.setSizePolicy(sizePolicy)
        self.partsDatabase_filterPatternLabel.setMinimumSize(QtCore.QSize(70, 0))
        self.partsDatabase_filterPatternLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.partsDatabase_filterPatternLabel.setMargin(0)
        self.partsDatabase_filterPatternLabel.setTextInteractionFlags(
            QtCore.Qt.NoTextInteraction
        )
        self.partsDatabase_filterPatternLabel.setObjectName(
            "partsDatabase_filterPatternLabel"
        )
        self.gridLayout_7.addWidget(self.partsDatabase_filterPatternLabel, 0, 0, 1, 1)
        self.partsDatabase_filterColumn = QtWidgets.QComboBox(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_filterColumn.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_filterColumn.setSizePolicy(sizePolicy)
        self.partsDatabase_filterColumn.setMinimumSize(QtCore.QSize(150, 25))
        self.partsDatabase_filterColumn.setObjectName("partsDatabase_filterColumn")
        self.gridLayout_7.addWidget(self.partsDatabase_filterColumn, 2, 1, 1, 2)
        self.partsDatabase_filterColumnLabel = QtWidgets.QLabel(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_filterColumnLabel.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_filterColumnLabel.setSizePolicy(sizePolicy)
        self.partsDatabase_filterColumnLabel.setMinimumSize(QtCore.QSize(70, 0))
        self.partsDatabase_filterColumnLabel.setMaximumSize(QtCore.QSize(70, 16777215))
        self.partsDatabase_filterColumnLabel.setObjectName(
            "partsDatabase_filterColumnLabel"
        )
        self.gridLayout_7.addWidget(self.partsDatabase_filterColumnLabel, 2, 0, 1, 1)
        self.partsDatabase_resetButton = QtWidgets.QPushButton(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_resetButton.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_resetButton.setSizePolicy(sizePolicy)
        self.partsDatabase_resetButton.setMinimumSize(QtCore.QSize(50, 25))
        self.partsDatabase_resetButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.partsDatabase_resetButton.setObjectName("partsDatabase_resetButton")
        self.gridLayout_7.addWidget(self.partsDatabase_resetButton, 2, 4, 1, 1)
        self.partsDatabase_filterPattern = QtWidgets.QLineEdit(
            self.database_selectedpart_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.partsDatabase_filterPattern.sizePolicy().hasHeightForWidth()
        )
        self.partsDatabase_filterPattern.setSizePolicy(sizePolicy)
        self.partsDatabase_filterPattern.setMinimumSize(QtCore.QSize(280, 0))
        self.partsDatabase_filterPattern.setObjectName("partsDatabase_filterPattern")
        self.gridLayout_7.addWidget(self.partsDatabase_filterPattern, 0, 1, 1, 4)
        self.verticalLayout_12.addWidget(self.database_selectedpart_frame)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.database_right_frame = QtWidgets.QFrame(self.tabDatabase_splitter)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_right_frame.sizePolicy().hasHeightForWidth()
        )
        self.database_right_frame.setSizePolicy(sizePolicy)
        self.database_right_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.database_right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.database_right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.database_right_frame.setObjectName("database_right_frame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.database_right_frame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.mainWidget_databaseTab = QtWidgets.QWidget(self.database_right_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWidget_databaseTab.sizePolicy().hasHeightForWidth()
        )
        self.mainWidget_databaseTab.setSizePolicy(sizePolicy)
        self.mainWidget_databaseTab.setMinimumSize(QtCore.QSize(900, 700))
        self.mainWidget_databaseTab.setAutoFillBackground(True)
        self.mainWidget_databaseTab.setObjectName("mainWidget_databaseTab")
        self.gridLayout_mainWidget_databaseTab = QtWidgets.QGridLayout(
            self.mainWidget_databaseTab
        )
        self.gridLayout_mainWidget_databaseTab.setSpacing(0)
        self.gridLayout_mainWidget_databaseTab.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_mainWidget_databaseTab.setObjectName(
            "gridLayout_mainWidget_databaseTab"
        )
        self.verticalLayout_7.addWidget(self.mainWidget_databaseTab)
        self.database_rhs_bottom_sub_frame = QtWidgets.QFrame(self.database_right_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.database_rhs_bottom_sub_frame.sizePolicy().hasHeightForWidth()
        )
        self.database_rhs_bottom_sub_frame.setSizePolicy(sizePolicy)
        self.database_rhs_bottom_sub_frame.setMinimumSize(QtCore.QSize(700, 100))
        self.database_rhs_bottom_sub_frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.database_rhs_bottom_sub_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.database_rhs_bottom_sub_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.database_rhs_bottom_sub_frame.setObjectName(
            "database_rhs_bottom_sub_frame"
        )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.database_rhs_bottom_sub_frame
        )
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.databaseTab_selectedPart_groupBox = QtWidgets.QGroupBox(
            self.database_rhs_bottom_sub_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_selectedPart_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_selectedPart_groupBox.setSizePolicy(sizePolicy)
        self.databaseTab_selectedPart_groupBox.setMinimumSize(QtCore.QSize(150, 0))
        self.databaseTab_selectedPart_groupBox.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.databaseTab_selectedPart_groupBox.setObjectName(
            "databaseTab_selectedPart_groupBox"
        )
        self.gridLayout_10 = QtWidgets.QGridLayout(
            self.databaseTab_selectedPart_groupBox
        )
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.databaseTab_reset_featureSimilarity = QtWidgets.QPushButton(
            self.databaseTab_selectedPart_groupBox
        )
        self.databaseTab_reset_featureSimilarity.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_reset_featureSimilarity.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_reset_featureSimilarity.setSizePolicy(sizePolicy)
        self.databaseTab_reset_featureSimilarity.setMinimumSize(QtCore.QSize(40, 0))
        self.databaseTab_reset_featureSimilarity.setMaximumSize(
            QtCore.QSize(40, 16777215)
        )
        self.databaseTab_reset_featureSimilarity.setObjectName(
            "databaseTab_reset_featureSimilarity"
        )
        self.gridLayout_10.addWidget(
            self.databaseTab_reset_featureSimilarity, 0, 2, 1, 1
        )
        self.databaseTab_reset_detailSimilarity = QtWidgets.QPushButton(
            self.databaseTab_selectedPart_groupBox
        )
        self.databaseTab_reset_detailSimilarity.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_reset_detailSimilarity.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_reset_detailSimilarity.setSizePolicy(sizePolicy)
        self.databaseTab_reset_detailSimilarity.setMinimumSize(QtCore.QSize(25, 25))
        self.databaseTab_reset_detailSimilarity.setMaximumSize(
            QtCore.QSize(40, 16777215)
        )
        self.databaseTab_reset_detailSimilarity.setObjectName(
            "databaseTab_reset_detailSimilarity"
        )
        self.gridLayout_10.addWidget(
            self.databaseTab_reset_detailSimilarity, 1, 2, 1, 1
        )
        self.databaseTab_run_detailSimilarity = QtWidgets.QPushButton(
            self.databaseTab_selectedPart_groupBox
        )
        self.databaseTab_run_detailSimilarity.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_run_detailSimilarity.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_run_detailSimilarity.setSizePolicy(sizePolicy)
        self.databaseTab_run_detailSimilarity.setMinimumSize(QtCore.QSize(40, 0))
        self.databaseTab_run_detailSimilarity.setMaximumSize(QtCore.QSize(40, 16777215))
        self.databaseTab_run_detailSimilarity.setObjectName(
            "databaseTab_run_detailSimilarity"
        )
        self.gridLayout_10.addWidget(self.databaseTab_run_detailSimilarity, 1, 1, 1, 1)
        self.databaseTab_run_featureSimilarity = QtWidgets.QPushButton(
            self.databaseTab_selectedPart_groupBox
        )
        self.databaseTab_run_featureSimilarity.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_run_featureSimilarity.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_run_featureSimilarity.setSizePolicy(sizePolicy)
        self.databaseTab_run_featureSimilarity.setMinimumSize(QtCore.QSize(40, 25))
        self.databaseTab_run_featureSimilarity.setMaximumSize(
            QtCore.QSize(40, 16777215)
        )
        font = QtGui.QFont()
        self.databaseTab_run_featureSimilarity.setFont(font)
        self.databaseTab_run_featureSimilarity.setObjectName(
            "databaseTab_run_featureSimilarity"
        )
        self.gridLayout_10.addWidget(self.databaseTab_run_featureSimilarity, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.databaseTab_selectedPart_groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_2.setObjectName("label_2")
        self.gridLayout_10.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.databaseTab_selectedPart_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(50, 0))
        self.label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label.setObjectName("label")
        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.databaseTab_selectedPart_groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.database_rhs_bottom_sub_frame)
        self.groupBox_3.setMaximumSize(QtCore.QSize(125, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.databaseTab_resultPart = QtWidgets.QPushButton(self.groupBox_3)
        self.databaseTab_resultPart.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_resultPart.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_resultPart.setSizePolicy(sizePolicy)
        self.databaseTab_resultPart.setMinimumSize(QtCore.QSize(0, 0))
        self.databaseTab_resultPart.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        self.databaseTab_resultPart.setFont(font)
        self.databaseTab_resultPart.setObjectName("databaseTab_resultPart")
        self.gridLayout_13.addWidget(self.databaseTab_resultPart, 0, 1, 1, 1)
        self.databaseTab_3DView = QtWidgets.QPushButton(self.groupBox_3)
        self.databaseTab_3DView.setEnabled(False)
        self.databaseTab_3DView.setObjectName("databaseTab_3DView")
        self.gridLayout_13.addWidget(self.databaseTab_3DView, 1, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.databaseTab_dbAnalysis_groupBox = QtWidgets.QGroupBox(
            self.database_rhs_bottom_sub_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_dbAnalysis_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_dbAnalysis_groupBox.setSizePolicy(sizePolicy)
        self.databaseTab_dbAnalysis_groupBox.setMinimumSize(QtCore.QSize(125, 0))
        self.databaseTab_dbAnalysis_groupBox.setMaximumSize(QtCore.QSize(125, 16777215))
        self.databaseTab_dbAnalysis_groupBox.setObjectName(
            "databaseTab_dbAnalysis_groupBox"
        )
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(
            self.databaseTab_dbAnalysis_groupBox
        )
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.databaseTab_diagramDatabase = QtWidgets.QPushButton(
            self.databaseTab_dbAnalysis_groupBox
        )
        self.databaseTab_diagramDatabase.setEnabled(False)
        self.databaseTab_diagramDatabase.setObjectName("databaseTab_diagramDatabase")
        self.verticalLayout_11.addWidget(self.databaseTab_diagramDatabase)
        self.databaseTab_diagramParts = QtWidgets.QPushButton(
            self.databaseTab_dbAnalysis_groupBox
        )
        self.databaseTab_diagramParts.setEnabled(False)
        self.databaseTab_diagramParts.setObjectName("databaseTab_diagramParts")
        self.verticalLayout_11.addWidget(self.databaseTab_diagramParts)
        self.horizontalLayout_2.addWidget(self.databaseTab_dbAnalysis_groupBox)
        self.databaseTab_IO_groupBox = QtWidgets.QGroupBox(
            self.database_rhs_bottom_sub_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_IO_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_IO_groupBox.setSizePolicy(sizePolicy)
        self.databaseTab_IO_groupBox.setMinimumSize(QtCore.QSize(100, 0))
        self.databaseTab_IO_groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.databaseTab_IO_groupBox.setObjectName("databaseTab_IO_groupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.databaseTab_IO_groupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.databaseTab_deletePart = QtWidgets.QPushButton(
            self.databaseTab_IO_groupBox
        )
        self.databaseTab_deletePart.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_deletePart.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_deletePart.setSizePolicy(sizePolicy)
        self.databaseTab_deletePart.setMinimumSize(QtCore.QSize(100, 0))
        self.databaseTab_deletePart.setObjectName("databaseTab_deletePart")
        self.gridLayout_8.addWidget(self.databaseTab_deletePart, 1, 0, 1, 1)
        self.databaseTab_loadParts_pushButton = QtWidgets.QPushButton(
            self.databaseTab_IO_groupBox
        )
        self.databaseTab_loadParts_pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_loadParts_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_loadParts_pushButton.setSizePolicy(sizePolicy)
        self.databaseTab_loadParts_pushButton.setMinimumSize(QtCore.QSize(100, 25))
        self.databaseTab_loadParts_pushButton.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        self.databaseTab_loadParts_pushButton.setFont(font)
        self.databaseTab_loadParts_pushButton.setObjectName(
            "databaseTab_loadParts_pushButton"
        )
        self.gridLayout_8.addWidget(self.databaseTab_loadParts_pushButton, 2, 0, 1, 1)
        self.databaseTab_loadFolder_pushButton = QtWidgets.QPushButton(
            self.databaseTab_IO_groupBox
        )
        self.databaseTab_loadFolder_pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_loadFolder_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_loadFolder_pushButton.setSizePolicy(sizePolicy)
        self.databaseTab_loadFolder_pushButton.setMinimumSize(QtCore.QSize(100, 25))
        self.databaseTab_loadFolder_pushButton.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        font = QtGui.QFont()
        self.databaseTab_loadFolder_pushButton.setFont(font)
        self.databaseTab_loadFolder_pushButton.setObjectName(
            "databaseTab_loadFolder_pushButton"
        )
        self.gridLayout_8.addWidget(self.databaseTab_loadFolder_pushButton, 1, 1, 1, 1)
        self.databaseTab_deleteOverlays = QtWidgets.QPushButton(
            self.databaseTab_IO_groupBox
        )
        self.databaseTab_deleteOverlays.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.databaseTab_deleteOverlays.sizePolicy().hasHeightForWidth()
        )
        self.databaseTab_deleteOverlays.setSizePolicy(sizePolicy)
        self.databaseTab_deleteOverlays.setObjectName("databaseTab_deleteOverlays")
        self.gridLayout_8.addWidget(self.databaseTab_deleteOverlays, 2, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.databaseTab_IO_groupBox)
        spacerItem3 = QtWidgets.QSpacerItem(
            17, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_7.addWidget(self.database_rhs_bottom_sub_frame)
        self.gridLayout_3.addWidget(self.tabDatabase_splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_database, "")
        self.tab_preferences = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tab_preferences.sizePolicy().hasHeightForWidth()
        )
        self.tab_preferences.setSizePolicy(sizePolicy)
        self.tab_preferences.setObjectName("tab_preferences")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_preferences)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabPreferences_splitter = QtWidgets.QSplitter(self.tab_preferences)
        self.tabPreferences_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.tabPreferences_splitter.setObjectName("tabPreferences_splitter")
        self.preferences_lhs_frame = QtWidgets.QFrame(self.tabPreferences_splitter)
        self.preferences_lhs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.preferences_lhs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.preferences_lhs_frame.setObjectName("preferences_lhs_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.preferences_lhs_frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.preferencesTab_treeView = QtWidgets.QTreeView(self.preferences_lhs_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.preferencesTab_treeView.sizePolicy().hasHeightForWidth()
        )
        self.preferencesTab_treeView.setSizePolicy(sizePolicy)
        self.preferencesTab_treeView.setMinimumSize(QtCore.QSize(200, 0))
        self.preferencesTab_treeView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.preferencesTab_treeView.setProperty("showDropIndicator", False)
        self.preferencesTab_treeView.setTextElideMode(QtCore.Qt.ElideNone)
        self.preferencesTab_treeView.setObjectName("preferencesTab_treeView")
        self.verticalLayout_8.addWidget(self.preferencesTab_treeView)
        self.preferencesGlobal_horizontalLayout = QtWidgets.QHBoxLayout()
        self.preferencesGlobal_horizontalLayout.setObjectName(
            "preferencesGlobal_horizontalLayout"
        )
        self.preferencesGlobal_groupBox = QtWidgets.QGroupBox(
            self.preferences_lhs_frame
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.preferencesGlobal_groupBox.sizePolicy().hasHeightForWidth()
        )
        self.preferencesGlobal_groupBox.setSizePolicy(sizePolicy)
        self.preferencesGlobal_groupBox.setMinimumSize(QtCore.QSize(200, 60))
        self.preferencesGlobal_groupBox.setMaximumSize(QtCore.QSize(200, 60))
        self.preferencesGlobal_groupBox.setObjectName("preferencesGlobal_groupBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.preferencesGlobal_groupBox)
        self.horizontalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.preferencesGlobal_load_pushButton = QtWidgets.QPushButton(
            self.preferencesGlobal_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.preferencesGlobal_load_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.preferencesGlobal_load_pushButton.setSizePolicy(sizePolicy)
        self.preferencesGlobal_load_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.preferencesGlobal_load_pushButton.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.preferencesGlobal_load_pushButton.setObjectName(
            "preferencesGlobal_load_pushButton"
        )
        self.horizontalLayout_5.addWidget(self.preferencesGlobal_load_pushButton)
        self.preferencesGlobal_save_pushButton = QtWidgets.QPushButton(
            self.preferencesGlobal_groupBox
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.preferencesGlobal_save_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.preferencesGlobal_save_pushButton.setSizePolicy(sizePolicy)
        self.preferencesGlobal_save_pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.preferencesGlobal_save_pushButton.setMaximumSize(
            QtCore.QSize(16777215, 16777215)
        )
        self.preferencesGlobal_save_pushButton.setObjectName(
            "preferencesGlobal_save_pushButton"
        )
        self.horizontalLayout_5.addWidget(self.preferencesGlobal_save_pushButton)
        self.preferencesGlobal_horizontalLayout.addWidget(
            self.preferencesGlobal_groupBox
        )
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.preferencesGlobal_horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_8.addLayout(self.preferencesGlobal_horizontalLayout)
        self.preferences_rhs_frame = QtWidgets.QFrame(self.tabPreferences_splitter)
        self.preferences_rhs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.preferences_rhs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.preferences_rhs_frame.setObjectName("preferences_rhs_frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.preferences_rhs_frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.mainWidget_preferencesTab = QtWidgets.QWidget(self.preferences_rhs_frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWidget_preferencesTab.sizePolicy().hasHeightForWidth()
        )
        self.mainWidget_preferencesTab.setSizePolicy(sizePolicy)
        self.mainWidget_preferencesTab.setMinimumSize(QtCore.QSize(1000, 800))
        self.mainWidget_preferencesTab.setAutoFillBackground(True)
        self.mainWidget_preferencesTab.setObjectName("mainWidget_preferencesTab")
        self.gridLayout_mainWidget_preferencesTab = QtWidgets.QGridLayout(
            self.mainWidget_preferencesTab
        )
        self.gridLayout_mainWidget_preferencesTab.setSpacing(0)
        self.gridLayout_mainWidget_preferencesTab.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_mainWidget_preferencesTab.setObjectName(
            "gridLayout_mainWidget_preferencesTab"
        )
        self.verticalLayout_9.addWidget(self.mainWidget_preferencesTab)
        self.gridLayout_4.addWidget(self.tabPreferences_splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_preferences, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1)
        )
        self.groupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Part List", None, -1)
        )
        self.selectAll_checkBox.setText(
            QtWidgets.QApplication.translate("MainWindow", "Select All", None, -1)
        )
        self.delete_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Delete", None, -1)
        )
        self.viewer_label.setText(
            QtWidgets.QApplication.translate("MainWindow", "Viewer", None, -1)
        )
        self.mainLabel_analysisTab.setText(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "2 possible fullscreen views: \n"
                "- status run analysis \n"
                "- 3D-View of the part",
                None,
                -1,
            )
        )
        self.input_groupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Input", None, -1)
        )
        self.loadPart_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load Part(s)", None, -1)
        )
        self.loadFolder_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load Folder", None, -1)
        )
        self.analysis_groupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Selected Part(s)", None, -1)
        )
        self.analysisTab_run_importCADData.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Import CAD\n" "Data", None, -1
            )
        )
        self.selectedPart_3D_view_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "3D-View", None, -1)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_analysis),
            QtWidgets.QApplication.translate("MainWindow", "Analysis", None, -1),
        )
        self.partsDatabase_groupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Imported Parts", None, -1)
        )
        self.partsDatabase_selectAll.setText(
            QtWidgets.QApplication.translate("MainWindow", "Select All", None, -1)
        )
        self.partsDatabase_count.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parts: 0", None, -1)
        )
        self.partsDatabase_selectNone.setText(
            QtWidgets.QApplication.translate("MainWindow", "Select None", None, -1)
        )
        self.partsDatabase_editThreshold.setText(
            QtWidgets.QApplication.translate("MainWindow", "Edit Threshold", None, -1)
        )
        self.groupBox_2.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Filtered Parts", None, -1)
        )
        self.partsDatabase_filtered_count.setText(
            QtWidgets.QApplication.translate("MainWindow", "Parts: 0", None, -1)
        )
        self.partsDatabase_filtered_selectNone.setText(
            QtWidgets.QApplication.translate("MainWindow", "Select None", None, -1)
        )
        self.partsDatabase_filtered_selectAll.setText(
            QtWidgets.QApplication.translate("MainWindow", "Select All", None, -1)
        )
        self.partsDatabase_filtered_editThreshold.setText(
            QtWidgets.QApplication.translate("MainWindow", "Edit Threshold", None, -1)
        )
        self.partsDatabase_filterButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Filter", None, -1)
        )
        self.partsDatabase_filterPatternLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "Filter Pattern:", None, -1)
        )
        self.partsDatabase_filterColumnLabel.setText(
            QtWidgets.QApplication.translate("MainWindow", "Filter Column:", None, -1)
        )
        self.partsDatabase_resetButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reset", None, -1)
        )
        self.databaseTab_selectedPart_groupBox.setTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Selected Part(s) Calculation", None, -1
            )
        )
        self.databaseTab_reset_featureSimilarity.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reset", None, -1)
        )
        self.databaseTab_reset_detailSimilarity.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reset", None, -1)
        )
        self.databaseTab_run_detailSimilarity.setText(
            QtWidgets.QApplication.translate("MainWindow", "Run", None, -1)
        )
        self.databaseTab_run_featureSimilarity.setText(
            QtWidgets.QApplication.translate("MainWindow", "Run", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Detail\n" "Similarity", None, -1
            )
        )
        self.label.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Feature\n" "Similarity", None, -1
            )
        )
        self.groupBox_3.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Selected Part", None, -1)
        )
        self.databaseTab_resultPart.setText(
            QtWidgets.QApplication.translate("MainWindow", "Results", None, -1)
        )
        self.databaseTab_3DView.setText(
            QtWidgets.QApplication.translate("MainWindow", "3D-View", None, -1)
        )
        self.databaseTab_dbAnalysis_groupBox.setTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Feature Data Diagram", None, -1
            )
        )
        self.databaseTab_diagramDatabase.setText(
            QtWidgets.QApplication.translate("MainWindow", "Database", None, -1)
        )
        self.databaseTab_diagramParts.setText(
            QtWidgets.QApplication.translate("MainWindow", "Selected Part(s)", None, -1)
        )
        self.databaseTab_IO_groupBox.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Manage Database", None, -1)
        )
        self.databaseTab_deletePart.setText(
            QtWidgets.QApplication.translate("MainWindow", "Delete Part(s)", None, -1)
        )
        self.databaseTab_loadParts_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load Part(s)", None, -1)
        )
        self.databaseTab_loadFolder_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load Folder", None, -1)
        )
        self.databaseTab_deleteOverlays.setText(
            QtWidgets.QApplication.translate(
                "MainWindow", "Delete Overlay(s)", None, -1
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_database),
            QtWidgets.QApplication.translate("MainWindow", "Database", None, -1),
        )
        self.preferencesGlobal_groupBox.setTitle(
            QtWidgets.QApplication.translate(
                "MainWindow", "Preferences Global", None, -1
            )
        )
        self.preferencesGlobal_load_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Reset", None, -1)
        )
        self.preferencesGlobal_save_pushButton.setText(
            QtWidgets.QApplication.translate("MainWindow", "Save", None, -1)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_preferences),
            QtWidgets.QApplication.translate("MainWindow", "Preferences", None, -1),
        )
