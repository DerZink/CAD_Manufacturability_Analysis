# -*- coding: utf-8 -*-
"""
@author: Zink
"""
import csv

# cpickles
import os
import multiprocessing as mp
import time
from typing import Dict, List, Tuple

import numpy as np
from tables import *

from Analysis.Pytable.Work_Functions import Work_Functions_Class

# from Pytables_Feature_Analysis import Feature_Analysis_Class
# from Work_Functions import Work_Functions_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass


class PytableLeaf_Class:
    """Class for defining leaf structure in h5 tables"""

    def __init__(
        self,
        name: str,
        pos: int,
        type_in: str,
        csvFile: str = None,
        table_data_dtype: np.dtype = None,
    ):
        """
        name = "Table"
        pos = 1...
        type = "Table"/"Array"
        csvFile = Path to csv data (column titles used for h5 definition, no table_data_dtype necessary)
        table_data_dtype = np.dtype([(Name, numpy type, optional byte),...]) =
        np.dtype([("ID", np.int16), ("Angel", np.unicode_, 16), ("Devil", np.float64)])
        dtype see https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
        pytables see https://www.pytables.org/usersguide/datatypes.html?#id10
        """
        self.name = name  # type: str
        self.pos = pos  # type: int
        self.type = type_in  # type: str
        self.table_data_dtype = table_data_dtype  # type: Dict[str, Col]
        self.csvFile = csvFile  # type: str


class PytableGroup_Class:
    """Class for defining group structure in h5 tables"""

    def __init__(self, name: str, path: str, leafList: List[PytableLeaf_Class]):
        """
        name = name of group
        path = path to group
        leafList = list of leafes see: PytableLeaf_Class
        """
        self.name = name  # type: str
        self.path = path  # type: str
        self.type = "Group"
        self.table_dict = dict()  # type: dict[str, PytableLeaf_Class]
        # Dictionary: Key: Table_Name, Value: Table_Class
        for Table_Class in leafList:
            self.table_dict[Table_Class.name] = Table_Class


