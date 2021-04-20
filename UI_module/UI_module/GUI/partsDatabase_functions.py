# -*- coding: utf-8 -*-
import os
from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
import shutil

from PySide2 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets, QtAxContainer
from PySide2.QtCore import Signal, Slot


from Analysis.Evaluation.DetailSimilarity import CalcDetailSimilarity
from Analysis.Evaluation.FeatureSimilarity import CalcFeatureSimilarity
from Illustration.PartOverview import OverviewView
from Illustration.PartResults import ResultView
from Illustration.FeatureClustering import BokehPlot_features
from Illustration.Utility import PDFViewerClass
from Analysis.Pytable.Pytables_Management_Functions import (
    Pytables_Write_Class,
    Pytables_Read_Class,
    Pytables_Update_Class,
)
from Analysis.Pytable.Pytables_Detail_Analysis import Detail_Transformation_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


def readInSimilarityTable(self):
    featureTable = Pytables_Read_Class(self.paths, "similarity_h5")
    if featureTable.status == True:

        # get parts dnames and ids
        partIDs = np.char.decode(
            featureTable.Read_table_column(
                self.paths.features_table, self.paths.part_id
            ),
            "utf-8",
        )  # type: np.ndarray
        partNames = np.char.decode(
            featureTable.Read_table_column(
                self.paths.features_table, self.paths.part_name
            ),
            "utf-8",
        )

        nrOfRows = partIDs.shape[0]
        if nrOfRows > 0:

            # partIDCol = QtGui.QStandardItem(lenRows, 1)
            # partIDCol.setData(partIDs)

            # partNameCol = QtGui.QStandardItem(lenRows, 1)
            # partNameCol.setData(partNames)

            # set all similarity entries false
            falseArrayFeature = np.full(nrOfRows, "False")

            falseArrayDetail = np.full(nrOfRows, "False")

            # set similarity threshold

            thresholdArray = np.full(nrOfRows, self.calcPrefs.threshold_detail_calc)

            # check if some similarity data was calced and saved in H5
            if featureTable.checkNodeExistence(self.paths.similarity_results_info):
                similarityInfoTable = featureTable.Read_entire_table(
                    self.paths.similarity_results_info
                )

                for posSimTable, partID in enumerate(
                    np.char.decode(similarityInfoTable[self.paths.part_id], "utf-8")
                ):
                    rowSimTable = similarityInfoTable[posSimTable]

                    index_Database = np.where(partIDs == partID)[0]
                    falseArrayFeature[index_Database] = rowSimTable[
                        self.paths.feature_similarity
                    ]
                    falseArrayDetail[index_Database] = rowSimTable[
                        self.paths.detail_similarity
                    ]
                    thresholdArray[index_Database] = rowSimTable[
                        self.paths.detail_threshold
                    ]

            # build numpy array of data
            dataArray = np.ndarray(
                nrOfRows,
                dtype=[
                    (self.paths.part_id, np.unicode_, len(partIDs[0])),
                    (self.paths.part_name, np.object),  # part name len not known
                    (self.paths.feature_similarity, np.unicode_, 5),
                    (self.paths.detail_similarity, np.unicode_, 5),
                    (self.paths.detail_threshold, np.float),
                ],
            )
            dataArray[self.paths.part_id] = partIDs
            dataArray[self.paths.part_name] = partNames
            dataArray[self.paths.feature_similarity] = falseArrayFeature
            dataArray[self.paths.detail_similarity] = falseArrayDetail
            dataArray[self.paths.detail_threshold] = thresholdArray

            # assign data to model of table
            self.model_partsDatabase.setData(dataArray)

        featureTable.closeTable()
    return


def updateSimilarityInfoTable(
    paths: PathsClass,
    tablePath: str,
    column: str,
    parts: List[PartInfoClass],
    values: object,
    standardValues: Dict[str, object],
):
    featureTable = Pytables_Update_Class(paths, "similarity_h5")
    featureTable.updateOrAppend(tablePath, {column: values}, parts, standardValues)
    featureTable.closeTable()


def filterDatabase(self):
    filterText = self.partsDatabase_filterPattern.text()
    columnIndex = self.partsDatabase_filterColumn.currentIndex()
    caseSensitivity = QtCore.Qt.CaseInsensitive
    syntax = QtCore.QRegExp.RegExp
    regExp = QtCore.QRegExp(filterText, caseSensitivity, syntax)
    self.filterModel_partsDatabase.setFilterRegExp(regExp)
    self.filterModel_partsDatabase.setFilterKeyColumn(columnIndex)
    self.filterModel_partsDatabase.invalidate()


