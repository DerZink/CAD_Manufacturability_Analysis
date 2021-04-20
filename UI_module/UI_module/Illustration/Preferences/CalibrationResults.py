import copy
import os
from typing import Dict, List
import copy
import pickle as _pi

import matplotlib as mpl
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

from Analysis.Calibration.FeatureSimilarity import CalibrationFeatureSimilarity
from Analysis.Calibration.GeometricSimilarity import CalibrationGeometricSimilarity

from Analysis.Evaluation.DetailSimilarityClasses.PartPairClass import GS_PartPairclass
from GUI.UI_CalibrationResult import Ui_CalibrationResult
from Shared.Paths import PathsClass
from Shared.Preferences import PreferencesClass, calcPrefClass, detailColumnsClass


class CalibrationResultFS(QtCore.QObject):
    def __init__(
        self,
        paths: PathsClass,
        featureSimilarityColumns: Dict[str, list],
        A: np.ndarray = None,
        y: np.ndarray = None,
        x: np.ndarray = None,
    ):
        super().__init__()
        self.paths = paths
        self.featureSimilarityColumns = featureSimilarityColumns

        self.calibrationResultWidget = QtWidgets.QWidget()
        self.calibrationResultView = Ui_CalibrationResult()
        self.calibrationResultView.setupUi(self.calibrationResultWidget)

        self.scatterWidget = self.calibrationResultView.plot_Residual
        self.histogramWidget = self.calibrationResultView.plot_Histogram

        self.FScalibration = CalibrationFeatureSimilarity(
            self.paths, self.featureSimilarityColumns
        )
        self.savedPreferences = PreferencesClass()

        self.A = A
        self.y = y
        self.x = x
        self.xOld = None

        if self.A is None or self.y is None:
            self.A, self.y = self.FScalibration.getSavedConfiguration()

        if self.y.shape[0] > 0:
            self.__readSavedX__()
            self.__buildScatterPlot__()
            self.__buildHistogramPlot__()
            self.__buildTableView__()
            self.__defineButtons__()

        self.__layout__()

    def __readSavedX__(self):
        self.savedFeatureColumns = (
            self.savedPreferences.getFeatureColumns()
        )  # type: List[Tuple[str, str]]
        self.savedfeatureWeights = {
            f[0]: float(f[1]) for f in self.savedFeatureColumns
        }  # type: Dict[str, str]

        x = np.empty(self.FScalibration.numberOfFeatures)
        if self.FScalibration.type == "majorCategories":
            for category in self.featureSimilarityColumns:
                if not "value" in category:
                    value_cat = 0
                    for featureCat in self.featureSimilarityColumns[category]:
                        value_cat += self.savedfeatureWeights[featureCat]
                    self.savedfeatureWeights[category] = min(
                        1.0, value_cat / len(self.featureSimilarityColumns[category])
                    )

        for i, cat in enumerate(self.FScalibration.featuresList):
            valCat = self.savedfeatureWeights[cat] / self.FScalibration.numberOfFeatures
            # safety first for the boundary values 0.0 & 1.0 with min max function
            x[i] = max(0.0, min(1.0, valCat))

        if self.x is None:
            self.x = x
        else:
            self.xOld = x

    def __buildScatterPlot__(self):
        xData = range(1, len(self.y) + 1)
        yDataList = []
        dataNames = []

        yDataList.append(self.y)
        dataNames.append("Objective")
        yDataList.append(self.A.dot(self.x))
        dataNames.append("Result")
        if not self.xOld is None:
            yDataList.append(self.A.dot(self.xOld))
            dataNames.append("Old result")

        self.scatterWidget.hide()
        self.scatterWidget = scatterPlotWidget(
            xData,
            yDataList,
            dataNames,
            self.calibrationResultWidget,
            self.scatterWidget.size().width(),
            self.scatterWidget.size().height(),
        )
        self.calibrationResultView.gridLayout.addWidget(self.scatterWidget, 0, 0, 3, 1)

    def __buildHistogramPlot__(self):
        frequencyData = []
        dataNames = []
        frequencyData.append(np.abs(self.A.dot(self.x) - self.y))
        dataNames.append("Result")
        if not self.xOld is None:
            frequencyData.append(np.abs(self.A.dot(self.xOld) - self.y))
            dataNames.append("Old result")

        self.histogramWidget.hide()
        self.histogramWidget = histogramPlotWidget(
            frequencyData,
            dataNames,
            self.calibrationResultWidget,
            self.histogramWidget.size().width(),
            self.histogramWidget.size().height(),
        )
        self.calibrationResultView.gridLayout_4.addWidget(
            self.histogramWidget, 1, 0, 1, 3
        )

    def __buildTableView__(self):
        rows = self.FScalibration.featuresList
        cols = []
        data = []
        cols.append("Result")
        data.append(self.x)
        if not self.xOld is None:
            cols.append("Old result")
            data.append(self.xOld)

        self.dataModel = qtModel_calibrationResults(rows, cols)

        for c, data_i in enumerate(data):
            for r, value in enumerate(data_i):
                self.dataModel.setData_init(c, rows[r], value)

        self.calibrationResultView.tableView_Results.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.NoSelection
        )
        self.calibrationResultView.tableView_Results.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.calibrationResultView.tableView_Results.verticalHeader().setDefaultAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )
        self.calibrationResultView.tableView_Results.setModel(self.dataModel)
        self.dataModel.layoutChanged.connect(self.__recalcPlots__)

    def __defineButtons__(self):
        self.calibrationResultView.pushButton_undo.setEnabled(False)
        self.calibrationResultView.pushButton_save.setEnabled(False)
        if not self.xOld is None:
            self.calibrationResultView.pushButton_save.setEnabled(True)

        self.calibrationResultView.pushButton_save.clicked.connect(
            lambda: self.__saveCalibration__(self.x, False)
        )
        self.calibrationResultView.pushButton_undo.clicked.connect(
            lambda: self.__saveCalibration__(self.xOld, True)
        )

    def __saveCalibration__(self, x: np.ndarray, status: bool):
        featureNames = []
        featureValues = []

        for i, value in enumerate(x):
            catF = self.FScalibration.featuresList[i]
            valueFeature = str(value * self.FScalibration.numberOfFeatures)
            if catF in self.featureSimilarityColumns:
                for features in self.featureSimilarityColumns[catF]:
                    featureNames.append(features)
                    featureValues.append(valueFeature)
            else:
                featureNames.append(catF)
                featureValues.append(valueFeature)
        self.savedPreferences.change(["feature_columns"], featureNames, featureValues)

        self.calibrationResultView.pushButton_undo.setDisabled(False)
        self.calibrationResultView.pushButton_save.setEnabled(False)

    def __layout__(self):
        self.calibrationResultWidget.setAutoFillBackground(True)
        palette = self.calibrationResultWidget.palette()
        palette.setColor(self.calibrationResultWidget.backgroundRole(), QtCore.Qt.white)
        self.calibrationResultWidget.setPalette(palette)

    def __recalcPlots__(self):
        self.x = list(self.dataModel._data[0])
        if not self.xOld is None:
            self.xOld = list(self.dataModel._data[1])

        self.__buildScatterPlot__()
        self.__buildHistogramPlot__()