class Pytables_Write_Class(Work_Functions_Class):
    """Generate and manage PyTables Data"""

    # group_input_list is a List with Tuples: [(Group_Name, Group_Path, [Table_Class1, Table_Class2,...]),(),...

    def __init__(
        self,
        paths: PathsClass,
        name: str = None,
        part: PartInfoClass = None,
        group_input_list: List[PytableGroup_Class] = None,
    ):
        """
        "name": Name of H5-file
        "path": Path to new H5-file destination
        "csv_file": Path to CSV-File"""
        self.paths = paths
        if part != None:
            self.part = part
            self.partTotalID = part.getTotalID()
            self.lenID = len(self.partTotalID)
        ### Attributes_table ###
        self.name = getattr(self.paths, name)
        self.path = os.path.normpath(self.paths.path_analyticaldatabase)
        self.HDF5_Path = os.path.join(self.path, self.name)  # Path to New HDF5-File
        self.root = "/"
        self.copyright = "Dennis Zink"
        self.group_input_list = group_input_list
        self.checkTableName = True
        self.checkGroupName = True

    def setInputData(
        self,
        partInputList: List[PartInfoClass],
        group_input_list: List[PytableGroup_Class] = None,
    ):
        if not partInputList is None:
            self.partInputList = partInputList
            self.part = partInputList[0]
            self.partTotalID = self.part.getTotalID()
            self.lenID = len(self.partTotalID)

        if not group_input_list is None:
            self.group_input_list = group_input_list

    def partListInput(self, dataType: str) -> Dict[str, Dict[bool, str]]:
        outputDict = {}
        for part in self.partInputList:
            self.part = part
            self.partTotalID = part.getTotalID()
            self.lenID = len(self.partTotalID)

            self.__change_group_input_list(dataType)

            output = self.startInput()
            outputDict[self.partTotalID] = output

        self.closeTable()
        return outputDict

    def __change_group_input_list(self, dataType: str):
        folderPart = self.part.path_physicalDirectory

        if dataType == "Box":
            csvData_Box = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_minimalboundingbox_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.box_table
            ].csvFile = csvData_Box

        elif dataType == "Surfaces":
            self.checkTableName = False
            self.checkGroupName = False
            csvData_connected = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_surfaces_connected_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.surfaces_table_connected
            ].csvFile = csvData_connected

            csvData_NX = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_surfaces_nx_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.surfaces_table_nx
            ].csvFile = csvData_NX

            self.group_input_list[0].name = self.partTotalID

        elif dataType == "Surfaces_Distribution_perNumber":
            csvData_distribution_perNumber = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_surfaces_distribution_pernumber_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.surfaces_table_distributions
            ].csvFile = csvData_distribution_perNumber

        elif dataType == "Surfaces_Distribution_perArea":
            csvData_distribution_perArea = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_surfaces_distribution_perarea_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.surfaces_table_distributions
            ].csvFile = csvData_distribution_perArea

        elif dataType == "PointCloud":
            self.checkTableName = False
            csvData_PointCloud = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_pointcloud_csv,
            )
            PointCloudTable = PytableLeaf_Class(
                self.partTotalID, 1, "Table", csvData_PointCloud
            )
            self.group_input_list[0].table_dict = {self.partTotalID: PointCloudTable}

        elif dataType == "PointCloud_Distribution":
            csvData_distribution = self.paths.getCSVpath(
                folderPart,
                self.part.partName_physicalDatabase
                + self.paths.namedata_pointcloud_distribution_csv,
            )
            self.group_input_list[0].table_dict[
                self.paths.pointcloud_table_distributions
            ].csvFile = csvData_distribution

    def startInput(self) -> Dict[bool, str]:
        try:
            if (
                self.name != None
                and self.path != None
                and self.group_input_list != None
            ):
                self.groups_dict = dict()
                # "Item" is Tuple with Group Information of ONE Group
                for item in self.group_input_list:
                    self.groups_dict[item.name] = item

                self.__Open_HDF5_File()  # Generate New HDF5-File
                ### Generate New File with new Groups and new Tables ###
                for group_name in self.groups_dict.keys():
                    if group_name != "":
                        self.__Make_Groups(group_name)  # Generate New Group
                    groupData = self.groups_dict[group_name].table_dict
                    for table_name in groupData.keys():
                        # Generate New Table ### (Table_Name, Table_Path)
                        leafClass = groupData[table_name]
                        self.__Make_Table(leafClass, self.root + group_name)
                        # Write CSV Data to H5 Table
                        if leafClass.csvFile != None:
                            self.Write_Data(group_name, table_name, leafClass.csvFile)
                            # self.Create_Feature_Table(leafClass.csvFile) --> extra class

            self.pytables_file.flush()
            return {True: "All good"}
        except ValueError as err:
            print("Drin: {}, {}".format(self.name, err))
            return {False: str(err)}

    ####### Management Functions #######
    def __Open_HDF5_File(self):
        try:
            if os.path.isfile(self.HDF5_Path):
                self.__openFile__("a")
                return
            if os.path.isdir(self.path) == False:
                os.makedirs(self.path)
            self.pytables_file = open_file(
                self.HDF5_Path, mode="w", title=self.name.replace(".h5", "")
            )
            self.pytables_file.root._v_attrs.Created_on = "{}_{}_{}".format(
                time.localtime()[0:3][0],
                time.localtime()[0:3][1],
                time.localtime()[0:3][2],
            )
            self.pytables_file.root._v_attrs.Copyright = self.copyright
            self.pytables_file.root._v_attrs.Root = self.root
            self.pytables_file.root._v_attrs.Filename = self.name
        except:
            raise ValueError("Table {} could not be build".format(self.name))

    def __Get_AttributesFromCSV(self, csvFile: str) -> Dict[str, Col]:
        with open(csvFile, "rU") as File:
            # can only deliver strings
            csv_input = csv.reader(File, delimiter=";")
            column_name_list = []
            column_type_list = []
            for i, row_csv in enumerate(csv_input):
                if i == 0:
                    for item in row_csv:
                        item = item.replace("ï»¿", "")
                        column_name_list.append(str(item))
                elif i == 1:
                    for j, item in enumerate(row_csv):
                        if column_name_list[j] == self.paths.date:
                            column_type_list.append(StringCol(itemsize=24, pos=j + 1))
                        else:
                            try:
                                item = float(item)
                                # (int(j), Float64Col(pos=j)))
                                column_type_list.append(Float64Col(pos=j + 1))
                            except:
                                try:
                                    item = str(item)
                                    if item == "âˆž":  # infinity
                                        column_type_list.append(Float64Col(pos=j + 1))
                                    else:
                                        column_type_list.append(
                                            StringCol(itemsize=30, pos=j + 1)
                                        )
                                except:
                                    raise ValueError(
                                        "Error defining Table with CSV: no valid type, Item = {}".format(
                                            item
                                        )
                                    )
            # insert ID of part for every csv defined table
            if not "ID" in column_name_list:
                column_name_list.insert(0, self.paths.part_id)
                column_type_list.insert(0, StringCol(itemsize=self.lenID, pos=0))
            # {Column_Name:Column_Type,...}
            column_property_dict = dict(list(zip(column_name_list, column_type_list)))
        return column_property_dict

    def __Make_Table(self, leafClass: PytableLeaf_Class, Tablepath):

        if leafClass.type == "Table":

            table_existing = False
            if self.checkTableName:
                for node in self.pytables_file.iter_nodes(Tablepath):
                    if leafClass.name == node._v_name and node._v_title == "Table":
                        table_existing = True
                        break

            if table_existing == False:
                # self.pytables_file = open_file(self.HDF5_Path, mode="a")
                try:
                    # "table_data_dtype" set in H5 Call
                    if leafClass.table_data_dtype != None:
                        self.pytables_file.create_table(
                            Tablepath,
                            leafClass.name,
                            leafClass.table_data_dtype,
                            leafClass.type,
                        )  # Create Table(Tablepath, Tablename, Column Description, Type (which is table)
                    else:
                        colsFromCSV = self.__Get_AttributesFromCSV(leafClass.csvFile)
                        self.pytables_file.create_table(
                            Tablepath, leafClass.name, colsFromCSV, leafClass.type
                        )  # Use own "column_property_dict"
                except ValueError as err:
                    raise err
            else:
                pass

    def __Make_Groups(self, Groupname: str):

        try:
            # self.pytables_file = open_file(self.HDF5_Path, mode="a")
            group_existing = False
            # Grouppath
            # for node in self.pytables_file.iter_nodes(next(iter(self.groups_dict[Groupname])).path):
            if self.checkGroupName:
                for node in self.pytables_file.iter_nodes(
                    self.groups_dict[Groupname].path
                ):
                    if Groupname == node._v_name and node._v_title == "Group":
                        group_existing = True
                        break
            if group_existing == False:
                self.pytables_file.create_group(
                    self.groups_dict[Groupname].path,
                    Groupname,
                    self.groups_dict[Groupname].type,
                )  # Grouppath, Groupname, Type
            else:
                pass

        except:
            raise ValueError("Group {} could not be build".format(Groupname))


