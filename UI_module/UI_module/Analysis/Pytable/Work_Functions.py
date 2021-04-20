# -*- coding: utf-8 -*-
"""
@author: Zink
"""
# import Pytables_Management_Functions
import csv
import os
import time

import numpy as np
from tables import *
import tables.tableextension as tableextension

from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from typing import List, Dict


class Work_Functions_Class:
    """Pytables functions: only used es subclass"""

    groups_dict = dict()
    HDF5_Path = str()
    name = str()
    root = "/"
    pytables_file = None  # type: File
    partTotalID = str()
    paths = PathsClass()
    # Write Table or Array depending on Tableinfo set in Group_Class

    def __openFile__(self, mode_in: str = "a") -> bool:
        status = False
        if self.pytables_file == None or self.pytables_file.isopen == 0:
            if os.path.isfile(self.HDF5_Path) == True:
                self.pytables_file = open_file(self.HDF5_Path, mode=mode_in)
        if self.pytables_file != None and self.pytables_file.isopen == True:
            status = True
            self.root = self.pytables_file.root._v_name
        return status

    def BuildOrOpenTable(
        self, tablePath: str, tableName: str, tableCols: np.dtype, nrOfRows: int = 10000
    ) -> Table:
        tableNamepath = tablePath + self.root + tableName
        if self.pytables_file.__contains__(tableNamepath):
            tableNode = self.pytables_file.get_node(tableNamepath)  # type: Table
            if tableName == tableNode._v_name and tableNode._v_title == "Table":
                tableNode._v_expectedrows = nrOfRows
                return tableNode

        if tablePath == "":
            tablePath = self.root
        self.pytables_file.create_table(
            tablePath, tableName, tableCols, "Table", expectedrows=nrOfRows
        )

        tableNode = self.pytables_file.get_node(tableNamepath)  # type: Table
        return tableNode

    def Write_Data(self, Groupname, Tablename, CSV_File):
        try:
            if self.__openFile__("a") == True:
                if self.groups_dict[Groupname].table_dict[Tablename].type == "Array":
                    self.Write_Array_Data(
                        Groupname,
                        Tablename,
                        self.groups_dict[Groupname].table_dict[Tablename].name,
                        CSV_File,
                    )

                elif self.groups_dict[Groupname].table_dict[Tablename].type == "Table":
                    # Grouppath, Tablepath, CSV_File
                    self.Write_Table_Data(
                        self.HDF5_Path, Groupname, Tablename, CSV_File
                    )

                else:
                    raise ValueError("Error: Table_Type not set")
        except ValueError as err:
            raise err

    def Write_Array_Data(self, Groupname, Tablename, Arrayname, CSV_File):

        # pytables_file = open_file(self.HDF5_Path, mode="a")
        with open(CSV_File, "rU") as File:
            csv_input = csv.reader(File, delimiter=";")
            dataarray_current_column_new_list = []
            for i, row in enumerate(csv_input):
                for j, item in enumerate(row):
                    if str(item).replace("ï»¿", "").replace(" ", "") != "":
                        # This is a list now # map(int,str(item).replace(" ","").split(","))
                        dataarray_current_column = str(item).replace(" ", "").split(",")

                        for element in dataarray_current_column:
                            dataarray_current_column_new_list.append(int(element))
            try:
                self.pytables_file.create_array(
                    self.root + Groupname,
                    Arrayname,
                    dataarray_current_column_new_list,
                    self.groups_dict[Groupname].table_dict[Tablename].type,
                )
            except NodeError:
                print("Array '{}' already exists".format(Arrayname))

    def Read_Array(self, Groupname, Arrayname):
        if self.__openFile__("r") == True:
            Arraypath = self.root + Groupname + self.root + Arrayname
            if self.pytables_file.__contains__(Arraypath):
                pytables_array = self.pytables_file.get_node(Arraypath)
                data_array = pytables_array.read()
                return data_array
        return None

    def Read_entire_table(self, Tablepath) -> np.ndarray:
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                tables_data = pytables_node.read()
                return tables_data
        return None

    def Read_table_column(self, Tablepath: str, ColumnName: str) -> np.ndarray:
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                return pytables_node.cols._f_col(ColumnName)[:]
        return None

    def Read_table_where(self, Tablepath: str, expr: str) -> tableextension.Row:
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                return pytables_node.where(expr)
        return None

    def Read_table_readWhere(
        self, Tablepath: str, expr: str, args: Dict = None
    ) -> np.ndarray:
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                return pytables_node.read_where(expr, condvars=args)
        return None

    def Read_table_range(self, Tablepath: str, start: int, stop: int, step: int = 1):
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                return pytables_node.read(start=start, stop=stop, step=step)
        return None

    def Write_table_where(
        self, Tablepath: str, expr: str, columns: List[str], values: List[object]
    ):
        if self.__openFile__("a") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                pytables_node = self.pytables_file.get_node(Tablepath)  # type: Table
                for row in pytables_node.where(expr):
                    for i, column in enumerate(columns):
                        row[column] = values[i]
                    row.update()
                pytables_node.flush()

    def Read_single_row_table(self, Tablepath: str, ID: str = None) -> Table.row:
        if self.__openFile__("r") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                table = self.pytables_file.get_node(Tablepath)  # type: Table
                rowNr = self._findRow(table, ID)
                if rowNr is None:
                    return None
                table_raw = table[rowNr]  # type: Table.row
                return table_raw
        return None

    def Write_Table_Data(self, HDF5_Path, Groupname, Tablename, CSV_File):
        try:
            pytables_node = self.pytables_file.get_node(
                self.root + Groupname + self.root + Tablename
            )

            with open(CSV_File, "rU") as File:
                csv_input = csv.reader(File, delimiter=";")
                column_name_list = []
                # set ID
                column = pytables_node.row
                for i, row_csv in enumerate(csv_input):
                    if i == 0:
                        for item in row_csv:
                            # Some stuff before ID in csv. The BOM does not work with Python 3.X, as python interprets any text as Unicode String. The BOM is not recognized within the string.
                            item = item.replace("ï»¿", "")
                            column_name_list.append(str(item))
                    elif len(row_csv) != 0:
                        try:
                            column[self.paths.part_id] = self.partTotalID
                        except:
                            pass
                            # if i == 1:
                            # print("Writing Data: No PartID column defined")
                        for j, item in enumerate(row_csv):
                            column_curr = column_name_list[j]
                            try:
                                # default value of column "datum" is a byte object
                                pytables_column_curr = column[column_curr]
                            except KeyError:
                                break
                            if isinstance(pytables_column_curr, (int)):
                                item_formated = int(item)
                            elif isinstance(pytables_column_curr, (float)):
                                if item == "âˆž":  # infinity
                                    item_formated = np.inf
                                else:
                                    item_formated = float(item)
                            elif isinstance(pytables_column_curr, (str)):
                                item_formated = str(item)
                            # Need to add this due to default value of StringCol in row pointer of pytables (which is b'')
                            elif isinstance(pytables_column_curr, (bytes)):
                                if column_curr == self.paths.date:
                                    item_formated = time.asctime(time.localtime())
                                else:
                                    item_formated = str(item)
                            else:
                                raise ValueError(
                                    "Reading CSV: Error, unknown file format (Integer, Float, String, Byte), type = {} ".format(
                                        type(pytables_column_curr)
                                    )
                                )
                            column[column_curr] = item_formated
                        column.append()

            pytables_node.flush()
            pytables_node._f_close()
        except ValueError as err:
            raise err

    def SetColumnValues(self, Tablepath: str, colName: str, colValue: List[object]):
        if self.__openFile__("a") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                table = self.pytables_file.get_node(Tablepath)  # type: Table
                entries = table.nrows
                data = np.array(colValue)

                if len(data) != entries:
                    data = np.full(entries, colValue[0])
                table.cols._f_col(colName)[:] = data[:]

    def getNrOfEntriesNode(self, Nodepath: str) -> int:
        if self.__openFile__("r") == True:
            Nodepath = self.root + Nodepath
            if self.pytables_file.__contains__(Nodepath):
                node = self.pytables_file.get_node(Nodepath)
                entries = node.nrows
                return entries
        return None

    def Clear_Table(self, Tablepath: str):
        """Tablepath means Groupname+/+Tablename"""
        if self.__openFile__("a") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                self.pytables_file.get_node(Tablepath).remove_rows()
                print("Deleted table entries from table '{}'".format(Tablepath))
            self.pytables_file.close()

    def deleteRow(self, Tablepath: str, IDList: List[str] = None):
        """Tablepath means Groupname+/+Tablename"""
        if self.__openFile__("a") == True:
            Tablepath = self.root + Tablepath
            if self.pytables_file.__contains__(Tablepath):
                table = self.pytables_file.get_node(Tablepath)  # type: Table
                for ID in IDList:
                    rowNr = self._findRow(table, ID)
                    if rowNr != None:
                        table.remove_rows(rowNr, rowNr + 1, 1)
                        print(
                            "Deleted table row {} from table '{}'".format(
                                rowNr, Tablepath
                            )
                        )
                    table.flush()
            self.pytables_file.close()

    def _findRow(self, table: Table, ID: str = None) -> int:
        if ID == None:
            ID = self.partTotalID
        row = table.get_where_list("{}==b'{}'".format(self.paths.part_id, ID))
        if len(row) == 0:
            return None
        return row[0]

    def checkNodeExistence(self, Node: str) -> bool:
        if self.__openFile__("a") == True:
            Nodepath = self.root + Node
            try:
                return self.pytables_file.__contains__(Nodepath)
            except:
                return False
        return False

    def deleteNode(self, NodeList: List[str]):
        if self.__openFile__("a") == True:
            for Node in NodeList:
                Nodepath = self.root + Node
                if self.pytables_file.__contains__(Nodepath):
                    self.pytables_file.remove_node(self.root, Node, True)
                    print("Deleted group {} from table '{}'".format(Node, self.name))
            self.pytables_file.close()

    def closeTable(self):
        if not self.pytables_file is None:
            self.pytables_file.close()
