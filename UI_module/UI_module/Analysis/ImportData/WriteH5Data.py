# -*- coding: utf-8 -*-
"""
Writing in H5 files
"""
import multiprocessing as mp
import os
import shutil
from typing import Dict, List, Tuple

# import ptvsd
import csv

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import Signal, Slot
from tables import *

from Analysis.Pytable.Pytables_Feature_Analysis import Feature_Input_Class
from Analysis.Pytable.Pytables_Management_Functions import (
    PytableGroup_Class,
    PytableLeaf_Class,
    Pytables_Write_Class,
    Pytables_Read_Class,
)
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass


class WriteH5Data(QtCore.QObject):
    """Class for writing H5 data (PyTables)
        Input:
                - Global paths as PathsClass
                - Similarity features"""

    outputImportError = Signal(str)

    def __init__(
        self,
        pathsInput: PathsClass,
        featureColumns: List[Tuple[str, float]],
        partInputList: List[PartInfoClass],
    ):
        super().__init__()
        # input
        self.paths = pathsInput
        self.featureColumns = featureColumns  # type: List[Tuple[str, float]]
        self.similarity_class = False  # If similarity table was build
        self.partInputList = partInputList

        self.box_class = Pytables_Write_Class(self.paths, "boxdata_h5")
        self.surfaces_class = Pytables_Write_Class(self.paths, "surfacesdata_h5")
        self.surfaces_distNr_class = Pytables_Write_Class(
            self.paths, "surfacesdistribution_pernumber_h5"
        )
        self.surfaces_distAr_class = Pytables_Write_Class(
            self.paths, "surfacesdistribution_perarea_h5"
        )
        self.pointCloud_class = Pytables_Write_Class(self.paths, "pointclouddata_h5")
        self.pointCloud_dist_class = Pytables_Write_Class(
            self.paths, "pointclouddistribution_h5"
        )

        self.feature_class = Feature_Input_Class(self.paths, "similarity_h5")

    def start(self):
        if len(self.partInputList) > 0:
            self.set_Tables()
            self.run()

    def set_Tables(self):
        self.part0 = self.partInputList[0]

        self._readData_Box()
        self._readData_Surfaces()
        self._readData_Surfaces_Distribution_perNumber()
        self._readData_Surfaces_Distribution_perArea()
        self._readData_PointCloud()
        self._readData_PointCloud_Distribution()

    @Slot(str)
    def run(self):

        self.poolh5Writing = mp.Pool(6)

        # Box
        box_pool = self.poolh5Writing.apply_async(
            self.box_class.partListInput, args=("Box",)
        )

        # Surfaces data
        surfaces_pool = self.poolh5Writing.apply_async(
            self.surfaces_class.partListInput, args=("Surfaces",)
        )

        # Surfaces distribution per number
        surfaces_distNr_pool = self.poolh5Writing.apply_async(
            self.surfaces_distNr_class.partListInput,
            args=("Surfaces_Distribution_perNumber",),
        )

        # Surfaces distribution per area
        surfaces_distAr_pool = self.poolh5Writing.apply_async(
            self.surfaces_distAr_class.partListInput,
            args=("Surfaces_Distribution_perArea",),
        )

        # PointCloud data
        pointCloud_pool = self.poolh5Writing.apply_async(
            self.pointCloud_class.partListInput, args=("PointCloud",)
        )

        # PointCloud distribution
        pointCloud_dist_pool = self.poolh5Writing.apply_async(
            self.pointCloud_dist_class.partListInput, args=("PointCloud_Distribution",)
        )

        self.poolh5Writing.close()
        self.poolh5Writing.join()

        # get output
        o_Box = box_pool.get()
        o_Surface = surfaces_pool.get()
        o_Surfaces_Distribution_perNumber = surfaces_distNr_pool.get()
        o_Surfaces_Distribution_perArea = surfaces_distAr_pool.get()
        o_PointCloud = pointCloud_pool.get()
        o_PointCloud_Distribution = pointCloud_dist_pool.get()

        outputMsg_dict = {True: {}, False: {}}
        for part_key in o_Box.keys():
            status = True
            for outputDict in [
                (o_Box, "Box"),
                (o_Surface, "Surfaces"),
                (o_Surfaces_Distribution_perNumber, "Surface distribution per Number"),
                (o_Surfaces_Distribution_perArea, "Surface distribution per Area"),
                (o_PointCloud, "Point Cloud"),
                (o_PointCloud_Distribution, "Point Cloud distribution"),
            ]:
                if False in outputDict[0][part_key]:
                    status = False
                    outputMsg_dict[False].update(
                        {part_key: (outputDict[0][part_key][False], outputDict[1])}
                    )
                    break
            if status == True:
                outputMsg_dict[True].update({part_key: "All good"})

        # transform part list to dict
        partInputDict = {}
        for partClass in self.partInputList:
            partInputDict[partClass.getTotalID()] = partClass

        # check if something went wrong
        if len(outputMsg_dict[False]) > 0:
            "something went wrong"
            parts2Clear = []
            for failedPart in outputMsg_dict[False].keys():
                msg, calcType = outputMsg_dict[False][failedPart]
                self.outputImportError.emit(
                    "Problem: Imported data of part {} are corrupted. All H5 entries well be deleted.\nImport type: {}\n Message {}".format(
                        failedPart, calcType, msg
                    )
                )
                parts2Clear.append(partInputDict[failedPart])
            self.clearPartData(parts2Clear)

        # proceed the good parts
        if len(outputMsg_dict[True]) > 0:
            "all good -> make feature table"
            parts2Feature = []
            for calcedPart in outputMsg_dict[True].keys():
                parts2Feature.append(partInputDict[calcedPart])

            self._FeatureTable(parts2Feature)

    def close(self):
        self.box_class.closeTable()
        self.surfaces_class.closeTable()
        self.surfaces_distNr_class.closeTable()
        self.surfaces_distAr_class.closeTable()
        self.pointCloud_class.closeTable()
        self.pointCloud_dist_class.closeTable()
        self.feature_class.closeTable()

    def _readData_Box(self):
        ###################################
        # box data
        ###################################
        # ptvsd.debug_this_thread()
        folderPart = self.part0.path_physicalDirectory

        csvData_Box = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase
            + self.paths.namedata_minimalboundingbox_csv,
        )

        BoxTable = PytableLeaf_Class(self.paths.box_table, 1, "Table", csvData_Box)

        BoxTableGroup = PytableGroup_Class("", "/", [BoxTable])

        self.box_class.setInputData(self.partInputList, [BoxTableGroup])

    def _readData_Surfaces(self):
        ###################################
        # detailed surfaces data
        ###################################
        folderPart = self.part0.path_physicalDirectory
        csvData_connected = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase
            + self.paths.namedata_surfaces_connected_csv,
        )
        connectedTableHeader = self.__readCSVHeader(csvData_connected)
        connectedTableTypeDef = [
            (np.int16),
            (bytes, 600),
            (np.float64),
            (np.int16),
            (np.int16),
            (bytes, 30),
            (bytes, 30),
        ]
        connectedTableTypes = self.__buildDtype(
            connectedTableHeader, connectedTableTypeDef
        )

        connectedTable = PytableLeaf_Class(
            self.paths.surfaces_table_connected,
            1,
            "Table",
            csvData_connected,
            connectedTableTypes,
        )

        csvData_NX = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase + self.paths.namedata_surfaces_nx_csv,
        )

        NXTableHeader = self.__readCSVHeader(csvData_NX)
        NXTableTypeDef = [
            (np.int16),
            (np.float64),
            (np.int16),
            (np.int16),
            (bytes, 600),
            (np.int16),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.float64),
            (np.int16),
            (np.int16),
            (np.int16),
            (bytes, 30),
            (bytes, 30),
        ]
        NXTableTypes = self.__buildDtype(NXTableHeader, NXTableTypeDef)

        NXTable = PytableLeaf_Class(
            self.paths.surfaces_table_nx, 1, "Table", csvData_NX, NXTableTypes
        )

        SurfacesTableGroup = PytableGroup_Class(
            self.part0.getTotalID(), "/", [connectedTable, NXTable]
        )

        self.surfaces_class.setInputData(self.partInputList, [SurfacesTableGroup])

    def _readData_Surfaces_Distribution_perNumber(self):
        ###################################
        # surfaces distribution data per number
        ###################################
        folderPart = self.part0.path_physicalDirectory

        csvData_distribution_perNumber = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase
            + self.paths.namedata_surfaces_distribution_pernumber_csv,
        )

        distributionTable_perNumber = PytableLeaf_Class(
            self.paths.surfaces_table_distributions,
            1,
            "Table",
            csvData_distribution_perNumber,
        )

        distributionTableGroup_perNumber = PytableGroup_Class(
            "", "/", [distributionTable_perNumber]
        )

        self.surfaces_distNr_class.setInputData(
            self.partInputList, [distributionTableGroup_perNumber]
        )

    def _readData_Surfaces_Distribution_perArea(self):
        ###################################
        # surfaces distribution data per area
        ###################################
        folderPart = self.part0.path_physicalDirectory

        csvData_distribution_perArea = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase
            + self.paths.namedata_surfaces_distribution_perarea_csv,
        )

        distributionTable_perArea = PytableLeaf_Class(
            self.paths.surfaces_table_distributions,
            1,
            "Table",
            csvData_distribution_perArea,
        )

        distributionTableGroup_perArea = PytableGroup_Class(
            "", "/", [distributionTable_perArea]
        )

        self.surfaces_distAr_class.setInputData(
            self.partInputList, [distributionTableGroup_perArea]
        )

    def _readData_PointCloud(self):
        ###################################
        # detailed PointCloud data
        ###################################
        folderPart = self.part0.path_physicalDirectory

        csvData_PointCloud = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase + self.paths.namedata_pointcloud_csv,
        )

        PointCloudTable = PytableLeaf_Class(
            self.part0.getTotalID(), 1, "Table", csvData_PointCloud
        )

        PointCloudTableGroup = PytableGroup_Class("", "/", [PointCloudTable])

        self.pointCloud_class.setInputData(self.partInputList, [PointCloudTableGroup])

    def _readData_PointCloud_Distribution(self):
        ###################################
        # PointCloud distribution data
        ###################################
        folderPart = self.part0.path_physicalDirectory

        csvData_distribution = self.paths.getCSVpath(
            folderPart,
            self.part0.partName_physicalDatabase
            + self.paths.namedata_pointcloud_distribution_csv,
        )

        distributionTable = PytableLeaf_Class(
            self.paths.pointcloud_table_distributions, 1, "Table", csvData_distribution
        )

        distributionTableGroup = PytableGroup_Class("", "/", [distributionTable])

        self.pointCloud_dist_class.setInputData(
            self.partInputList, [distributionTableGroup]
        )

    def clearPartData(self, partInputList: List[PartInfoClass]):

        IDs2Delete = []
        for partInput in partInputList:
            part = partInput
            IDs2Delete.append(part.getTotalID())

            # clear imported CAD data
            # shutil.rmtree(part.path_physicalDirectory)

        # clear H5 data
        self.box_class.deleteRow(self.paths.namedata_minimalboundingbox, IDs2Delete)
        self.surfaces_class.deleteNode(IDs2Delete)
        self.surfaces_distNr_class.deleteRow(
            self.paths.surfaces_table_distributions, IDs2Delete
        )
        self.surfaces_distAr_class.deleteRow(
            self.paths.surfaces_table_distributions, IDs2Delete
        )
        self.pointCloud_class.deleteNode(IDs2Delete)
        self.pointCloud_dist_class.deleteRow(
            self.paths.pointcloud_table_distributions, IDs2Delete
        )

        # else:
        #     self.box_class.deleteRow(self.paths.namedata_minimalboundingbox)
        #     self.surfaces_class.deleteNode(self.part.getTotalID())
        #     self.surfaces_distNr_class.deleteRow(
        #         self.paths.surfaces_table_distributions
        #     )
        #     self.surfaces_distAr_class.deleteRow(
        #         self.paths.surfaces_table_distributions
        #     )
        #     self.pointCloud_class.deleteNode(self.part.getTotalID())
        #     self.pointCloud_dist_class.deleteRow(
        #         self.paths.pointcloud_table_distributions
        #     )
        #     if os.path.isfile(self.paths.path_similarity_h5) == True:
        #         self.similarity_class.deleteRow(
        #             self.paths.features_table, self.part.getTotalID()
        #         )
        #         similarityNode = (
        #             self.paths.similarity_results_group + "/" + self.part.getTotalID()
        #         )
        #         self.similarity_class.deleteNode(similarityNode)

    def _FeatureTable(self, partInputList: List[PartInfoClass]):

        # get column names from preferences and asign typ float64
        # python str is in byte
        lenID = len(self.part0.getTotalID())
        featureList = [(self.paths.part_id, bytes, lenID)]
        featureList.append((self.paths.part_name, bytes, 500))
        for column in self.featureColumns:
            featureList.append((column[0], np.float64))
        dtypeFeatureColumns = np.dtype(featureList)

        featureTable = PytableLeaf_Class(
            self.paths.features_table, 1, "Table", None, dtypeFeatureColumns
        )

        columns_calibrationTable = np.dtype(
            [
                (self.paths.part_a, bytes, lenID),
                (self.paths.part_b, bytes, lenID),
                (self.paths.manufacturing_similarity_gs, np.float64),
                (self.paths.manufacturing_similarity_fs, np.float64),
            ]
        )

        calibrationTable = PytableLeaf_Class(
            self.paths.calibration_table, 3, "Table", None, columns_calibrationTable
        )

        featureTableGroup = PytableGroup_Class(
            "", "/", [featureTable, calibrationTable]
        )

        featureResultsGroup = PytableGroup_Class(
            self.paths.similarity_results_group, "/", []
        )

        self.feature_class.setInputData(
            partInputList, [featureTableGroup, featureResultsGroup]
        )

        # build tables if they don't exists
        self.feature_class.startInput()

        # get features from other tables
        self.feature_class.getFeatures(self.paths)

    def __readCSVHeader(self, csvFile: str) -> List[str]:
        column_name_list = []
        with open(csvFile, "rU") as File:
            # can only deliver strings
            csv_input = csv.reader(File, delimiter=";")
            for i, row_csv in enumerate(csv_input):
                if i == 0:
                    for item in row_csv:
                        item = item.replace("ï»¿", "")
                        column_name_list.append(str(item))
                break
        File.close()
        return column_name_list

    def __buildDtype(self, names: List[str], types: List[tuple]) -> np.dtype:
        dType_list = []
        for i, name in enumerate(names):
            type_i = types[i]
            if type(type_i) == type:
                dType_list.append((name, type_i))
            if type(type_i) == tuple:
                dType_list.append((name, type_i[0], type_i[1]))

        return np.dtype(dType_list)