class Pytables_Read_Class(Work_Functions_Class):
    """Read PyTables Data"""

    def __init__(self, paths: PathsClass, name: str):
        self.paths = paths
        ### Attributes_table ###
        self.name = getattr(self.paths, name)
        self.path = os.path.normpath(self.paths.path_analyticaldatabase)
        self.HDF5_Path = os.path.join(self.path, self.name)
        ### Open file ###
        self.status = self.__openFile__("r")


class Pytables_Update_Class(Work_Functions_Class):
    """Update PyTables Data"""

    def __init__(self, paths: PathsClass, name: str, pytables_file: File = None):
        self.paths = paths
        ### Attributes_table ###
        self.name = getattr(self.paths, name)
        self.path = os.path.normpath(self.paths.path_analyticaldatabase)
        self.HDF5_Path = os.path.join(self.path, self.name)
        ### Open file ###
        if pytables_file is None:
            self.status = self.__openFile__("a")
        else:
            self.pytables_file = pytables_file

    def updateTable(
        self,
        tablePath: str,
        resultColumn: str,
        results: List,
        parts: List[PartInfoClass],
    ):

        listInput = False
        if type(results) == list and len(results) == len(parts):
            listInput = True

        if self.checkNodeExistence(tablePath):
            self.H5table = self.pytables_file.get_node(
                self.root + tablePath
            )  # type: Table
            if self.H5table._v_title == "Table":

                rows_Parts = self.indexNewParts(parts)
                if listInput:
                    for i, row in enumerate(rows_Parts):
                        self.H5table.cols._f_col(resultColumn)[row] = results[i]
                else:
                    self.H5table.cols._f_col(resultColumn)[rows_Parts] = results[0]
                self.H5table.flush()

    def updateOrAppend(
        self,
        tablePath: str,
        results: Dict[str, object],
        parts: List[object],
        standardValues: Dict[str, object],
    ) -> List[PartInfoClass]:
        """results = Dict of column and results {c1 : [r1, r2..], c2:[r1, r2..], ..},
        parts = list of parts as IDs or PartInfoClass
        standardValues = Dict of standard values for each column"""

        listInput = False
        for key in results.keys():
            if type(results[key]) == list and len(results[key]) == len(parts):
                listInput = True
            break

        if self.checkNodeExistence(tablePath):
            self.H5table = self.pytables_file.get_node(
                self.root + tablePath
            )  # type: Table
            if self.H5table._v_title == "Table":
                for i, part in enumerate(parts):
                    partID = part
                    if type(part) == PartInfoClass:
                        partID = part.getTotalID()
                    row = self._findRow(self.H5table, partID)
                    if not row is None:
                        for colRes in results.keys():
                            if listInput:
                                self.H5table.cols._f_col(colRes)[row] = results[colRes][
                                    i
                                ]
                            else:
                                self.H5table.cols._f_col(colRes)[row] = results[colRes]

                    else:
                        newRow = self.H5table.row
                        for col in standardValues.keys():
                            if col == self.paths.part_id:
                                newRow[col] = partID
                            elif not col in results:
                                newRow[col] = standardValues[col]
                            elif col in results:
                                if listInput:
                                    newRow[col] = results[col][i]
                                else:
                                    newRow[col] = results[col]
                        newRow.append()
                    self.H5table.flush()

    def appendTable(self, tablePath: str, data: np.ndarray):
        """data = structured array with matching columns"""
        if self.checkNodeExistence(tablePath):
            self.H5table = self.pytables_file.get_node(
                self.root + tablePath
            )  # type: Table
            self.H5table.append(data)
            self.H5table.flush()

    def indexNewParts(
        self, partList: List[PartInfoClass]
    ) -> Tuple[List[int], List[int]]:
        partIDs = [x.getTotalID() for x in partList]  # type: List[str]

        conditionStr = ""
        for partID in partIDs:
            conditionStr += "({} == b'{}') | ".format(self.paths.part_id, partID)
        conditionStr = conditionStr[:-3]
        rows_newParts = self.H5table.get_where_list(conditionStr)
        return rows_newParts
