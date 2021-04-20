# -*- coding: utf-8 -*-
"""
@author: Zink
"""
import csv
import math
import multiprocessing as mp

# cpickles
import os
import time
from typing import List, Tuple, Dict

# import ptvsd

import numpy as np
from tables import *

from Analysis.Pytable.Pytables_Management_Functions import (
    PytableLeaf_Class,
    PytableGroup_Class,
    Pytables_Write_Class,
    Pytables_Read_Class,
    Pytables_Update_Class,
)
from Analysis.Pytable.Work_Functions import Work_Functions_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class Feature_Input_Class(Pytables_Write_Class):

    part = PartInfoClass()
    partID = str()

    def __init__(
        self,
        paths: PathsClass,
        name: str = None,
        part: PartInfoClass = None,
        group_input_list: List[PytableGroup_Class] = None,
    ):
        super().__init__(paths, name, part, group_input_list)

    def getFeatures(self, paths: PathsClass):
        self.paths = paths
        self.__openFile__("a")
        self.path_FeatureTable = self.root + self.paths.features_table
        self.featureTable = self.pytables_file.get_node(
            self.path_FeatureTable
        )  # type: Table
        self.featureTableRow = self.featureTable.row

        # open tables
        self.boxH5 = Pytables_Read_Class(self.paths, "boxdata_h5")
        self.surfaceDistH5 = Pytables_Read_Class(
            self.paths, "surfacesdistribution_perarea_h5"
        )
        self.pointCloudDistH5 = Pytables_Read_Class(
            self.paths, "pointclouddistribution_h5"
        )

        # Fill data for every new part
        for part in self.partInputList:
            self.part = part
            self.partTotalID = part.getTotalID()
            self.lenID = len(self.partTotalID)

            # get data from H5 files
            self.boxData = self.boxH5.Read_single_row_table(
                self.paths.box_table, self.partTotalID
            )
            self.surfaceData = self.surfaceDistH5.Read_single_row_table(
                self.paths.surfaces_table_distributions, self.partTotalID
            )
            self.pointCloudData = self.pointCloudDistH5.Read_single_row_table(
                self.paths.pointcloud_table_distributions, self.partTotalID
            )

            self.__fillFeatures()
            self.__calcFeatures()
            self.featureTableRow.append()
            self.featureTable.flush()

        self.boxH5.closeTable()
        self.surfaceDistH5.closeTable()
        self.pointCloudDistH5.closeTable()

        # ptvsd.debug_this_thread()

        self.SetColumnValues(
            self.paths.similarity_results_info, self.paths.feature_similarity, ["Old"]
        )

        detailExpr = "{} == b'{}'".format(self.paths.detail_similarity, "Done")
        self.Write_table_where(
            self.paths.similarity_results_info,
            detailExpr,
            [self.paths.detail_similarity],
            ["Old"],
        )

        self.closeTable()

    def __fillFeatures(self):
        """Get feature data from h5 files"""
        colsBox = set(self.boxData.dtype.names)
        colsSurface = set(self.surfaceData.dtype.names)
        colsPointCloud = set(self.pointCloudData.dtype.names)

        self.featureTableRow[self.paths.part_name] = self.part.partName

        for colname in self.featureTable.colnames:
            if colname in colsBox:
                self.featureTableRow[colname] = self.boxData[colname]
            elif colname in colsSurface:
                self.featureTableRow[colname] = self.surfaceData[colname]
            elif colname in colsPointCloud:
                self.featureTableRow[colname] = self.pointCloudData[colname]

    def __calcFeatures(self):
        """Calculation of missing feature data"""
        # area_total_box
        self.featureTableRow["area_total_box"] = 2 * (
            self.boxData["dim_box_1"] * self.boxData["dim_box_2"]
            + self.boxData["dim_box_1"] * self.boxData["dim_box_3"]
            + self.boxData["dim_box_2"] * self.boxData["dim_box_3"]
        )
        # area_part_through_box
        self.featureTableRow["area_part_through_box"] = (
            self.featureTableRow["area_total_part"]
            / self.featureTableRow["area_total_box"]
        )
        # volume_part_through_box
        self.featureTableRow["volume_part_through_box"] = (
            self.featureTableRow["volume_part"] / self.featureTableRow["volume_box"]
        )
        # distance_cog_part_box
        self.featureTableRow[
            "distance_cog_part_box"
        ] = self.__calc_distance_cog_part_box()
        # ratio_box_12
        self.featureTableRow["ratio_box_12"] = (
            self.boxData["dim_box_1"] / self.boxData["dim_box_2"]
        )
        # ratio_box_13
        self.featureTableRow["ratio_box_13"] = (
            self.boxData["dim_box_1"] / self.boxData["dim_box_3"]
        )

    def __calc_distance_cog_part_box(self) -> float:
        """ calc cog of box and distance to cog of part"""
        cog_x_box = (
            self.boxData["coordinate_p2_x"] + self.boxData["coordinate_p1_x"]
        ) / 2.0
        cog_y_box = (
            self.boxData["coordinate_p2_y"] + self.boxData["coordinate_p1_y"]
        ) / 2.0
        cog_z_box = (
            self.boxData["coordinate_p2_z"] + self.boxData["coordinate_p1_z"]
        ) / 2.0
        cog_x_part = self.boxData["cog_part_x"]
        cog_y_part = self.boxData["cog_part_y"]
        cog_z_part = self.boxData["cog_part_z"]

        euclidean_distance = math.sqrt(
            (cog_x_part - cog_x_box) ** 2
            + (cog_y_part - cog_y_box) ** 2
            + (cog_z_part - cog_z_box) ** 2
        )
        # solving zero division: 1 - (abs(part_x-part_a)/(part_a))
        if euclidean_distance < 1:
            euclidean_distance = 1
        return euclidean_distance