class CalibrationResultsGS(QtCore.QObject):
    def __init__(
        self,
        paths: PathsClass,
        detailColumns: detailColumnsClass,
        calcPrefs: calcPrefClass,
        GSpartPairs: List[GS_PartPairclass] = None,
        y: np.ndarray = None,
        x: np.ndarray = None,
    ):
        super().__init__()

        self.paths = paths
        self.detailColumns = detailColumns
        self.calcPrefs = calcPrefs
        self.__defineXParameters__()

        self.calibrationResultWidget = QtWidgets.QWidget()
        self.calibrationResultView = Ui_CalibrationResult()
        self.calibrationResultView.setupUi(self.calibrationResultWidget)

        self.GScalibration = CalibrationGeometricSimilarity(
            self.paths, self.detailColumns, copy.deepcopy(self.calcPrefs)
        )

        self.scatterWidget = self.calibrationResultView.plot_Residual
        self.histogramWidget = self.calibrationResultView.plot_Histogram

        self.savedPreferences = PreferencesClass()

        self.GSpartPairs = GSpartPairs
        self.y = y
        self.x = x
        self.xOld = None

        if self.GSpartPairs is None or self.y is None:
            self.GSpartPairs, self.y = self.__loadPartPairs__()
        else:
            self.__savePartPairs__()

        if not self.GSpartPairs is None:
            self.__readSavedX__()
            self.__defineGScalibration__()
            self.__buildScatterPlot__()
            self.__buildHistogramPlot__()
            self.__buildTableView__()
            self.__defineButtons__()

        self.__layout__()

    def __defineXParameters__(self):
        self.xParams = [
            "weight_point_distance_detail_calc",
            "weight_normal_angle_detail_calc",
            "weight_curv_radius_1_detail_calc",
            "weight_curv_radius_2_detail_calc",
            "exponent_d_point_distance_detail_calc",
            "exponent_d_normal_angle_detail_calc",
            "exponent_e_normal_angle_detail_calc",
            "exponent_d_curv_radius_min_detail_calc",
            "exponent_e_curv_radius_min_detail_calc",
            "exponent_d_curv_radius_max_detail_calc",
            "exponent_e_curv_radius_max_detail_calc",
        ]

    def __readSavedX__(self):
        self.savedCalcPrefs = self.savedPreferences.calculationPreferences()
        x = np.empty(len(self.xParams))
        for i, cat in enumerate(self.xParams):
            value_i = self.savedCalcPrefs.__getattribute__(cat)

            if i < 4:
                # safety first for the boundary values 0.0 & 1.0 with min max function
                x[i] = max(0.0, min(1.0, value_i))
            else:
                # and boundary values 0.0 & inf with max function
                x[i] = max(0.0, value_i)

        if self.x is None:
            self.x = x
        else:
            self.xOld = x

    def __defineGScalibration__(self):
        self.GScalibration.GS_BodyPairclass_list = self.GSpartPairs
        self.GScalibration.numberOfPartPairs = len(self.GSpartPairs)
        self.GSx = self.__calcGS_of_X__(self.x)
        if not self.xOld is None:
            self.GSxOld = self.__calcGS_of_X__(self.xOld)

    def __calcGS_of_X__(self, x) -> List[float]:
        # self.GScalibration.__resetCalcPrefs__(x)
        # self.GScalibration.__transformEachBodyB__()
        return self.GScalibration.calcGSvalues(x)

    def __buildScatterPlot__(self):
        xData = range(1, len(self.y) + 1)
        yDataList = []
        dataNames = []

        yDataList.append(self.y)
        dataNames.append("Objective")
        yDataList.append(self.GSx)
        dataNames.append("Result")
        if not self.xOld is None:
            yDataList.append(self.GSxOld)
            dataNames.append("Old result")

        self.scatterWidget.hide()
        self.scatterWidget = scatterPlotWidget(
            xData,
            yDataList,
            dataNames,
            self.calibrationResultWidget,
            self.scatterWidget.size().width(),
            self.scatterWidget.size().height(),
        )
        self.calibrationResultView.gridLayout.addWidget(self.scatterWidget, 0, 0, 3, 1)

    def __buildHistogramPlot__(self):
        frequencyData = []
        dataNames = []
        frequencyData.append(np.abs(self.GSx - self.y))
        dataNames.append("Result")
        if not self.xOld is None:
            frequencyData.append(np.abs(self.GSxOld - self.y))
            dataNames.append("Old result")
        self.histogramWidget.hide()
        self.histogramWidget = histogramPlotWidget(
            frequencyData,
            dataNames,
            self.calibrationResultWidget,
            self.histogramWidget.size().width(),
            self.histogramWidget.size().height(),
        )
        self.calibrationResultView.gridLayout_4.addWidget(
            self.histogramWidget, 1, 0, 1, 3
        )

    def __buildTableView__(self):
        rows = self.xParams
        cols = []
        data = []
        cols.append("Result")
        data.append(self.x)
        if not self.xOld is None:
            cols.append("Old result")
            data.append(self.xOld)

        self.dataModel = qtModel_calibrationResults(rows, cols)

        for c, data_i in enumerate(data):
            for r, value in enumerate(data_i):
                self.dataModel.setData_init(c, rows[r], value)

        self.calibrationResultView.tableView_Results.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.ExtendedSelection
        )
        self.calibrationResultView.tableView_Results.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.calibrationResultView.tableView_Results.verticalHeader().setDefaultAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )
        self.calibrationResultView.tableView_Results.setModel(self.dataModel)
        self.dataModel.layoutChanged.connect(self.__recalcPlots__)

    def __defineButtons__(self):
        self.calibrationResultView.pushButton_undo.setEnabled(False)
        self.calibrationResultView.pushButton_save.setEnabled(False)
        if not self.xOld is None:
            self.calibrationResultView.pushButton_save.setEnabled(True)

        self.calibrationResultView.pushButton_save.clicked.connect(
            lambda: self.__saveCalibration__(self.x, False)
        )
        self.calibrationResultView.pushButton_undo.clicked.connect(
            lambda: self.__saveCalibration__(self.xOld, True)
        )

    def __saveCalibration__(self, x: np.ndarray, status: bool):
        self.savedPreferences.change(
            ["calc_float"], self.xParams, [str(val) for val in x]
        )

        self.calibrationResultView.pushButton_undo.setDisabled(False)
        self.calibrationResultView.pushButton_save.setEnabled(False)

    def __savePartPairs__(self):
        pickleGSPairs = open(self.paths.gs_calibrationpairs, "wb")
        _pi.dump((self.GSpartPairs, self.y), pickleGSPairs, _pi.HIGHEST_PROTOCOL)
        pickleGSPairs.close()

    def __loadPartPairs__(self):
        if os.path.isfile(self.paths.gs_calibrationpairs):
            pickleGSPairs = open(self.paths.gs_calibrationpairs, "rb")
            GS_Pairs, y = _pi.load(pickleGSPairs)
            pickleGSPairs.close()
            return GS_Pairs, y
        else:
            return None, None

    def __layout__(self):
        self.calibrationResultWidget.setAutoFillBackground(True)
        palette = self.calibrationResultWidget.palette()
        palette.setColor(self.calibrationResultWidget.backgroundRole(), QtCore.Qt.white)
        self.calibrationResultWidget.setPalette(palette)

    def __recalcPlots__(self):
        self.x = list(self.dataModel._data[0])
        if not self.xOld is None:
            self.xOld = list(self.dataModel._data[1])

        self.__defineGScalibration__()
        self.__buildScatterPlot__()
        self.__buildHistogramPlot__()


