import copy
import itertools
import os
import pickle as _pi
from typing import Dict, List, Tuple

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

from Analysis.Calibration.FeatureSimilarity import CalibrationFeatureSimilarity
from Analysis.Calibration.GeometricSimilarity import CalibrationGeometricSimilarity
from Analysis.Calibration.CollectPartPairs import (
    PairLoader,
    bodyPairPermutation,
    bodyPairComparison,
    savePickledBodyPairs,
    loadPickledBodyPairs,
)
from Analysis.Calibration.GeometricSimilarityClasses.FEM_PartPairClass import (
    FEM_BodyPairClass,
)

from Analysis.Pytable.Pytables_Management_Functions import (
    Pytables_Read_Class,
    Pytables_Update_Class,
)

from GUI.UI_PartPairs import Ui_PartPairForm
from Illustration.PartsOverlay import partsOverlay_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass


class PartPairView(QtCore.QObject):
    FScalibration_done = Signal(object)
    GScalibration_done = Signal(object)

    def __init__(
        self,
        paths: PathsClass,
        featureSimilarityColumns: Dict[str, list],
        detailColumns: detailColumnsClass,
        calcPrefs: calcPrefClass,
    ):
        super().__init__()
        self.paths = paths
        self.featureSimilarityColumns = featureSimilarityColumns
        self.detailColumns = detailColumns
        self.calcPrefs = calcPrefs

        self.partPairWidget = QtWidgets.QWidget()
        self.partPairView = Ui_PartPairForm()
        self.partPairView.setupUi(self.partPairWidget)

        self.PicSize = QtCore.QSize(170, 170)

        self.FScalibration = CalibrationFeatureSimilarity(
            self.paths, self.featureSimilarityColumns
        )
        self.FScalibration.finished.connect(self.FScalibration_done.emit)

        self.GScalibration = CalibrationGeometricSimilarity(
            self.paths, self.detailColumns, copy.deepcopy(self.calcPrefs)
        )
        self.GScalibration.finished.connect(self.GScalibration_done.emit)

        self.overlayClass = partsOverlay_Class(
            self.paths, self.calcPrefs, self.detailColumns, transformation=False
        )  # type: partsOverlay_Class
        self.partPairView.pushButton_Overlay.setEnabled(False)

        self.openTable()
        self.setTables()
        self.setButtons()

    def openTable(self, calibrations=None):
        featureH5 = Pytables_Update_Class(self.paths, "similarity_h5")
        self.calibration_path = featureH5.root + self.paths.calibration_table

        if calibrations is None:
            # get saved calibration data
            columns_calibrationTable = np.dtype(
                [
                    (self.paths.part_a, bytes, self.paths.IDLength),
                    (self.paths.part_b, bytes, self.paths.IDLength),
                    (self.paths.manufacturing_similarity_gs, np.float64),
                    (self.paths.manufacturing_similarity_fs, np.float64),
                ]
            )
            featureH5.BuildOrOpenTable(
                featureH5.root, self.paths.calibration_table, columns_calibrationTable
            )

            self.calibrations = featureH5.Read_entire_table(self.calibration_path)
        else:
            self.calibrations = calibrations

        if len(self.calibrations) > 0:
            # get parts ids
            self.partIDs = list(
                np.char.decode(
                    featureH5.Read_table_column(
                        self.paths.features_table, self.paths.part_id
                    ),
                    "utf-8",
                )
            )

            # get feature data of parts
            condition = "|".join(
                [
                    "({} == b'{}')".format(self.paths.part_id, str(IDx))
                    for IDx in self.calibrations
                ]
            )
            self.calibrationPartsFeaturesArray = featureH5.Read_table_readWhere(
                self.paths.features_table, condition
            )

        featureH5.closeTable()

    def setTables(self):
        self.partPairModel = qtModel_partPairTable(self.calibrations, self.partIDs)

        self.partPairView.partPairs_tableView.setModel(self.partPairModel)
        delegate = CompleterDelegate(
            self.partPairView.partPairs_tableView, self._completerSetupFunction
        )
        self.partPairView.partPairs_tableView.setItemDelegateForColumn(0, delegate)
        self.partPairView.partPairs_tableView.setItemDelegateForColumn(1, delegate)
        self.partPairView.partPairs_tableView.setColumnWidth(0, 275)
        self.partPairView.partPairs_tableView.setColumnWidth(1, 275)
        # self.partPairView.partPairs_tableView.setColumnWidth(2, 100)

        self.partPairView.partPairs_tableView.selectionModel().selectionChanged.connect(
            self.__builtInfoWidgets__
        )

        self.additionalRows = [
            self.paths.detail_similarity,
            self.paths.feature_similarity,
            "GCd_1",
            "GCd_minmax",
            "GCn_1",
            "GCn_minmax",
            "GCcmin_1",
            "GCcmin_minmax",
            "GCcmax_1",
            "GCcmax_minmax",
        ]
        self.featureBodiesModel = qtModel_featureTable(
            self.paths, self.calibrationPartsFeaturesArray, self.additionalRows
        )
        self.partPairView.pairProperties_tableView.setModel(self.featureBodiesModel)

    def _completerSetupFunction(self, editor, index):
        completer = QtWidgets.QCompleter(self.partIDs, editor)
        completer.setCompletionColumn(0)
        completer.setCompletionRole(QtCore.Qt.EditRole)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        try:
            editor.setCompleter(completer)
        except:
            pass

    def setButtons(self):

        self.partPairView.pushButton_load.clicked.connect(self.__loadBodyPairs__)
        self.partPairView.pushButton_deleteAll.clicked.connect(
            self.partPairModel.clearData
        )
        self.partPairView.pushButton_reset.clicked.connect(self.partPairModel.resetData)
        self.partPairView.pushButton_save.clicked.connect(self.__saveSettings__)

        self.partPairView.pushButton_featureSimilarity.clicked.connect(
            lambda: self.FScalibration.start(self.getSettings())
        )

        self.partPairView.pushButton_geometricSimilarity.clicked.connect(
            lambda: self.GScalibration.start(self.getSettings())
        )

        self.partPairView.pushButton_positioning.clicked.connect(
            self.__calcSimilarities__
        )
        self.partPairView.pushButton_Overlay.clicked.connect(self.__buildOverlay__)

    def __loadBodyPairs__(self):
        openExplorer = QtWidgets.QFileDialog(self.partPairWidget)
        openExplorer.FileMode = openExplorer.Directory
        openExplorer.Option = openExplorer.ShowDirsOnly

        dirBodyPairs = os.path.normpath(
            openExplorer.getExistingDirectory(self.partPairWidget)
        )
        openExplorer.close()
        if dirBodyPairs != ".":
            bodyPairLoader = PairLoader()
            columns_calibrationTable = bodyPairLoader.columns_calibrationTable
            bodyNamesIDs, bodyClasses = bodyPairLoader.getBodiesInfos(dirBodyPairs)
            bodyPairLoader.closeTable()

            bodyPairList = bodyPairPermutation(bodyClasses)
            bodyPairResults = bodyPairComparison(self.paths, bodyPairList, bodyNamesIDs)

            bodyPairResults_array = np.core.records.fromarrays(
                np.array(bodyPairResults).transpose(), dtype=columns_calibrationTable
            )

            self.openTable(calibrations=bodyPairResults_array)
            self.partPairModel.changeData(self.calibrations, self.partIDs)

    def __saveSettings__(self):
        featureH5 = Pytables_Update_Class(self.paths, "similarity_h5")
        featureH5.Clear_Table(self.calibration_path)

        featureH5.appendTable(self.calibration_path, self.getSettings())
        featureH5.closeTable()

    def getSettings(self) -> np.ndarray:
        settings = self.partPairModel.getData()
        settingsArray = np.ndarray(len(settings), dtype=self.calibrations.dtype)
        for i, setting in enumerate(settings):
            settingsArray[i] = tuple(setting)

        return settingsArray

    def __builtInfoWidgets__(self):
        column_len = self.partPairModel.columnCount()
        index = self.partPairView.partPairs_tableView.selectedIndexes()[::column_len][0]
        row = index.row()

        self.bodyA_ID = self.partPairModel._calibrationData[row][0]
        if self.bodyA_ID != "":
            self.bodyA = PartInfoClass(partIDstr=self.bodyA_ID, pathClass=self.paths)
            picPathA = os.path.join(
                self.bodyA.path_physicalDirectory, self.bodyA.partId + "_Trimetric.jpg"
            )
            pixmapA = QtGui.QPixmap(picPathA)
            pixmapA = pixmapA.scaled(self.PicSize, QtCore.Qt.KeepAspectRatio)
            self.partPairView.label_BodyA.setPixmap(pixmapA)
            self.featureBodiesModel.setBody(self.bodyA_ID, "Body A")

        self.bodyB_ID = self.partPairModel._calibrationData[row][1]
        if self.bodyB_ID != "":
            self.bodyB = PartInfoClass(partIDstr=self.bodyB_ID, pathClass=self.paths)
            picPathB = os.path.join(
                self.bodyB.path_physicalDirectory, self.bodyB.partId + "_Trimetric.jpg"
            )
            pixmapB = QtGui.QPixmap(picPathB)
            pixmapB = pixmapB.scaled(self.PicSize, QtCore.Qt.KeepAspectRatio)
            self.partPairView.label_BodyB.setPixmap(pixmapB)
            self.featureBodiesModel.setBody(self.bodyB_ID, "Body B")

        self.partPairView.pairProperties_tableView.resizeColumnsToContents()

        if self.bodyA_ID != "" and self.bodyB_ID != "":
            self.partPairView.pushButton_Overlay.setEnabled(True)
        else:
            self.partPairView.pushButton_Overlay.setEnabled(False)

    def __calcSimilarities__(self):
        A_features, y_features = self.FScalibration.getSavedConfiguration()
        x_features = np.array([1.0 / A_features.shape[1]] * A_features.shape[1])
        featureSimilarityValues = A_features.dot(x_features)

        self.GScalibration.calibrationData = self.getSettings()
        self.GScalibration.__getPartPairs__()
        x_geometric = np.array([0.25, 0.25, 0.25, 0.25, 1, 1, 1, 1, 1, 1, 1])
        geometricSimilarityValues = self.GScalibration.calcGSvalues(x_geometric)

        GS_BodyPairclass_list = self.GScalibration.GS_BodyPairclass_list
        similarityValues = {}
        for i, bodyPair in enumerate(self.GScalibration.calibrationData):
            GS_BodyPairclass = GS_BodyPairclass_list[i]
            GCd_min, GCd_1, GCd_max = self.__minMaxVal_GeometricCharacteristic__(
                GS_BodyPairclass.GC_d_array
            )
            GCn_min, GCn_1, GCn_max = self.__minMaxVal_GeometricCharacteristic__(
                GS_BodyPairclass.GC_n_array
            )
            (
                GCcmin_min,
                GCcmin_1,
                GCcmin_max,
            ) = self.__minMaxVal_GeometricCharacteristic__(
                GS_BodyPairclass.GC_cmin_array
            )
            (
                GCcmax_min,
                GCcmax_1,
                GCcmax_max,
            ) = self.__minMaxVal_GeometricCharacteristic__(
                GS_BodyPairclass.GC_cmax_array
            )

            valDict = {
                self.additionalRows[0]: (
                    geometricSimilarityValues[i],
                    geometricSimilarityValues[i],
                ),
                self.additionalRows[1]: (
                    featureSimilarityValues[i],
                    featureSimilarityValues[i],
                ),
                self.additionalRows[2]: (GCd_1, GCd_1),
                self.additionalRows[3]: (GCd_min, GCd_max),
                self.additionalRows[4]: (GCn_1, GCn_1),
                self.additionalRows[5]: (GCn_min, GCn_max),
                self.additionalRows[6]: (GCcmin_1, GCcmin_1),
                self.additionalRows[7]: (GCcmin_min, GCcmin_max),
                self.additionalRows[8]: (GCcmax_1, GCcmax_1),
                self.additionalRows[9]: (GCcmax_min, GCcmax_max),
            }

            similarityValues[(bodyPair[0], bodyPair[1])] = valDict

        self.featureBodiesModel.setSimilarityValues(similarityValues)

    def __minMaxVal_GeometricCharacteristic__(self, values: np.ndarray):
        numberOfPoints = len(values)
        valGC_min = len(values[values == 1]) / numberOfPoints
        valGC_1 = np.sum(values ** 1) / numberOfPoints
        valGC_max = len(values[values > 0]) / numberOfPoints
        return valGC_min, valGC_1, valGC_max

    def __buildOverlay__(self):
        if self.bodyA_ID != "" and self.bodyB_ID != "":
            self.overlayClass.setParts(self.bodyA, self.bodyB)
            self.overlayClass.start()


class CompleterDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, completerSetupFunction=None):
        super().__init__(parent)
        self._completerSetupFunction = completerSetupFunction

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        self._completerSetupFunction(editor, index)
        return editor

    def setEditorData(self, editor, index):
        super().setEditorData(editor, index)

    def closeEditor(self, editor, hint=None):
        super().closeEditor(editor, hint)

    def commitData(self, editor):
        super().commitData(editor)


class qtModel_partPairTable(QtCore.QAbstractTableModel):
    def __init__(self, partPairs: np.ndarray, partIDs: List[str]):
        super().__init__()
        self._headers = ["Body A", "Body B", "Geometric", "Feature"]

        self.partIDs = set(partIDs)
        self._calibrationData = []
        self.partPairs = partPairs
        self.fillData(self.partPairs)
        self.checkLastRow()

    def changeData(self, partPairs: np.ndarray, partIDs: List[str]):
        self.partIDs = set(partIDs)
        self.partPairs = partPairs
        self.fillData(self.partPairs)
        self.checkLastRow()

    def fillData(self, partPairs: np.ndarray):
        tableHeaders = partPairs.dtype.names
        for partPair in partPairs:
            dataList = [
                partPair[tableHeaders[0]].decode("utf-8"),
                partPair[tableHeaders[1]].decode("utf-8"),
                partPair[tableHeaders[2]],
                partPair[tableHeaders[3]],
            ]
            self._calibrationData.append(dataList)
        self.layoutChanged.emit()

    def getData(self) -> List:
        _calibrationDataOut = []
        for data in self._calibrationData:
            if not "" in data:
                _calibrationDataOut.append(data)
        return _calibrationDataOut

    def clearData(self):
        self._calibrationData = []
        self.checkLastRow()

    def resetData(self):
        self._calibrationData = []
        self.fillData(self.partPairs)
        self.checkLastRow()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        value = value.replace(" ", "")
        valueSave = ""
        if index.column() > 1:
            try:
                if value != "":
                    valueSave = float(value)
                    valueSave /= 100
                    if valueSave > 1.0:
                        valueSave = 1.0
                    elif valueSave < 0.0:
                        valueSave = 0.0
            except:
                return False
        else:
            if value in self.partIDs:
                valueSave = value
        self._calibrationData[index.row()][index.column()] = valueSave
        if value == "":
            deleteStatus = True
            for col in self._calibrationData[index.row()]:
                if col != "":
                    deleteStatus = False
                    break
            if deleteStatus == True:
                del self._calibrationData[index.row()]
                self.layoutChanged.emit()
        self.checkLastRow()
        return True

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsSelectable
        )

    def checkLastRow(self):
        if len(self._calibrationData) == 0:
            self._calibrationData.append([""] * len(self._headers))
            self.layoutChanged.emit()
        elif (
            self._calibrationData[-1][0] != ""
            and self._calibrationData[-1][1] != ""
            and self._calibrationData[-1][2] != ""
            and self._calibrationData[-1][3] != ""
        ):
            self._calibrationData.append([""] * len(self._headers))
            self.layoutChanged.emit()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            dataOutput = self._calibrationData[index.row()][index.column()]
            if index.column() > 1 and type(dataOutput) != str:
                data = round(dataOutput * 100, 1)
                return "{}%".format(data)
            return str(dataOutput)
        # if role == QtCore.Qt.TextAlignmentRole:
        #     if index.column() == 0:
        #         return int(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._headers[section])
            if orientation == QtCore.Qt.Vertical:
                return str(section)

    def rowCount(self, index=0):
        return len(self._calibrationData)

    def columnCount(self, index=0):
        return len(self._headers)