def selectAll(treeView: QtWidgets.QTreeView):

    model = treeView.model()
    selection = treeView.selectionModel()
    topLeft = model.index(0, 0)
    bottom = model.rowCount()
    right = model.columnCount()
    bottomRight = model.index(bottom - 1, right - 1)

    newSelection = QtCore.QItemSelection(topLeft, bottomRight)
    totalSelection = QtCore.QItemSelection()
    totalSelection.merge(newSelection, QtCore.QItemSelectionModel.Select)

    selection.select(totalSelection, QtCore.QItemSelectionModel.ClearAndSelect)


def getRowValues(list_model, curr_row, column_len):
    res = [""] * (column_len)
    for j in range(column_len):
        name = list_model.item(curr_row.row(), j).text()
        res[j] = name
    return res


def getSelectedPartsDB(
    tableView: QtWidgets.QTableView, viewInt: int, paths: PathsClass
) -> List[PartInfoClass]:

    # selected_rows_len = len(tableView.selectedIndexes())
    # current_partsDB_indicies = tableView.selectedIndexes()
    cur_model = tableView.model()  # type: tableViewModel
    column_lenDB = cur_model.columnCount()

    partListDB = []
    selected_indexes = tableView.selectedIndexes()[::column_lenDB]
    for index in selected_indexes:

        if viewInt == 0:
            row_i = index.row()

        elif viewInt == 1:
            totalPartID = cur_model.itemData(index)[0]
            cur_model = cur_model.sourceModel()
            row_i = np.where(cur_model._data[paths.part_id] == totalPartID)[0][0]

        totalPartID = cur_model.item(row_i, paths.part_id)
        partName = cur_model.item(row_i, paths.part_name)

        statusFeatureAnalysis = cur_model.item(row_i, paths.feature_similarity)
        statusDetailAnalysis = cur_model.item(row_i, paths.detail_similarity)

        tmpPart = PartInfoClass(
            partName=partName + ".db", partIDstr=totalPartID, pathClass=paths
        )
        tmpPart.featureAnalysis(statusFeatureAnalysis)
        tmpPart.detailAnalysis(statusDetailAnalysis)
        tmpPart.databaseRow(row_i)
        partListDB.append(tmpPart)

    return partListDB


def deleteSimilarityData(
    paths: PathsClass,
    part: PartInfoClass,
    similarityInt: int,
    detailSimilarityValue: float,
):

    changeStatus = False
    similarityTable = Pytables_Update_Class(paths, "similarity_h5")
    similarityNode = (
        paths.similarity_results_group + similarityTable.root + part.getTotalID()
    )

    # delete all similarity data
    if similarityInt == 0 and part.statusFeatureAnalysis != "False":
        similarityTable.deleteRow(paths.similarity_results_info, [part.getTotalID()])
        similarityTable.deleteNode([similarityNode])
        changeStatus = True
    # only delete detail similarity data
    elif similarityInt == 1 and part.statusDetailAnalysis != "False":
        similarityTable.SetColumnValues(
            similarityNode, paths.detail_similarity, [detailSimilarityValue]
        )
        similarityTable.updateOrAppend(
            paths.similarity_results_info,
            {paths.detail_similarity: "False"},
            [part.getTotalID()],
            {},
        )
        changeStatus = True
    # if something changed: delete diagram
    if changeStatus == True:
        diagramPath = os.path.join(
            part.path_physicalDirectory, paths.namedata_feature_diagramm
        )
        if os.path.isfile(diagramPath):
            os.remove(diagramPath)

    similarityTable.closeTable()
    return changeStatus


def deleteH5Data(
    paths: PathsClass, calcPrefs: calcPrefClass, parts: List[PartInfoClass]
):

    box_class = Pytables_Write_Class(paths, "boxdata_h5")

    surfaces_class = Pytables_Write_Class(paths, "surfacesdata_h5")
    surfaces_distNr_class = Pytables_Write_Class(
        paths, "surfacesdistribution_pernumber_h5"
    )
    surfaces_distAr_class = Pytables_Write_Class(
        paths, "surfacesdistribution_perarea_h5"
    )

    pointCloud_class = Pytables_Write_Class(paths, "pointclouddata_h5")
    pointCloud_dist_class = Pytables_Write_Class(paths, "pointclouddistribution_h5")

    feature_class = Pytables_Write_Class(paths, "similarity_h5")

    partIDs = []
    for part in parts:
        partIDs.append(part.getTotalID())

    box_class.deleteRow(paths.box_table, partIDs)

    surfaces_class.deleteNode(partIDs)

    surfaces_distNr_class.deleteRow(paths.surfaces_table_distributions, partIDs)
    surfaces_distAr_class.deleteRow(paths.surfaces_table_distributions, partIDs)

    pointCloud_class.deleteNode(partIDs)
    pointCloud_dist_class.deleteRow(paths.pointcloud_table_distributions, partIDs)

    feature_class.deleteRow(paths.similarity_results_info, partIDs)
    feature_class.deleteRow(paths.features_table, partIDs)
    for part in parts:
        deleteSimilarityData(paths, part, 0, calcPrefs.default_detailsimilarity)