class scatterPlotWidget(FigureCanvas):
    def __init__(
        self,
        x: np.ndarray,
        y: List[np.ndarray],
        dataNames: List[str],
        parent: QtWidgets.QWidget = None,
        width=5,
        height=4,
        dpi=100,
    ):

        self.x = x
        self.y = y
        self.dataNames = dataNames

        self.parent = parent

        self.fontUI = self.parent.font()  # type: QtGui.QFont
        self.fig = Figure(
            figsize=(self.pix2inch(width, dpi), self.pix2inch(height, dpi)), dpi=dpi
        )

        self.axes = self.fig.add_subplot(111)  # type: mpl.axes.Axes

        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.parent)
        FigureCanvas.setMinimumSize(self, width, height)
        FigureCanvas.setSizePolicy(
            self,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )

        self.buildPlots()
        self.layoutOptions()
        self.update()

    def layoutOptions(self):
        self.axes.spines["right"].set_visible(False)
        self.axes.spines["bottom"].set_visible(False)
        self.axes.spines["left"].set_visible(False)
        self.axes.spines["top"].set_visible(False)
        self.axes.tick_params(axis="x", which="both", length=0)

        fontDictUI = {
            "family": self.fontUI.family(),
            "weight": self.fontUI.weight(),
            "size": self.fontUI.pointSize(),
        }
        if fontDictUI["family"] == "MS Shell Dlg 2":
            fontDictUI["family"] = "Tahoma"

        self.axes.set_xticks([])

        yMin = 0.0  # np.floor(self.axes.dataLim.minpos[1] * 10) / 10
        yTicks = np.arange(yMin, 1.05, 0.1)
        self.axes.set_yticks(yTicks)
        self.axes.set_yticklabels(
            ["{:,.0%}".format(y) for y in yTicks], fontdict=fontDictUI
        )
        self.axes.set_ylim(top=(yTicks[-1] + (yTicks[-1] - yTicks[0]) / 100))

        self.axes.set_xlabel("Part Pairs", fontdict=fontDictUI)
        self.axes.set_ylabel("Similarity", fontdict=fontDictUI)

        self.axes.legend(framealpha=0.8, prop=fontDictUI)
        self.fig.tight_layout()

    def update(self):

        FigureCanvas.updateGeometry(self)

    def buildPlots(self):
        colorList = ["#000000", "#808080", "#D3D3D3"]
        alpha = [1.0, 0.7, 0.7]
        for i, plotName in enumerate(self.dataNames):
            self.buildScatter(self.x, self.y[i], colorList[i], alpha[i], plotName)

    def buildScatter(
        self, x: np.ndarray, y: np.ndarray, color: str, alpha: float, name: str
    ):
        self.axes.scatter(x, y, c=color, label=name, alpha=alpha)

    def pix2inch(self, pix: float, dpi: int = 100):
        return pix / dpi


