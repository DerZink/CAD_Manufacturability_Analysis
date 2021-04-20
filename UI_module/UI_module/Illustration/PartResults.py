import os
from typing import List
import sys
import subprocess

import numpy as np
from numpy.lib import recfunctions as rfn
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from GUI.UI_ResultFile import Ui_ResultForm
from Illustration.Utility import PDFViewerClass
from Illustration.PartsOverlay import partsOverlay_Class, debugOverlay_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass

# import ptvsd


class ResultView(QtCore.QObject):

    buildingFinished = Signal(object)
    calculatingSignal = Signal(bool)
    partResultWidget = ""

    def __init__(
        self,
        paths: PathsClass,
        calcPrefs: calcPrefClass,
        detailColumns: detailColumnsClass,
        part: PartInfoClass,
        mainWidget_databaseTab: QtWidgets.QWidget,
    ):
        super().__init__()
        self.paths = paths
        self.calcPrefs = calcPrefs
        self.part = part
        self.partID = self.part.getTotalID()
        self.mainWidget_databaseTab = mainWidget_databaseTab

        self.partResultWidget = QtWidgets.QWidget()
        self.partResultView = Ui_ResultForm()
        self.partResultView.setupUi(self.partResultWidget)

        self.setViews()
        self.process3DX = PDFViewerClass()
        self.process3D = PDFViewerClass()
        self.PicSize = QtCore.QSize(120, 120)

        self.overlayClass = partsOverlay_Class(
            self.paths, self.calcPrefs, detailColumns
        )  # type: partsOverlay_Class
        self.debugOverlay = debugOverlay_Class(
            self.paths, self.calcPrefs, detailColumns
        )  # type: debugOverlay_Class

    def setViews(self):
        self.maxPartsPerListView = 5
        self.listModel = qtModel_iconPartList(self.maxPartsPerListView)
        self.listModel.clear()
        # part list widget
        self.partResultView.results_listParts.setModel(self.listModel)

        self.tableModel = qtModel_featureTables(self.partID, self.paths)
        self.tableModel.clear()
        # part features view widget
        self.partResultView.results_dataParts.setModel(self.tableModel)

    @Slot(object)
    def start(self):

        self.featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")
        self.similarityResultsPart_path = (
            self.featureH5.root
            + self.paths.similarity_results_group
            + self.featureH5.root
            + self.partID
        )

        self.similarParts = self.featureH5.Read_table_range(
            self.similarityResultsPart_path, 0, self.calcPrefs.similar_parts_diagramm
        )

        # build part list view
        self.setPartList()

        # build feature table
        self.setFeatureTable()

        # build 3D view
        # imported part
        self.set3DView(self.partResultView.pushButton_3D, self.partID)
        self.setPics(self.partID)

        # databse part
        bestPartID = self.partResultView.results_listParts.model().dataItem(
            self.paths.part_id, 0
        )
        self.set3DView(self.partResultView.pushButton_3DX, bestPartID)
        self.setPics(bestPartID)
        self.definePartOverlay(bestPartID)

        # connect part list and feature table
        partListSelection = (
            self.partResultView.results_listParts.selectionModel()
        )  # type: QtCore.QItemSelectionModel
        partListSelection.selectionChanged.connect(self.getPartName)

        self.buildingFinished.emit("done")

    def close(self):
        self.featureH5.closeTable()

    def setPartList(self):

        partIDs = self.similarParts[self.paths.part_id]
        numberOfParts = len(partIDs) - 1

        steps = int(round(numberOfParts / self.maxPartsPerListView, 0))

        # horizontal scroll
        self.partResultView.results_PageScroll.setMaximum(steps)
        self.partResultView.results_PageMaxLabel.setNum(steps)
        self.partResultView.results_PageScroll.valueChanged.connect(
            self.partResultView.results_PageCountLabel.setNum
        )
        self.partResultView.results_PageScroll.valueChanged.connect(
            self.listModel.sliceData
        )

        # part list data
        dataArray = np.ndarray(
            numberOfParts,
            dtype=[
                (self.paths.part_id, np.unicode_, len(partIDs[0])),
                (self.paths.part_name, np.object),  # part name len not known
                ("images", np.object),  # image name len not known
            ],
        )

        partIDsArray = np.char.decode(partIDs, "utf-8")
        # remove imported part from list
        rowPart = np.where(partIDsArray == self.partID)[0][0]
        partIDsArray = np.delete(partIDsArray, rowPart)

        partNamesArray = np.full(numberOfParts, object)
        picsArray = np.full(numberOfParts, object)

        for i, partID in enumerate(partIDsArray):
            assemblyID = "".join(partID.split("_")[:-1])
            name_i = partID.split("_")[-1]

            pathPart = os.path.join(
                self.paths.path_physicaldatabase, assemblyID, name_i
            )
            # picsArray[i] = QtGui.QIcon(
            #     os.path.join(pathPart, name_i + "_" + self.paths.namedata_image)
            # )
            picsArray[i] = os.path.join(
                pathPart, name_i + "_" + self.paths.namedata_image
            )

            partNamesArray[i] = name_i

        dataArray[self.paths.part_id] = partIDsArray
        dataArray[self.paths.part_name] = partNamesArray
        dataArray["images"] = picsArray

        # if detail data available, sort after it
        if self.part.statusDetailAnalysis == "Done":
            detailSimilarityData = self.similarParts[self.paths.detail_similarity]
            detailSimilarityData = np.delete(detailSimilarityData, rowPart)

            featureSimilarityData = self.similarParts[self.paths.feature_similarity]
            featureSimilarityData = np.delete(featureSimilarityData, rowPart)

            dataArray = rfn.append_fields(
                dataArray,
                self.paths.detail_similarity,
                detailSimilarityData,
                usemask=False,
            )
            dataArray = rfn.append_fields(
                dataArray,
                self.paths.feature_similarity,
                featureSimilarityData,
                usemask=False,
            )

            dataArray[::-1].sort(
                order=[self.paths.detail_similarity, self.paths.feature_similarity]
            )

        self.listModel.setData(dataArray)

    def getPartName(self):
        index = self.partResultView.results_listParts.selectedIndexes()[0]
        partName = self.partResultView.results_listParts.model().dataItem(
            self.paths.part_id, index.row()
        )
        self.partResultView.results_dataParts.model().setDatabasePart(partName)
        self.set3DView(self.partResultView.pushButton_3DX, partName)
        self.setPics(partName)
        self.definePartOverlay(partName)

    def setFeatureTable(self):

        # part list widgets
        firstDatabasePart = self.partResultView.results_listParts.model().dataItem(
            self.paths.part_id, 0
        )
        self.tableModel.setProperties(firstDatabasePart)

        # some layout options
        self.partResultView.results_dataParts.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.NoSelection
        )
        self.partResultView.results_dataParts.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

        self.partResultView.results_dataParts.verticalHeader().setDefaultAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )

        # get feature data of parts
        condition = "|".join(
            [
                "({} == ".format(self.paths.part_id) + str(IDx) + ")"
                for IDx in self.similarParts[self.paths.part_id]
            ]
        )
        similarPartsFeaturesArray = self.featureH5.Read_table_readWhere(
            self.paths.features_table, condition
        )

        # set feature data
        self.tableModel.setData(similarPartsFeaturesArray, self.similarParts)

    def set3DView(self, button: QtWidgets.QPushButton, partID: str):

        assemblyID = "".join(partID.split("_")[:-1])
        name = partID.split("_")[-1]
        pdfPath = os.path.join(
            self.paths.path_physicaldatabase,
            assemblyID,
            name,
            name + self.paths.namedata_3d_pdf,
        )

        button.clicked.connect(lambda: self.openPdfThread(pdfPath, partID))

    def setPics(self, partID: str):
        topL = self.partResultView.label_TopX
        triL = self.partResultView.label_TrimetricX
        lefL = self.partResultView.label_LeftX
        rigL = self.partResultView.label_RightX
        if partID == self.partID:
            topL = self.partResultView.label_Top
            triL = self.partResultView.label_Trimetric
            lefL = self.partResultView.label_Left
            rigL = self.partResultView.label_Right

        assemblyID = "".join(partID.split("_")[:-1])
        name = partID.split("_")[-1]

        labelList = [lefL, rigL, topL, triL]
        for i, namePic in enumerate(
            ["_Left.jpg", "_Right.jpg", "_Top.jpg", "_Trimetric.jpg"]
        ):
            path = os.path.join(
                self.paths.path_physicaldatabase, assemblyID, name, name + namePic
            )
            pixmap = QtGui.QPixmap(path)
            pixmap = pixmap.scaled(self.PicSize, QtCore.Qt.KeepAspectRatio)
            labelList[i].setPixmap(pixmap)

    def openPdfThread(self, pdfPath: str, partID: str):
        process = self.process3DX
        if partID == self.partID:
            process = self.process3D

        process.setPath(pdfPath)
        process.start()

    def definePartOverlay(self, partID: str):
        # ptvsd.debug_this_thread()
        partData = self.tableModel.getPartData(partID)

        self.partResultView.pushButton_DebugComparedView.setEnabled(True)
        self.partResultView.pushButton_DebugComparedView.clicked.connect(
            lambda: self.debugPartOverlay(partID)
        )
        self.partResultView.pushButton_ComparedView.setEnabled(True)
        self.partResultView.pushButton_ComparedView.clicked.connect(
            lambda: self.openPartOverlay(partID)
        )

    def openPartOverlay(self, partID: str):
        # build PartInfoClass of part
        tmpPart = PartInfoClass(
            partName="Unknown", partIDstr=partID, pathClass=self.paths
        )

        # sort parts after ID
        partDict = {tmpPart.getTotalID(): tmpPart, self.partID: self.part}
        sortedID = sorted([tmpPart.getTotalID(), self.partID])

        self.overlayClass.setParts(partDict[sortedID[0]], partDict[sortedID[1]])
        self.calculatingSignal.emit(False)
        self.overlayClass.finishedSignal.connect(
            lambda: self.calculatingSignal.emit(True)
        )
        self.overlayClass.start()

    def debugPartOverlay(self, partID: str):
        # build PartInfoClass of part
        tmpPart = PartInfoClass(
            partName="Unknown", partIDstr=partID, pathClass=self.paths
        )
        self.debugOverlay.setParts(self.part, tmpPart)
        self.debugOverlay.start()