def deleteOverlays(
    paths: PathsClass, parts: List[PartInfoClass]
) -> List[PartInfoClass]:
    similarityH5 = Detail_Transformation_Class(paths, "similarity_h5")
    h5_searchConditions = []
    partIDs_dict = {}
    for part in parts:
        condition = "(({} == b'{}') | ({} == b'{}'))".format(
            paths.part_id + "_a",
            part.getTotalID(),
            paths.part_id + "_b",
            part.getTotalID(),
        )
        h5_searchConditions.append(condition)
        partIDs_dict[part.getTotalID()] = part

    h5_searchConditions_Str = "|".join(h5_searchConditions)

    transformationsParts = similarityH5.Read_table_readWhere(
        paths.transformation_table, h5_searchConditions_Str
    )
    partClasses = []
    if not transformationsParts is None:
        idPairs = []
        for overlayPart in transformationsParts:
            id_a = overlayPart[paths.part_id + "_a"].decode("utf-8")
            id_b = overlayPart[paths.part_id + "_b"].decode("utf-8")
            idPairs.append((id_a, id_b))

            # delete files
            deleteList = []
            if id_a in partIDs_dict:
                deleteList.append(id_a + paths.namedata_overlay)
                partClasses.append(partIDs_dict[id_a])
            if id_b in partIDs_dict:
                deleteList.append(id_b + paths.namedata_overlay)
                partClasses.append(partIDs_dict[id_b])

            combName = id_a + "_vs_" + id_b
            deleteList.append(combName + ".prt")
            deleteList.append(combName + ".pdf")
            deleteList.append(combName + ".log")

            for fileName in deleteList:
                try:
                    os.remove(os.path.join(paths.path_parttransformations, fileName))
                except:
                    print(
                        "Deleting {} failed".format(
                            os.path.join(paths.path_parttransformations, fileName)
                        )
                    )

        similarityH5.deletePartPairs(idPairs)
    similarityH5.closeTable()

    return partClasses


def set3DView(self, part: PartInfoClass = None):
    self.porcess3DPDF = PDFViewerClass()
    assemblyID = part.assemblyId
    name = part.partId

    pdfPath = os.path.join(
        self.paths.path_physicaldatabase,
        assemblyID,
        name,
        name + self.paths.namedata_3d_pdf,
    )
    self.porcess3DPDF.setPath(pdfPath)


def open3DView(self):
    self.porcess3DPDF.start()


def buildOverviewView(self, part: PartInfoClass = None):
    set3DView(self, part)
    statusUITab(self, False)
    self.overViewClass = OverviewView(
        self.paths, self.calcPrefs, part, self.mainWidget_databaseTab
    )
    resultView_whiteBackground(self)
    statusUITab(self, True)
    self.setResultWidget(self.overViewClass.partOverviewWidget)
    self.overViewClass.close()


def buildResultView(self, part: PartInfoClass = None):

    statusUITab(self, False)
    self.resultViewClass = ResultView(
        self.paths,
        self.calcPrefs,
        self.detailColumns,
        part,
        self.mainWidget_databaseTab,
    )

    # output plot
    def outpuWidget():
        resultView_whiteBackground(self)
        statusUITab(self, True)
        self.setResultWidget(self.resultViewClass.partResultWidget)
        self.resultViewClass.close()

    def calcFreeze(status: bool):
        self.tabWidget.setEnabled(status)

    self.resultViewClass.buildingFinished.connect(outpuWidget)
    self.resultViewClass.calculatingSignal.connect(calcFreeze)

    if part.statusFeatureAnalysis == "False" or part.statusFeatureAnalysis == "Old":
        # calc similarity
        self.calcFeatSim = CalcFeatureSimilarity(
            [part],
            self.paths,
            self.calcPrefs,
            self.featureColumns,
            self.featureSimilarityColumns,
        )
        # self.calcFeatSim.start()
        self.calcFeatSim.updateDatabase.connect(self.updateDatabaseTable)
        self.calcFeatSim.updateDatabase.connect(self.resultViewClass.start)
        self.statusbar.showMessage("Missing feature similarity is calculated")
        self.calcFeatSim.thread.start()
    else:
        self.resultViewClass.start()