class histogramPlotWidget(FigureCanvas):
    def __init__(
        self,
        frequencyData: List[np.ndarray],
        dataNames: List[str],
        parent: QtWidgets.QWidget = None,
        width=5,
        height=4,
        dpi=100,
    ):
        self.frequencyData = frequencyData
        self.dataNames = dataNames

        self.parent = parent

        self.fontUI = self.parent.font()  # type: QtGui.QFont
        self.fig = Figure(
            figsize=(self.pix2inch(width, dpi), self.pix2inch(height, dpi)), dpi=dpi
        )
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.parent)
        FigureCanvas.setMinimumSize(self, width, height)
        FigureCanvas.setSizePolicy(
            self,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )

        self.buildPlots()
        self.layoutOptions()
        self.update()

    def layoutOptions(self):
        self.axes.spines["right"].set_visible(False)
        self.axes.spines["bottom"].set_visible(False)
        self.axes.spines["left"].set_visible(False)
        self.axes.spines["top"].set_visible(False)
        self.axes.tick_params(axis="both", which="both", length=0)

        fontDictUI = {
            "family": self.fontUI.family(),
            "weight": self.fontUI.weight(),
            "size": self.fontUI.pointSize(),
        }
        if fontDictUI["family"] == "MS Shell Dlg 2":
            fontDictUI["family"] = "Tahoma"

        self.axes.set_xticks(np.arange(0.0, 1.1, 0.1))
        self.axes.set_xticklabels(
            ["{:,.0%}".format(x) for x in self.axes.get_xticks()], fontdict=fontDictUI
        )

        yTicks = np.arange(0.0, 1.1, 0.5)

        self.axes.set_yticks(yTicks)
        self.axes.set_yticklabels(
            ["{:,.0%}".format(y) for y in yTicks], fontdict=fontDictUI
        )

        self.axes.set_xlabel("Calibration Failure", fontdict=fontDictUI)
        self.axes.set_ylabel("Frequency", fontdict=fontDictUI)
        self.axes.legend(framealpha=0.8, prop=fontDictUI)
        self.fig.tight_layout()

    def update(self):

        FigureCanvas.updateGeometry(self)

    def buildPlots(self):
        colorList = ["#808080", "#D3D3D3"]
        step = 0.02
        self.xBins = list(np.round(np.arange(0 - step / 2, 1, step), 2))
        self.xBins.append(self.xBins[-1] + step)
        frequencies = []
        colors = []
        names = []
        bins = []
        for i, plotName in enumerate(self.dataNames):
            frequencies.append(self.buildHistogram(self.frequencyData[i]))
            bins.append(self.xBins[:-1])
            colors.append(colorList[i])
            names.append(plotName)
        self.stackHistogram(bins, frequencies, colors, names)

    def buildHistogram(
        self, frequencyData: np.ndarray
    ):  # , color: str, plotName: str):

        counts, bins = np.histogram(
            frequencyData, bins=self.xBins, density=True, weights=None
        )
        counts = counts / np.sum(counts)

        return counts

    def stackHistogram(
        self,
        bins: List[List[float]],
        frequencyData: List[np.ndarray],
        colors: List[str],
        plotNames: List[str],
    ):
        self.axes.hist(
            bins,
            self.xBins,
            weights=frequencyData,
            histtype="bar",
            align="mid",
            color=colors,
            label=plotNames,
        )

    def pix2inch(self, pix: float, dpi: int = 100):
        return pix / dpi


