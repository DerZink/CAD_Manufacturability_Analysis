import os

# os.environ["QT_API"] = "PySide2"
import sys

import matplotlib

from PySide2 import QtCore, QtGui, QtWidgets

import numpy as np

# QT_API = "PySide2" manipulated C:\Miniconda3\Lib\site-packages\matplotlib\backends\qt_compat.py with:
# # Manipulation Zink2020
# if "PyQt5.QtCore" in sys.modules:
#     del sys.modules["PyQt5.QtCore"]

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2.QtCore import Signal, Slot

from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from GUI.UI_OverviewFile import Ui_OverviewForm
from Illustration.PartResults import PDFViewerClass
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class OverviewView(QtCore.QObject):
    buildingFinished = Signal(object)
    featureH5 = None

    def __init__(
        self,
        paths: PathsClass,
        calcPrefs: calcPrefClass,
        part: PartInfoClass,
        mainWidget_databaseTab: QtWidgets.QWidget,
    ):
        super().__init__()
        self.paths = paths
        self.calcPrefs = calcPrefs
        self.part = part
        self.partID = self.part.getTotalID()
        self.assemblyID = self.part.assemblyId
        self.name = self.part.partId

        # self.mainWidget_databaseTab = mainWidget_databaseTab
        self.partOverviewWidget = QtWidgets.QWidget()
        self.partOverviewView = Ui_OverviewForm()
        self.partOverviewView.setupUi(self.partOverviewWidget)

        self.setImages()
        self.setDataList()
        self.setHistogram()

    def setImages(self):
        PicSize = self.partOverviewView.label_Top.size()
        topL = self.partOverviewView.label_Top
        triL = self.partOverviewView.label_Trimetric
        lefL = self.partOverviewView.label_Left
        rigL = self.partOverviewView.label_Right

        labelList = [lefL, rigL, topL, triL]
        for i, namePic in enumerate(
            ["_Left.jpg", "_Right.jpg", "_Top.jpg", "_Trimetric.jpg"]
        ):
            path = os.path.join(
                self.paths.path_physicaldatabase,
                self.assemblyID,
                self.name,
                self.name + namePic,
            )
            pixmap = QtGui.QPixmap(path)
            pixmap = pixmap.scaled(PicSize, QtCore.Qt.KeepAspectRatio)
            labelList[i].setPixmap(pixmap)

    def setDataList(self):

        self.featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")

        # get feature data of parts
        condition = "{} == b'{}'".format(self.paths.part_id, self.partID)

        featureData = self.featureH5.Read_table_readWhere(
            self.paths.features_table, condition
        )

        self.dataModel = qtModel_partData(featureData)

        # some layout options
        self.partOverviewView.tableView_partData.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.NoSelection
        )
        self.partOverviewView.tableView_partData.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

        self.partOverviewView.tableView_partData.verticalHeader().setDefaultAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
        )

        self.partOverviewView.tableView_partData.setModel(self.dataModel)

    def setHistogram(self):

        self.placeholder = self.partOverviewView.label_histograms
        if self.part.statusFeatureAnalysis == "Done":
            featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")
            similarityResultsPart_path = (
                self.featureH5.root
                + self.paths.similarity_results_group
                + self.featureH5.root
                + self.partID
            )
            similarityData = featureH5.Read_table_column(
                similarityResultsPart_path, self.paths.feature_similarity
            )

            featureH5.closeTable()

            lableSize = (
                self.partOverviewView.label_histograms.size()
            )  # type: QtCore.QSize

            self.placeholder = qtClass_Matplotlib(
                self.partOverviewWidget, lableSize.width(), lableSize.height()
            )
            self.placeholder.compute_initial_figure(similarityData)

        else:
            self.placeholder.setText("No Feature Similarity calculated so far")
            self.partOverviewView.label_xHistogram.setText("")
        self.partOverviewView.gridLayout.addWidget(self.placeholder, 1, 0, 1, 1)

    def close(self):
        if not self.featureH5 is None:
            self.featureH5.closeTable()


class qtModel_partData(QtCore.QAbstractTableModel):
    _data = np.ndarray(0)
    _rows = []

    def __init__(self, data: np.ndarray):
        super().__init__()
        self.clear()
        self._data = data
        self._rows = data.dtype.names

    def clear(self):
        self._data = np.ndarray(0)
        self._rows = []

    def data(self, index, role):
        # print("i: ", index.row(), " role: ", QtCore.Qt.ItemDataRole(role))
        if role == QtCore.Qt.DisplayRole:
            rowName = self._rows[index.row()]
            data = self._data[rowName][0]
            if type(data) == np.bytes_:
                data = data.decode("utf-8")
            else:
                data = round(data, 3)
            return str(data)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return "Data"
            if orientation == QtCore.Qt.Vertical:
                return str(self._rows[section])

    def rowCount(self, index=0):
        # The length of the outer list.
        return len(self._rows)

    def columnCount(self, index=0):
        return 1


class qtClass_Matplotlib(FigureCanvas):
    def __init__(self, parent: QtWidgets.QWidget = None, width=5, height=4, dpi=100):
        self.parent = parent

        self.fontUI = self.parent.font()  # type: QtGui.QFont
        self.fig = Figure(
            figsize=(self.pix2inch(width, dpi), self.pix2inch(height, dpi)), dpi=dpi
        )
        # self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.15, right=1, top=1, wspace=0, hspace=0)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(self.parent)
        FigureCanvas.setMinimumSize(self, width, height)
        FigureCanvas.setSizePolicy(
            self,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )

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

        xValues = np.arange(0.0, 1.2, 0.2)
        self.axes.set_xticks(xValues)
        self.axes.set_xticklabels(
            ["{:,.0%}".format(x) for x in xValues], fontdict=fontDictUI
        )
        yTicks = self.axes.get_yticks()
        yStep = int(len(yTicks - 1) / 3)
        self.axes.set_yticks(yTicks[1:-1][::yStep])
        self.axes.set_yticklabels(
            ["{:,.0f}".format(y) for y in yTicks[1:-1][::yStep]], fontdict=fontDictUI
        )
        for yPos in yTicks[1:-1][::yStep]:
            self.axes.axhline(yPos, xmin=0, xmax=0.95, color="grey", lw=1)

    def update(self):

        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self, data: np.ndarray):

        self.axes.hist(data, histtype="step", ec="black")
        self.layoutOptions()
        self.update()

    def pix2inch(self, pix: float, dpi: int = 100):
        return pix / dpi