class qtModel_iconPartList(QtCore.QAbstractListModel):
    _data = np.ndarray(0)
    _data_slice = np.ndarray(0)

    def __init__(self, maxParts: int = 5):
        super().__init__()
        self.maxParts = maxParts

    def clear(self):
        self._data = np.ndarray(0)
        self._data_slice = np.ndarray(0)

    def setData(self, data: np.ndarray):
        '''np.ndarray columns = see self.paths + "images"'''
        self._data = data
        self.sliceData()

    def sliceData(self, page: int = 1):
        sliceStart = (page - 1) * self.maxParts
        self._data_slice = self._data[sliceStart : sliceStart + self.maxParts]
        self.layoutChanged.emit()

    def data(self, index, role):
        # print("i: ", index.row(), " role: ", QtCore.Qt.ItemDataRole(role))
        if role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(self._data_slice["images"][index.row()])
        # if role == QtCore.Qt.DisplayRole:
        #     return self._data_slice["PartID"][index.row()]

    def dataItem(self, column: str, row: int):
        return self._data_slice[column][row]

    def rowCount(self, index=0):
        # The length of the outer list.
        return len(self._data_slice)


class qtModel_featureTables(QtCore.QAbstractTableModel):
    _featureData = np.ndarray(0)
    _similarityData = np.ndarray(0)
    _cols_featureData = {}
    _cols_similarityData = {}
    _dataPartImported = np.ndarray(0)
    _dataPartDatabase = np.ndarray(0)
    _dataOutputDict = {}
    _rows = []
    _headers = []

    def __init__(self, partIDSelected: str, paths: PathsClass):
        super().__init__()
        self.paths = paths
        self.partIDSelected = partIDSelected
        self._headers = ["Part Database", "Part Imported"]

    def setProperties(self, partIDDatabase: str):
        self.partIDDatabase = partIDDatabase

    def clear(self):
        self._featureData = np.ndarray(0)
        self._dataPartImported = np.ndarray(0)
        self._dataPartDatabase = np.ndarray(0)
        self._dataOutputDict = {}
        self._rows = []

    def setData(self, featureData: np.ndarray, similiarityData: np.ndarray):
        self._featureData = featureData
        self._similarityData = similiarityData

        self._cols_featureData = featureData.dtype.fields
        self._cols_similarityData = similiarityData.dtype.fields

        self._rows = list(self._featureData.dtype.names)
        self.__defineRows__()

        self.decodedFeaturePartIDs = np.char.decode(
            self._featureData[self.paths.part_id], "utf-8"
        )
        self.decodedSimilarityPartIDs = np.char.decode(
            self._similarityData[self.paths.part_id], "utf-8"
        )

        self._dataPartImported = self.getPartData(self.partIDSelected)
        self.setDatabasePart(self.partIDDatabase)

    def __defineRows__(self):
        self._rows.insert(2, self.paths.detail_similarity)
        self._rows.insert(3, self.paths.feature_similarity)

    def setDatabasePart(self, partIDDatabase: str):
        self.partIDDatabase = partIDDatabase
        self._dataPartDatabase = self.getPartData(self.partIDDatabase)
        self._dataOutputDict = {0: self._dataPartDatabase, 1: self._dataPartImported}
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            rowName = self._rows[index.row()]
            data = self._dataOutputDict[index.column()][rowName][0]
            if type(data) == np.bytes_:
                data = data.decode("utf-8")
            elif (
                rowName == self.paths.detail_similarity
                or rowName == self.paths.feature_similarity
            ):
                if data == -1:
                    return "-"
                else:
                    data *= 100
                    data = round(data, 3)
                    return "{}%".format(data)
            else:
                data = round(data, 3)
            return str(data)
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() == 0:
                return int(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._headers[section])
            if orientation == QtCore.Qt.Vertical:
                return str(self._rows[section])

    def getPartData(self, partID: str) -> np.ndarray:
        rowPart_featureData = np.where(self.decodedFeaturePartIDs == partID)[0][0]
        rowPart_similarityData = np.where(self.decodedSimilarityPartIDs == partID)[0][0]

        outputArray = self._featureData[rowPart_featureData]

        similarityDataPart = self._similarityData[rowPart_similarityData]
        for col in self._cols_similarityData.keys():
            if not col in self._cols_featureData:
                outputArray = rfn.append_fields(
                    outputArray, col, [similarityDataPart[col]], usemask=False
                )

        return outputArray

    def rowCount(self, index=0):
        return len(self._rows)

    def columnCount(self, index=0):
        return 2