class qtModel_calibrationResults(QtCore.QAbstractTableModel):
    _data = np.ndarray(0)
    _rows = []

    def __init__(self, rows: List[str], cols: List[str]):
        super().__init__()
        self._rows = rows
        self._cols = cols

        data_columns = np.dtype([(name, np.float64) for name in self._rows])

        self._data = np.ndarray((len(self._cols),), dtype=data_columns)

    def setData_init(self, colPos: int, parameter: str, value: float):
        self._data[colPos][parameter] = value

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        value = value.replace(" ", "")
        try:
            value = float(value)
            rowName = self._rows[index.row()]
            colPos = index.column()
            self._data[colPos][rowName] = float(value)
            self.layoutChanged.emit()
            return True
        except:
            return False

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsEditable
            | QtCore.Qt.ItemIsSelectable
        )

    def data(self, index, role):
        # print("i: ", index.row(), " role: ", QtCore.Qt.ItemDataRole(role))
        if role == QtCore.Qt.DisplayRole:
            rowName = self._rows[index.row()]
            colPos = index.column()
            data = self._data[colPos][rowName]
            if type(data) == np.bytes_:
                data = data.decode("utf-8")
            else:
                data = round(data, 10)
            return str(data)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._cols[section]
            if orientation == QtCore.Qt.Vertical:
                return self._rows[section]

    def rowCount(self, index=0):
        # The length of the outer list.
        return len(self._rows)

    def columnCount(self, index=0):
        return len(self._cols)
