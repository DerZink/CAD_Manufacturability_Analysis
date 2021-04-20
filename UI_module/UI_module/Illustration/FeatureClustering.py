import os
from typing import Dict, List, Set, Tuple

import numpy as np

# import ptvsd
# import sklearn.cluster as cluster
import tables.tableextension as tableextension
from bokeh.client import pull_session
from bokeh.embed import server_session
from numpy.lib import recfunctions as rfn
from PySide2 import QtCore, QtWebEngineWidgets, QtWidgets
from PySide2.QtCore import Signal, Slot
from tables import *

from Illustration.BokehPlotFunctions.BuildBokehPlot import BokehPlot
from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class FeaturesData:
    paths = None
    calcPrefs = None

    def setData(self, paths: PathsClass = None, calcPrefs: calcPrefClass = None):
        self.featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")
        self.similarityResultsPath = (
            self.featureH5.root + self.paths.similarity_results_group
        )

    def getFeatureData(self) -> np.ndarray:
        # get feature data of database
        return self.featureH5.Read_entire_table(self.paths.features_table)

    def getSimilarityData(self, partID: str):
        # get similarity data

        similarityResultsPart_path = (
            self.similarityResultsPath + self.featureH5.root + partID
        )

        similarParts = self.featureH5.Read_table_range(
            similarityResultsPart_path, 0, self.calcPrefs.similar_parts_diagramm
        )

        # get feature data of parts
        similarPartsFeaturesList = []
        for id_i in similarParts[self.paths.part_id]:
            row_i = self.featureH5.Read_single_row_table(
                self.paths.features_table, id_i.decode("utf-8")
            )
            similarPartsFeaturesList.append(row_i)

        similarPartsFeaturesArray = np.array(
            similarPartsFeaturesList, dtype=similarPartsFeaturesList[0].dtype
        )

        # featureDataNames_List = []
        dTypeFields = similarPartsFeaturesArray.dtype.fields
        for colName in dTypeFields:
            typeCol = dTypeFields[colName][0].type
            if typeCol != np.bytes_:
                similarParts = rfn.append_fields(
                    similarParts,
                    colName,
                    similarPartsFeaturesArray[colName],
                    usemask=False,
                )
                # featureDataNames_List.append(colName)

        return similarParts

    def getAllSimilarityData(self) -> Dict:
        self.similarityPartsDict = {}
        for tableNode in self.featureH5.pytables_file.iter_nodes(
            self.similarityResultsPath
        ):  # type: Table
            partName = tableNode.name
            nrOfRows = tableNode.nrows
            self.similarityPartsDict[partName] = np.ndarray(
                nrOfRows,
                dtype=[
                    (self.paths.part_id, np.unicode_, len(partName)),
                    (self.paths.feature_similarity, np.float64),
                    (self.paths.detail_similarity, np.float64),
                ],
            )
            self.similarityPartsDict[partName][:] = tableNode.read()

    # def calcClusters(self):
    #     self.featureData_namesTuple = self.featureData.dtype.names
    #     clusterSizes = [10]
    #     numericalData = self.featureData[
    #         list(self.featureData_namesTuple)[2:]
    #     ]  # type: np.ndarray #data without names
    #     numerialDataArray = rfn.structured_to_unstructured(
    #         numericalData, dtype=np.float64
    #     )
    #     for size in clusterSizes:
    #         kmeans = cluster.KMeans(n_clusters=size, copy_x=True)
    #         nameKmeans = "K-Means {}".format(size)
    #         groupsKmeans = kmeans.fit_predict(numerialDataArray)
    #         centroidsKmeans = kmeans.cluster_centers_

    def featureHistograms(self):

        pass

    def close(self):
        self.featureH5.closeTable()


class BokehPlot_features(QtCore.QObject, FeaturesData):

    plotBuildingPartsFinished = Signal(object)
    plotBuildingDatabaseFinished = Signal(str)

    def __init__(
        self,
        paths: PathsClass,
        calcPrefs: calcPrefClass,
        featureDetails: Dict[str, Tuple[str, str]],
    ):

        self.paths = paths
        self.calcPrefs = calcPrefs
        self.featureDetails = featureDetails
        super().__init__()

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)

    def plotPartSimilarity(
        self,
        parts: List[PartInfoClass],
        # outputWidget: QtWidgets.QTabWidget,
        recalcParts: Set[str],
    ):
        self.parts = parts
        # self.outputWidget = outputWidget
        self.recalcParts = recalcParts
        self.thread.started.connect(self.startPartSimilarity)

    def plotFeatureDatabase(self):
        self.thread.started.connect(self.startFeatureDatabase)

    @Slot(object)
    def startPartSimilarity(self):
        self.setData()
        widgetOutput = []
        for part in self.parts:
            # get data
            partID = part.getTotalID()
            outputPath = os.path.join(
                part.path_physicalDirectory, self.paths.namedata_feature_diagramm
            )
            if os.path.isfile(outputPath) == False or partID in self.recalcParts:
                dataSimilarParts = self.getSimilarityData(partID)

                self.featureDetails[self.paths.feature_similarity] = (
                    "Feature similarity (FS)",
                    "per",
                )
                self.featureDetails[self.paths.detail_similarity] = (
                    "Geometric similarity (GS)",
                    "per",
                )
                plotClassDatabase = BokehPlot(
                    self.paths, self.featureDetails, outputPath, True
                )
                plotClassDatabase.start(dataSimilarParts)

            widgetOutput.append((outputPath, part.row_db))

        self.plotBuildingPartsFinished.emit(widgetOutput)
        self.thread.quit()

    @Slot(str)
    def startFeatureDatabase(self):
        self.setData()
        # ptvsd.debug_this_thread()
        # get data
        featureDatadatabase = self.getFeatureData()

        outputPath = self.paths.path_feature_diagramm_dataset
        if os.path.isfile(outputPath) == False:
            plotClassDatabase = BokehPlot(self.paths, self.featureDetails, outputPath)
            plotClassDatabase.start(featureDatadatabase)

        self.plotBuildingDatabaseFinished.emit(outputPath)
        self.thread.quit()
