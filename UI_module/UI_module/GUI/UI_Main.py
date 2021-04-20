# -*- coding: utf-8 -*-

import copy
import multiprocessing as mp
import os
import shutil
import time
from typing import List, Set, Tuple

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTextStream, Slot

import Analysis.Utility
import GUI.IO
import GUI.partsAnalysis_functions as partsAnalysis_functions
import GUI.partsDatabase_functions as partsDatabase_functions
import GUI.preferences_functions as preferences_functions
import GUI.UI_DesignFile as UI_DesignFile
from GUI.partsDatabase_functions import tableViewModel

from GUI.UI_ImportData import GetSelectedParts, ImportClass
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import PreferencesClass, calcPrefClass, detailColumnsClass


class Ui_MainWindow(UI_DesignFile.Ui_MainWindow):
    status = -1
    statusbarMsgAnalysis = "Please select new files for CAD import"
    statusbarMsgDatabase = (
        "Please select which part(s) in database should be compared to all other parts"
    )
    statusbarMsgPreferences = ""
    outputfilePath = os.path.join(os.getcwd(), "AnalysisOutput.txt")
    outputFile = QtCore.QFile(outputfilePath)

    def setupUi(self, MainWindow):
        # Import directly designed UI-Window
        super().setupUi(MainWindow)

        self.preferences = PreferencesClass(init=True)
        # Paths
        self.paths = self.preferences.getPaths()
        # Calculation preferences
        self.calcPrefs = (
            self.preferences.calculationPreferences()
        )  # type: calcPrefClass
        # Feature columns
        self.featureColumns = self.preferences.getFeatureColumns()
        # Feature columns for similarity calculation
        self.featureSimilarityColumns = self.preferences.getFeatureSimilarityColumns()
        # Feature details
        self.featureDetails = self.preferences.getFeatureDetails()
        # Detail columns
        self.detailColumns = (
            self.preferences.getDetailColumns()
        )  # type: detailColumnsClass
        # Global Preferences
        self.UIpreferences = self.preferences.getUIpreferences()
        # Changes
        self.manual_changes()
        # Slots
        self.UIslots()

        self.outputFile.open(QtCore.QFile.WriteOnly)
        self.outputStream = QTextStream(self.outputFile)

    def manual_changes(self):
        self.tabWidget.setCurrentIndex(0)
        self.AnalysisRunning = False
        self.selectAll_clicked = False
        ######### ANALYSIS #########
        self.model_partsAnalysis = QtGui.QStandardItemModel()
        self.model_partsAnalysis.setHorizontalHeaderLabels(
            ["Part", "Id", "Path", "CreateDate"]
        )
        self.tableView_partsAnalysis.setModel(self.model_partsAnalysis)
        self.tableView_partsAnalysis.setEnabled(True)
        self.tableView_partsAnalysis.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_partsAnalysis.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
        )
        self.selectionModel_tableView_partsAnalysis = (
            self.tableView_partsAnalysis.selectionModel()
        )
        self.selectionModel_tableView_partsAnalysis.selectionChanged.connect(
            self.activateAnalysisRunButton
        )
        self.selectionModel_tableView_partsAnalysis.selectionChanged.connect(
            self.control_selectAllBox
        )

        self.tableView_partsAnalysis.show()

        self.statusbar.showMessage(self.statusbarMsgAnalysis)

        ######### Database #########
        # Preferences
        selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection
        self.viewsDBList = [
            self.tableView_partsDatabase,
            self.tableView_partsDatabase_filtered,
        ]
        # Imported Parts
        self.model_partsDatabase = tableViewModel()
        self.model_partsDatabase.setHeaderData(
            [
                self.paths.part_id,
                self.paths.part_name,
                self.paths.feature_similarity,
                self.paths.detail_similarity,
                self.paths.detail_threshold,
            ]
        )

        self.tableView_partsDatabase.setModel(self.model_partsDatabase)
        self.tableView_partsDatabase.horizontalHeader().setEnabled(True)
        self.tableView_partsDatabase.horizontalHeader().setVisible(True)
        self.tableView_partsDatabase.setEnabled(True)
        self.tableView_partsDatabase.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
        )

        self.tableView_partsDatabase.setSortingEnabled(True)
        self.tableView_partsDatabase.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView_partsDatabase.setSelectionMode(selectionMode)
        self.tableView_partsDatabase.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Interactive
        )

        self.selectionModel_partsDatabase = (
            self.tableView_partsDatabase.selectionModel()
        )  # type: QtCore.QItemSelectionModel
        self.tableView_partsDatabase.show()

        # Filtered Parts
        self.groupBox_2.setEnabled(False)  # disable buggy filtering
        self.filterModel_partsDatabase = QtCore.QSortFilterProxyModel()
        self.filterModel_partsDatabase.setSourceModel(self.model_partsDatabase)
        self.tableView_partsDatabase_filtered.setModel(self.filterModel_partsDatabase)
        self.tableView_partsDatabase_filtered.setEnabled(True)
        self.tableView_partsDatabase_filtered.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
        )

        self.tableView_partsDatabase_filtered.setSortingEnabled(False)  # quite slow
        self.tableView_partsDatabase_filtered.setSelectionMode(selectionMode)
        self.tableView_partsDatabase_filtered.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Interactive
        )

        self.selectionModel_partsDatabase_filtered = (
            self.tableView_partsDatabase_filtered.selectionModel()
        )  # type: QtCore.QItemSelectionModel

        self.tableView_partsDatabase_filtered.show()

        # results
        self.resultWidget = QtWidgets.QWidget()
        partsDatabase_functions.resultView_whiteBackground(self)

        ######### Preferences #########
        self.model_preferences = QtGui.QStandardItemModel()
        self.preferencesTab_treeView.setModel(self.model_preferences)
        self.preferencesTab_treeView.header().hide()
        self.preferencesTab_treeView.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows
        )
        self.selectionModel_preferences = (
            self.preferencesTab_treeView.selectionModel()
        )  # type: QtCore.QItemSelectionModel
        # self.initPrefTab()

    def UIslots(self):
        ######### ANALYSIS #########
        self.selectAll_checkBox.clicked.connect(self.on_click_checkbox)
        self.delete_pushButton.clicked.connect(self.on_click_deleteparts)
        self.loadPart_pushButton.clicked.connect(self.on_click_loadPart)
        self.loadFolder_pushButton.clicked.connect(self.on_click_loadFolder)
        self.analysisTab_run_importCADData.clicked.connect(self.getSelection)
        ######### Database #########
        self.partsDatabase_filterButton.clicked.connect(self.filterDatabase)
        self.partsDatabase_resetButton.clicked.connect(self.resetFilterDatabase)

        self.partsDatabase_selectAll.clicked.connect(lambda: self.selectAllPartsDB(0))
        self.partsDatabase_selectNone.clicked.connect(lambda: self.selectNoPartsDB(0))
        self.selectionModel_partsDatabase.selectionChanged.connect(
            lambda: self.getSelectionPartsDB(0)
        )

        self.partsDatabase_filtered_selectAll.clicked.connect(
            lambda: self.selectAllPartsDB(1)
        )
        self.partsDatabase_filtered_selectNone.clicked.connect(
            lambda: self.selectNoPartsDB(1)
        )
        self.selectionModel_partsDatabase_filtered.selectionChanged.connect(
            lambda: self.getSelectionPartsDB(1)
        )

        self.databaseTab_run_featureSimilarity.clicked.connect(
            self.runFeatureSimilarity
        )
        self.databaseTab_run_detailSimilarity.clicked.connect(self.runDetailSimilarity)

        self.databaseTab_reset_featureSimilarity.clicked.connect(
            lambda: self.deleteSimilarityData(0)
        )
        self.databaseTab_reset_detailSimilarity.clicked.connect(
            lambda: self.deleteSimilarityData(1)
        )

        # Delete H5 data
        self.databaseTab_deletePart.clicked.connect(self.deletePartData)
        # Illustration
        self.databaseTab_resultPart.clicked.connect(self.showResults)

        self.databaseTab_diagramDatabase.clicked.connect(
            self.showFeatureDiagramDatabase
        )
        self.databaseTab_diagramParts.clicked.connect(self.showFeatureDiagramParts)
        # define filterable columns
        self.model_partsDatabase.headerChangedSignal.connect(
            self.partsDatabase_filterColumn.addItems
        )
        # edit detail threshold
        self.partsDatabase_editThreshold.clicked.connect(self.editDetailThreshold)
        self.partsDatabase_filtered_editThreshold.clicked.connect(
            self.editDetailThreshold
        )
        self.databaseTab_3DView.clicked.connect(
            lambda: partsDatabase_functions.open3DView(self)
        )
        # Delete overlays
        self.databaseTab_deleteOverlays.clicked.connect(self.deleteOverlays)
        ######## Preferences #######
        self.selectionModel_preferences.selectionChanged.connect(self.prefSelection)
        ######### Tab #########
        self.tabWidget.currentChanged.connect(self.checkCurrentTab)

    def checkCurrentTab(self):
        if self.tabWidget.currentIndex() == 0:
            self.statusbar.showMessage(self.statusbarMsgAnalysis)
        if self.tabWidget.currentIndex() == 1:
            self.statusbar.showMessage(self.statusbarMsgDatabase)
            self.updateDatabaseTable()
        if self.tabWidget.currentIndex() == 2:
            self.statusbar.showMessage(self.statusbarMsgPreferences)

    def printOutputMessages(self, message: str):
        self.outputStream << message + "\n"
        self.outputStream.flush()
        print(message)

    ############################
    ######### ANALYSIS #########
    ############################

    def activateAnalysisRunButton(self):
        if (
            len(self.tableView_partsAnalysis.selectedIndexes()) > 0
            and self.AnalysisRunning == False
        ):
            self.analysisTab_run_importCADData.setDisabled(False)

        else:
            self.analysisTab_run_importCADData.setDisabled(True)

    def control_selectAllBox(self):
        if self.selectAll_clicked == True:
            self.selectAll_clicked = False
        else:
            self.selectAll_checkBox.setChecked(False)

    def on_click_loadPart(self):
        # IO.openFileNameDialog(self)
        partsAnalysis_functions.openFileNameDialog(self, self.paths.file_endings)
        # self.tableView_partsAnalysis.resizeColumnsToContents()

    def on_click_loadFolder(self):
        # IO.openFileNamesDialog(self)
        partsAnalysis_functions.openDirectoryNameDialog(self, self.paths.file_endings)
        # self.tableView_partsAnalysis.resizeColumnsToContents()

    @Slot(bool)
    def statusFreezeCADAnalysis(self, status: bool):
        if status == True:
            self.statusbarMsgAnalysis = "Import of CAD data is running"
            self.statusbar.showMessage(self.statusbarMsgAnalysis)
        if status == False:
            self.statusbarMsgAnalysis = "Please select new files for CAD import"
            self.statusbar.showMessage(self.statusbarMsgAnalysis)

        self.AnalysisRunning = status

        selectionMode = QtWidgets.QAbstractItemView.MultiSelection
        if status == True:
            selectionMode = QtWidgets.QAbstractItemView.NoSelection

        self.tableView_partsAnalysis.setSelectionMode(selectionMode)

        self.analysisTab_run_importCADData.setDisabled(status)
        self.loadPart_pushButton.setDisabled(status)
        self.loadFolder_pushButton.setDisabled(status)
        self.selectAll_checkBox.setDisabled(status)
        self.delete_pushButton.setDisabled(status)

    def getSelection(self):
        self.statusFreezeCADAnalysis(True)

        column_len = self.model_partsAnalysis.columnCount()

        selected_indexes = self.tableView_partsAnalysis.selectedIndexes()[::column_len]
        if len(selected_indexes) > 70:
            cpuCount = os.cpu_count()
            selectionPackages = np.array_split(
                np.array(selected_indexes), cpuCount, axis=0
            )
        else:
            selectionPackages = np.array([selected_indexes])

        self.GetSelectedParts = GetSelectedParts(
            self.model_partsAnalysis, selectionPackages, self.paths
        )

        self.GetSelectedParts.selectionFinished.connect(self.startCADAnalysis)
        self.GetSelectedParts.outputSignal.connect(self.printOutputMessages)
        self.GetSelectedParts.start()

    @Slot(tuple)
    def startCADAnalysis(self, partsTuple: Tuple[List[PartInfoClass], Set[str]]):

        del self.GetSelectedParts
        self.partList = partsTuple[0]
        self.partIDsSet = partsTuple[1]

        self.Analysis = ImportClass(
            self.paths, self.calcPrefs, self.partList, self.featureColumns
        )

        self.Analysis.deletePartsFromList.connect(self.deleteParts_afterAnalysis)
        self.Analysis.outputMsg.connect(self.printOutputMessages)
        self.Analysis.updateDatabase.connect(self.updateDatabaseTable)
        self.Analysis.freezeStatusUI.connect(self.statusFreezeCADAnalysis)
        self.Analysis.start()

    def on_click_checkbox(self):
        if self.selectAll_checkBox.isChecked():
            self.selectAll_clicked = True
            self.tableView_partsAnalysis.selectAll()
        else:
            self.tableView_partsAnalysis.clearSelection()

    def on_click_deleteparts(self):
        # IO.openFileNamesDialog(self)

        column_len = self.model_partsAnalysis.columnCount()
        selected_indexes = self.tableView_partsAnalysis.selectedIndexes()[::column_len]

        if len(selected_indexes) == self.model_partsAnalysis.rowCount():
            partsAnalysis_functions.delete_partslist(self, True)
        else:

            if len(selected_indexes) > 70:
                cpuCount = os.cpu_count()
                selectionPackages = np.array_split(
                    np.array(selected_indexes), cpuCount, axis=0
                )
            else:
                selectionPackages = np.array([selected_indexes])

            self.GetSelectedPartsDelete = GetSelectedParts(
                self.model_partsAnalysis, selectionPackages, self.paths
            )

            def catchPartSet(outTuple):
                selectedPartsSet = outTuple[1]
                partsAnalysis_functions.delete_partslist(self, False, selectedPartsSet)

            self.GetSelectedPartsDelete.selectionFinished.connect(catchPartSet)
            self.GetSelectedPartsDelete.start()

    def deleteParts_afterAnalysis(self, parts: List[PartInfoClass]):
        partIDSet = set()
        for part in parts:
            partIDSet.add(part.assemblyId)
        partsAnalysis_functions.delete_partslist(self, False, partIDSet)

    ############################
    ######### Database #########
    ############################

    ######### Utilities ########

    def updateDatabaseTable(self, updateSignal: bool = False):
        numberOfRows = self.model_partsDatabase.rowCount()
        if numberOfRows == 0 or updateSignal:
            partsDatabase_functions.readInSimilarityTable(self)
            self.partsDatabase_count.setText(
                "Parts: {}".format(self.model_partsDatabase.rowCount())
            )
            # check if some new parts were added -> delete old diagram
            if numberOfRows > 0 and numberOfRows < self.model_partsDatabase.rowCount():
                diagramPath = self.paths.path_feature_diagramm_dataset
                if os.path.isfile(diagramPath):
                    os.remove(diagramPath)

            # self.filterDatabase()

        self.databaseTab_diagramDatabase.setEnabled(False)
        if self.model_partsDatabase.rowCount() > 0:
            self.databaseTab_diagramDatabase.setEnabled(True)

    def filterDatabase(self):
        partsDatabase_functions.filterDatabase(self)
        self.partsDatabase_filtered_count.setText(
            "Parts: {}".format(self.filterModel_partsDatabase.rowCount())
        )

    def resetFilterDatabase(self):
        self.partsDatabase_filterPattern.setText("")
        self.filterDatabase()

    def selectAllPartsDB(self, viewInt: int):
        antiViewInt = 1
        if viewInt == 1:
            antiViewInt = 0
        self.selectNoPartsDB(antiViewInt)
        partsDatabase_functions.selectAll(self.viewsDBList[viewInt])

    def selectNoPartsDB(self, viewInt: int):
        self.viewsDBList[viewInt].selectionModel().clearSelection()

    def getSelectionPartsDB(self, viewInt: int):
        self.viewDBint = viewInt

        antiViewInt = 1
        if viewInt == 1:
            antiViewInt = 0
        self.viewsDBList[antiViewInt].selectionModel().clearSelection()

        self.changeButtonstatus(False)
        selected = (
            len(self.viewsDBList[self.viewDBint].selectedIndexes())
            / self.viewsDBList[self.viewDBint].model().columnCount()
        )

        if selected > 0:
            if selected == 1:
                self.showOverview()
            self.changeButtonstatus(True, selected)

    def changeButtonstatus(self, status: bool, selectedItems: int = 0):
        self.databaseTab_run_featureSimilarity.setEnabled(status)
        self.databaseTab_run_detailSimilarity.setEnabled(status)

        self.databaseTab_reset_featureSimilarity.setEnabled(status)
        self.databaseTab_reset_detailSimilarity.setEnabled(status)
        self.databaseTab_deletePart.setEnabled(status)
        self.databaseTab_deleteOverlays.setEnabled(status)

        if selectedItems == 1 or status == False:
            self.databaseTab_resultPart.setEnabled(status)
            self.databaseTab_3DView.setEnabled(status)
        self.databaseTab_diagramParts.setEnabled(status)

        self.partsDatabase_editThreshold.setEnabled(status)
        self.partsDatabase_filtered_editThreshold.setEnabled(status)

    def deletePartData(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )

        # #!!no risk while debugging!!
        # tmpPart = PartInfoClass("5cef2581-c3e8-4917-bd70-80737de174e6", "00000")
        # tmpPart.defineOutputPaths(self.paths)
        # tmpPart.updateDecomposition("00000")
        # partList = [tmpPart]

        partsDatabase_functions.deleteH5Data(self.paths, self.calcPrefs, partList)

        for part in partList:
            if os.path.isdir(part.path_physicalDirectory):
                shutil.rmtree(part.path_physicalDirectory)

        self.updateDatabaseTable(True)

    def deleteSimilarityData(self, similarityInt: int):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )
        changeSet = set()
        for part in partList:
            changeSet.add(
                partsDatabase_functions.deleteSimilarityData(
                    self.paths,
                    part,
                    similarityInt,
                    self.calcPrefs.default_detailsimilarity,
                )
            )

        if True in changeSet:
            self.updateDatabaseTable(True)

    def deleteOverlays(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )
        deletedPartClasses = partsDatabase_functions.deleteOverlays(
            self.paths, partList
        )

        # remove detail similarity calculations
        for part in deletedPartClasses:
            partsDatabase_functions.deleteSimilarityData(
                self.paths, part, 1, self.calcPrefs.default_detailsimilarity
            )
        if len(deletedPartClasses) > 0:
            self.updateDatabaseTable(True)

    def editDetailThreshold(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )

        standardValuesInfo = {
            self.paths.part_id: "",
            self.paths.feature_similarity: "False",
            self.paths.detail_similarity: "False",
            self.paths.detail_threshold: self.calcPrefs.threshold_detail_calc,
        }

        self.thresholdInputWidget = QtWidgets.QInputDialog(self.centralwidget)
        title = "Threshold detail similarity calculation"
        label = "Please enter a threshold value for the selceted part(s)"
        threshold = self.calcPrefs.threshold_detail_calc
        minValue = 0.0
        maxValue = 1.0
        decimals = 2
        threshold, status = self.thresholdInputWidget.getDouble(
            self.centralwidget, title, label, threshold, minValue, maxValue, decimals
        )

        if status == True:
            partsDatabase_functions.updateSimilarityInfoTable(
                self.paths,
                self.paths.similarity_results_info,
                self.paths.detail_threshold,
                partList,
                threshold,
                standardValuesInfo,
            )
            self.updateDatabaseTable(True)

    ######### Analyzing ########

    def runFeatureSimilarity(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )

        self.calcFeatSim = partsDatabase_functions.CalcFeatureSimilarity(
            partList,
            self.paths,
            self.calcPrefs,
            self.featureColumns,
            self.featureSimilarityColumns,
        )

        self.calcFeatSim.updateDatabase.connect(self.updateDatabaseTable)

        self.calcFeatSim.thread.start()

    def runDetailSimilarity(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )

        self.calcDetSim = partsDatabase_functions.CalcDetailSimilarity(
            partList, self.paths, self.detailColumns, self.calcPrefs
        )
        self.calcDetSim.updateDatabase.connect(self.updateDatabaseTable)
        self.calcDetSim.updateDatabase.connect(lambda: self.tabWidget.setEnabled(True))

        # check if feature similarity was calculated
        parts_noFeatureCalc = []
        for part in partList:
            if part.statusFeatureAnalysis != "Done":
                parts_noFeatureCalc.append(part)
        if len(parts_noFeatureCalc) > 0:
            self.calcFeatSim = partsDatabase_functions.CalcFeatureSimilarity(
                parts_noFeatureCalc,
                self.paths,
                self.calcPrefs,
                self.featureColumns,
                self.featureSimilarityColumns,
            )
            self.calcFeatSim.updateDatabase.connect(self.calcDetSim.thread.start)
            self.calcFeatSim.thread.started.connect(
                lambda: self.tabWidget.setEnabled(False)
            )
            self.calcFeatSim.thread.start()
        else:
            self.tabWidget.setEnabled(False)
            self.calcDetSim.thread.start()

    ######### Illustration ########

    @Slot(object)
    def setResultWidget(self, widget):

        self.resultWidget = widget
        self.gridLayout_mainWidget_databaseTab.addWidget(widget, 0, 0, 1, 1)
        self.mainWidget_databaseTab.adjustSize()
        self.statusbar.showMessage(self.statusbarMsgDatabase)

    def showOverview(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )

        partsDatabase_functions.buildOverviewView(self, partList[0])

    def showResults(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )
        partsDatabase_functions.buildResultView(self, partList[0])

    def showFeatureDiagramParts(self):
        partList = partsDatabase_functions.getSelectedPartsDB(
            self.viewsDBList[self.viewDBint], self.viewDBint, self.paths
        )
        partsDatabase_functions.buildFeatureDiagramm(self, partList)

    def showFeatureDiagramDatabase(self):
        partsDatabase_functions.buildFeatureDiagramm(self)

    ############################
    ######## Preferences #######
    ############################

    def initPrefTab(self):
        self.preferenceWidget = None
        preferences_functions.initPreferenceTree(self)

    def prefSelection(self):
        index = self.preferencesTab_treeView.selectedIndexes()[0]
        item = self.model_preferences.itemFromIndex(index)
        if not item.parent() is None:
            parent = item.parent().text()
            subCat = item.text()
            self.setPreferenceWidget(self.widgetDict[parent, subCat])

    @Slot(object)
    def setPreferenceWidget(self, widget: QtWidgets.QWidget):
        if not self.preferenceWidget is None:
            widgetOld = self.preferenceWidget  # type: QtWidgets.QWidget
            widgetOld.hide()
            self.gridLayout_mainWidget_preferencesTab.removeWidget(widgetOld)
            self.preferenceWidget = widget
            self.preferenceWidget.show()
            self.gridLayout_mainWidget_preferencesTab.addWidget(
                self.preferenceWidget, 0, 0, 1, 1
            )
        else:
            self.preferenceWidget = widget
            self.gridLayout_mainWidget_preferencesTab.addWidget(
                self.preferenceWidget, 0, 0, 1, 1
            )

        self.mainWidget_preferencesTab.adjustSize()
        self.statusbar.showMessage(self.statusbarMsgPreferences)