class qtModel_featureTable(QtCore.QAbstractTableModel):
    _featureData = np.ndarray(0)
    _similarityData = np.ndarray(0)
    _cols_featureData = {}
    _cols_similarityData = {}
    _dataPartImported = np.ndarray(0)
    _dataPartDatabase = np.ndarray(0)
    _dataOutputDict = {}
    _rows = []
    _headers = []

    def __init__(
        self, paths: PathsClass, featureData: np.ndarray, additionalRows: List[str]
    ):
        super().__init__()
        self.paths = paths
        self._headers = ["Body A", "Body B"]
        self._featureData = featureData
        self.additionalRows = additionalRows
        self.additionalRowsSet = set(self.additionalRows)
        self.__setData__()
        self.BodyACol = None
        self.BodyBCol = None

    def setBody(self, bodyID: str, col: str):
        dataRow = np.where(self.decodedFeaturePartIDs == bodyID)[0][0]
        data = self._featureData[dataRow]
        if col == "Body A":
            self.BodyACol = data
        if col == "Body B":
            self.BodyBCol = data

        self.layoutChanged.emit()

    def setSimilarityValues(self, valueDict: Dict[Tuple[str, str], Dict]):
        self.similarityValues.update(valueDict)

    def __setData__(self):

        self._cols_featureData = self._featureData.dtype.fields

        self._rows = list(self._featureData.dtype.names)[1:]
        self.__defineRows__()

        self.decodedFeaturePartIDs = np.char.decode(
            self._featureData[self.paths.part_id], "utf-8"
        )

        self.similarityValues = {}
        emptyRows = ()
        for ID in self.decodedFeaturePartIDs:
            self.similarityValues[ID] = ("-", "-")

    def __defineRows__(self):
        for i, row in enumerate(self.additionalRows):
            self._rows.insert(i + 1, row)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            rowName = self._rows[index.row()]
            data = None

            if rowName in self.additionalRowsSet:
                if self.BodyACol is None or self.BodyBCol is None:
                    return ""
                IDkey = (
                    self.BodyACol[self.paths.part_id],
                    self.BodyBCol[self.paths.part_id],
                )
                if not IDkey in self.similarityValues:
                    return "-"
                else:
                    valDict = self.similarityValues[IDkey]
                    data = valDict[rowName][index.column()]
                    data *= 100
                    data = round(data, 3)
                    return "{}%".format(data)

            elif index.column() == 0:
                if self.BodyACol is None:
                    return ""
                else:
                    data = self.BodyACol[rowName]
            elif index.column() == 1:
                if self.BodyBCol is None:
                    return ""
                else:
                    data = self.BodyBCol[rowName]
            if type(data) == np.bytes_:
                data = data.decode("utf-8")
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

    def rowCount(self, index=0):
        return len(self._rows)

    def columnCount(self, index=0):
        return 2