def buildFeatureDiagramm(self, parts: List[PartInfoClass] = None):

    self.resultViewClass = BokehPlot_features(
        self.paths, self.calcPrefs, self.featureDetails
    )

    # start plot building
    def startPlotBuilder():
        self.statusbar.showMessage("Feature Data Diagram(s) are generated")
        self.resultViewClass.thread.start()

    # output plot
    def outpuWidget(widget):
        statusUITab(self, True)
        self.resultViewClass.close()
        self.setResultWidget(widget)

    # build plot
    def buildDatabaseWidget(widgetObject: str):
        resultView_whiteBackground(self)
        resultWidget = QtWebEngineWidgets.QWebEngineView()
        resultWidget.setUrl(QtCore.QUrl.fromLocalFile(widgetObject))
        resultWidget.setMinimumSize(QtCore.QSize(850, 670))

        outpuWidget(resultWidget)

    # build plot
    def buildPartsWidget(widgetObjects: List[Tuple[str, str]]):
        resultView_whiteBackground(self)
        resultWidget = QtWidgets.QTabWidget(self.mainWidget_databaseTab)
        resultWidget.setUsesScrollButtons(False)

        widgetObjects.sort(key=lambda tup: tup[1])
        for outputPath, part in widgetObjects:
            widgetDiagramm = QtWebEngineWidgets.QWebEngineView()
            widgetDiagramm.setUrl(QtCore.QUrl.fromLocalFile(outputPath))
            widgetDiagramm.setMinimumSize(QtCore.QSize(850, 670))
            resultWidget.addTab(widgetDiagramm, str(part))

        outpuWidget(resultWidget)

    self.resultViewClass.plotBuildingPartsFinished.connect(buildPartsWidget)
    self.resultViewClass.plotBuildingDatabaseFinished.connect(buildDatabaseWidget)

    statusUITab(self, False)

    self.statusbar.showMessage("Feature Data Diagram(s) are generated")

    if not parts is None:
        # check if similarity was calculated
        falseSimCalc_parts = []
        falsePartIds = set()

        for part in parts:
            if (
                part.statusFeatureAnalysis == "False"
                or part.statusFeatureAnalysis == "Old"
            ):
                falseSimCalc_parts.append(part)
                falsePartIds.add(part.getTotalID())

        self.resultViewClass.plotPartSimilarity(parts, falsePartIds)

        # calc similarity
        if len(falseSimCalc_parts) > 0:
            self.calcFeatSim = CalcFeatureSimilarity(
                falseSimCalc_parts,
                self.paths,
                self.calcPrefs,
                self.featureColumns,
                self.featureSimilarityColumns,
            )
            self.calcFeatSim.start()
            self.calcFeatSim.updateDatabase.connect(self.updateDatabaseTable)
            self.calcFeatSim.updateDatabase.connect(startPlotBuilder)
            self.statusbar.showMessage("Missing feature similarity is calculated")
            self.calcFeatSim.thread.start()
        else:
            startPlotBuilder()

    else:
        self.resultViewClass.plotFeatureDatabase()
        startPlotBuilder()


def statusUITab(self, status):
    self.tabWidget.setEnabled(status)
    if status == False:
        self.resultWidget.deleteLater()
        self.resultWidget.destroy()


def resultView_whiteBackground(self):
    resultWidget = QtWidgets.QWidget()  # tyype: QtWidgets.QWidget
    resultWidget.setAutoFillBackground(True)
    palette = resultWidget.palette()
    palette.setColor(resultWidget.backgroundRole(), QtCore.Qt.white)
    resultWidget.setPalette(palette)
    self.setResultWidget(resultWidget)


class tableViewModel(QtCore.QAbstractTableModel):

    _data = np.ndarray(0)
    _headers = [""]
    headerChangedSignal = Signal(object)

    def __init__(self):
        super().__init__()

    @Slot(object)
    def setData(self, data: np.ndarray):
        self._data = data
        self._headers = list(self._data.dtype.names)
        self.layoutChanged.emit()
        self.headerChangedSignal.emit(self._headers)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return str(self._data[index.row()][index.column()])

    def item(self, row, col):
        if type(col) == str:
            return self._data[col][row]
        if type(col) == int:
            return self._data[row][col]

    def findItem(self, col, value):
        if type(col) == str:
            row = np.where(self._data[col] == value)[0][0]
            return self._data[col][row]

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsDragEnabled
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
        )

    @Slot(object)
    def setHeaderData(self, names: List[str]):
        for name in names:
            self._headers.append(name)
        self.headerChangedSignal.emit(self._headers)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._headers[section])
            if orientation == QtCore.Qt.Vertical:
                return str(section)

    def rowCount(self, index=0):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index=0):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)

    def sort(self, col_in, order_in):
        if self.rowCount() > 0:
            if order_in == QtCore.Qt.SortOrder.AscendingOrder:
                self._data.sort(0, order=self._headers[col_in])
            elif order_in == QtCore.Qt.SortOrder.DescendingOrder:
                self._data[::-1].sort(0, order=self._headers[col_in])
            self.layoutChanged.emit()