class Feature_Similarity_Class(Work_Functions_Class):

    pytables_file = None

    def __init__(
        self,
        partIDList: List[str],
        paths: PathsClass,
        calcPrefs: calcPrefClass,
        featureWeights: Dict[str, str],
        featureSimilarityColumns: Dict[str, list],
    ):
        """Define variables for parallel in kernel calculation of feature similarity"""
        self.partIDList = partIDList
        self.lenID = len(partIDList[0])
        self.paths = paths
        self.HDF5_Path = os.path.join(
            self.paths.path_analyticaldatabase, self.paths.similarity_h5
        )
        self.calcPrefs = calcPrefs

        # ptvsd.debug_this_thread()
        # define histogramm feature columns
        self.histrogramCategory = set()
        numberOfFeatures = 0
        numberOfHistogrammFeatures = 0
        numberOfHistogrammCategories = 0
        similarityFeaturesList = []

        for category in featureSimilarityColumns:
            features = featureSimilarityColumns[category]
            similarityFeaturesList.extend([(f, featureWeights[f]) for f in features])
            numberOfFeatures += len(features)
            if not "value" in category:
                numberOfHistogrammFeatures += len(features)
                numberOfHistogrammCategories += 1
                self.histrogramCategory.update(features)

        # calculate weight of every feature column
        # histogram values sum up to one -> equally weighting of each category is possible
        # therefore weightings of each histogram category must be equal
        # and sum of weights must not exceed number of categories
        self.weightOfCategories = 1.0 / (
            numberOfFeatures - numberOfHistogrammFeatures + numberOfHistogrammCategories
        )

        # split feature calc because of numpy restriction
        maxNumpyDim = 32  # bug or feature in numpy: only 32 dimensions possible
        nrOfFeatureLists = int(np.ceil(numberOfFeatures / maxNumpyDim))
        self.featureCalcVariablesList = np.array_split(
            similarityFeaturesList, nrOfFeatureLists
        )

    def __generateStr_referencedCalc(self, categoryTuple: Tuple[str, float]) -> str:
        pytables_calc_string = "where(abs({0} - {1}) >= {1}, 0 , (1 - abs({0} - {1}) / {1}) * {2})".format(
            categoryTuple[0],
            self.featuresPart[categoryTuple[0]],
            categoryTuple[1] * self.weightOfCategories,
        )
        return pytables_calc_string

    def __generateStr_histogramms(self, categoryTuple: Tuple[str, float]) -> str:

        pytables_calc_string = "where({0} <= {1}, {0}, {1}) * {2}".format(
            categoryTuple[0],
            self.featuresPart[categoryTuple[0]],
            categoryTuple[1] * self.weightOfCategories,
        )
        return pytables_calc_string

    def __generateCalcString(self, featureList: np.ndarray):
        calcString = ""
        for featureTuple in featureList:
            featureName = featureTuple[0]
            featureWeight = float(featureTuple[1])
            strFeature = ""
            if featureName in self.histrogramCategory:
                strFeature = self.__generateStr_histogramms(
                    (featureName, featureWeight)
                )
            else:
                strFeature = self.__generateStr_referencedCalc(
                    (featureName, featureWeight)
                )
            calcString += strFeature + " + "

        calcString = calcString[0:-3]
        return calcString

    def __generateColumnInstances(self, featureList: np.ndarray) -> Dict[str, Column]:
        columnDict = {}
        for featureTuple in featureList:
            featureName = featureTuple[0]
            columnDict[featureName] = self.featureTable.colinstances[featureName]

        return columnDict

    def runCalculation(self, listPos: int):
        self.__openFile__("r")

        self.path_FeatureTable = self.root + self.paths.features_table
        self.numberOfParts = self.getNrOfEntriesNode(self.paths.features_table)

        solutions = {}
        for partID in self.partIDList:

            self.featuresPart = self.Read_single_row_table(
                self.paths.features_table, partID
            )

            featureCalcVariables = self.featureCalcVariablesList[listPos]
            calcString = self.__generateCalcString(featureCalcVariables)

            self.featureTable = self.pytables_file.get_node(self.path_FeatureTable)
            columnsDict = self.__generateColumnInstances(featureCalcVariables)

            pytablesExpr = Expr(calcString, columnsDict)
            solutions[partID] = pytablesExpr.eval()

        self.pytables_file.close()
        return solutions

    def buildSimilarityTables(self, poolResults: List[Dict[str, np.ndarray]]):
        self.__openFile__("a")
        self.getSimilarityResults(poolResults)

        self.path_similarityGroup = self.root + self.paths.similarity_results_group

        self.columns_SimilarityTables = np.dtype(
            [
                (self.paths.part_id, bytes, self.lenID),
                (self.paths.feature_similarity, np.float64),
                (self.paths.detail_similarity, np.float64),
            ]
        )
        self.__fillNewTable()
        self.pytables_file.close()

    def updateTable(self, poolResults: List, indicesParts: List[int]):
        self.__openFile__("a")
        self.getSimilarityResults(poolResults)

        self.path_similarityGroup = self.root + self.paths.similarity_results_group

        self.columns_SimilarityTables = np.dtype(
            [
                (self.paths.part_id, bytes, self.lenID),
                (self.paths.feature_similarity, np.float64),
                (self.paths.detail_similarity, np.float64),
            ]
        )

        self.__updateExistingTable(indicesParts)
        self.pytables_file.close()

    def getSimilarityResults(self, poolResults: List[Dict[str, np.ndarray]]):

        self.numberOfParts = self.getNrOfEntriesNode(self.paths.features_table)
        self.similaritySolutions = {}

        for partID in poolResults[0].keys():
            similarityValues = np.zeros(self.numberOfParts)  # type: np.ndarray

            for solutionDict in poolResults:
                similarityValues = np.sum(
                    (similarityValues, solutionDict[partID]), axis=0
                )

            similarityValues[similarityValues > 1.0] = 1.0
            np.around(
                similarityValues,
                self.calcPrefs.digits_round_similarity,
                similarityValues,
            )

            self.similaritySolutions[partID] = similarityValues

    def __build_open_SimilarityTable(self, tableName: str) -> Table:
        return self.BuildOrOpenTable(
            self.path_similarityGroup,
            tableName,
            self.columns_SimilarityTables,
            self.numberOfParts,
        )

    def __fillNewTable(self):

        path_FeatureTable = self.root + self.paths.features_table

        featureTable = self.pytables_file.get_node(path_FeatureTable)
        partIDs_column = featureTable.col(self.paths.part_id)  # type: np.ndarray

        detailSimValues = np.full(
            self.numberOfParts, self.calcPrefs.default_detailsimilarity
        )

        for partID in self.similaritySolutions.keys():

            tablePart = self.__build_open_SimilarityTable(partID)  # type: Table
            if tablePart.nrows > 0:
                tablePart.remove_rows()
            partDataStructured = np.ndarray(
                self.numberOfParts, dtype=self.columns_SimilarityTables
            )

            partDataStructured[self.paths.part_id] = partIDs_column
            partDataStructured[
                self.paths.feature_similarity
            ] = self.similaritySolutions[partID]
            partDataStructured[self.paths.detail_similarity] = detailSimValues

            partDataStructured[::-1].sort(order=self.paths.feature_similarity)

            rowPart = np.where(
                partDataStructured[self.paths.part_id] == partID.encode()
            )[0][0]
            # set own detail value to max
            partDataStructured[self.paths.detail_similarity][rowPart] = 1

            tablePart.append(partDataStructured)
            tablePart.flush()

        self.__writeSimilarityInfoTable()

    def __writeSimilarityInfoTable(self):
        # ptvsd.debug_this_thread()
        similarityInfo = Pytables_Update_Class(
            self.paths, "similarity_h5", self.pytables_file
        )

        columns_infoTable = np.dtype(
            [
                (self.paths.part_id, bytes, self.paths.IDLength),
                (self.paths.feature_similarity, bytes, 5),
                (self.paths.detail_similarity, bytes, 5),
                (self.paths.detail_threshold, np.float),
            ]
        )

        similarityInfo.BuildOrOpenTable(
            "", self.paths.similarity_results_info, columns_infoTable
        )
        similarityInfo.pytables_file.flush()

        standardValues = {
            self.paths.part_id: "",
            self.paths.feature_similarity: "False",
            self.paths.detail_similarity: "False",
            self.paths.detail_threshold: self.calcPrefs.threshold_detail_calc,
        }

        newInfo = {
            self.paths.feature_similarity: "Done",
            self.paths.detail_similarity: "False",
        }
        similarityInfo.updateOrAppend(
            self.paths.similarity_results_info,
            newInfo,
            self.similaritySolutions.keys(),
            standardValues,
        )

    def __updateExistingTable(self, indicesParts: List[int]):

        path_FeatureTable = self.root + self.paths.features_table
        featureTable = self.pytables_file.get_node(self.path_FeatureTable)

        numberOfnewParts = len(indicesParts)
        tablePart = self.__build_open_SimilarityTable(self.partID)  # type: Table
        for i in range(numberOfnewParts):
            tablePart.row.append()
        tablePart.flush()
        tablePart.cols._f_col(self.paths.part_id)[
            -numberOfnewParts:
        ] = featureTable.read_coordinates(indicesParts, field=self.paths.part_id)
        tablePart.cols._f_col(self.paths.feature_similarity)[
            -numberOfnewParts:
        ] = self.similarityValues[indicesParts]
