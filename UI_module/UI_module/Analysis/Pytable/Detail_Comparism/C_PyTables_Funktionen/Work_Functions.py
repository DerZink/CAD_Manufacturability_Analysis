# -*- coding: utf-8 -*-
"""
@author: Zink
"""
import C_PyTables_Funktionen.utility  # Problem with file utility which delivers the Part ID, where is is in this specific situation? --- Copied FIle to this location
import os
import time
import csv
import C_PyTables_Funktionen.Pytables_Class
from tables import *
import numpy as np

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Work_Functions_Class():

    # Write Table or Array depending on Tableinfo set in Group_Class
    def Write_Data(self, Groupname, Tablename, CSV_File):

        if next(iter(self.groups_dict[Groupname])).table_dict[Tablename].type == "Array":
            self.__Write_Array_Data(Groupname, Tablename, next(
                iter(self.groups_dict[Groupname])).table_dict[Tablename].name, CSV_File)

        elif next(iter(self.groups_dict[Groupname])).table_dict[Tablename].type == "Table":
            # Grouppath, Tablepath, CSV_File
            self.__Write_Table_Data(Groupname, Tablename, CSV_File)

        else:
            print("Error: Table_Type not set")

    def __Write_Array_Data(self, Groupname, Tablename, Arrayname, CSV_File):

        pytables_file = open_file(self.HDF5_Path, mode="a")
        with open(CSV_File, 'rU') as File:
            csv_input = csv.reader(File, delimiter=";")
            dataarray_current_column_new_list = []
            for i, row in enumerate(csv_input):
                for j, item in enumerate(row):
                    if str(item).replace("ï»¿", "").replace(" ", "") != "":
                        # This is a list now # map(int,str(item).replace(" ","").split(","))
                        dataarray_current_column = str(
                            item).replace(" ", "").split(",")

                        for element in dataarray_current_column:
                            dataarray_current_column_new_list.append(
                                int(element))
            try:
                pytables_file.create_array(self.root+Groupname, Arrayname, dataarray_current_column_new_list, next(
                    iter(self.groups_dict[Groupname])).table_dict[Tablename].type)
            except NodeError:
                print("Array '{}' already exists".format(Arrayname))
        pytables_file.close()

    def Read_Array(self, Groupname, Arrayname):
        pytables_file = open_file(self.HDF5_Path, mode="r")
        pytables_array = pytables_file.get_node(
            self.root+Groupname+self.root+Arrayname)
        data_array = pytables_array.read()
        pytables_file.close()
        return data_array

    # def read_data_from_HDF5(self,_Part_ID,_Table_Data):
    #    ## _Table_Data= 0_[1_[path_Table1, name_ausgabe_Table1,
    #    ##                      2_[
    #    ##                          3_[root1+blatt1,liste_ausgaben_spalten]_3,
    #    ##                          3_[root1+blatt2,liste_ausgaben_spalten]_3,..roots
    #    ##                      ]_2
    #    ##                    ]_1,..HDF5_tabellen
    #    ##                  ]_0
    #    output_dict={}
    #    for table_ in _Table_Data:
    #        table_path=table_[0]
    #        table_name=table_[1]
    #        pytables_file=open_file(table_path, mode = "r")
    #        for _node in table_[2]:
    #            node=_node[0]
    #            pytables_node=pytables_file.get_node(node)
    #            id_check=pytables_node.col("ID")[_Part_ID]
    #            ## ID-Control
    #            if id_check==_Part_ID:
    #                for column in _node[1]:
    #                    item=pytables_node.col(column)[_Part_ID]
    #                    output_dict[table_name+column]=item
    #            else:
    #                print("Part_ID ({}) and Row in table_ {} are not equal, seek for Row:".format(_Part_ID,node))
    #                ## Find Row
    #                for x in pytables_node.where("ID=={}".format(_Part_ID)):
    #                    for column in _node[1]:
    #                        item=x[column]
    #                        output_dict[table_name+column]=item

    #        pytables_file.close()

    #    return output_dict

    def Read_entire_table(self, Tablepath):

        pytables_file = open_file(self.HDF5_Path, mode="r")
        pytables_node = pytables_file.get_node(Tablepath)
        tables_data = pytables_node.read()
        pytables_file.close()
        return tables_data

    def Read_single_row_table(self, Tablepath, Rownumber):  # Reads one Part

        pytables_file = open_file(self.HDF5_Path, mode="r")
        pytables_node = pytables_file.get_node(Tablepath)
        tables_row_data = pytables_node.read(Rownumber, Rownumber+1)
        pytables_file.close()
        print(tables_row_data)
        return tables_row_data

    # def write_data_in_existing_HDF5data(self,_Part_ID,_Table_Data):
    #    ## _Table_Data= 0_[1_[path_Table1,
    #    ##                      2_[
    #    ##                          3_[root1+blatt1,
    #    ##                              4_[
    #    ##                                  5_[spalten_name1,spalten_eintrag1]_5,
    #    ##                                  5_[spalten_name2,spalten_eintrag2]_5,..column
    #    ##                              ]_4
    #    ##                          ]_3,..roots
    #    ##                      ]_2,
    #    ##                    ]_1,..HDF5_tabellen
    #    ##                  ]_0
    #    for table_ in _Table_Data:
    #        table_path=table_[0]
    #        pytables_file=open_file(table_path, mode = "r+")
    #        for _node in table_[1]:
    #            node=_node[0]
    #            pytables_node=pytables_file.get_node(node)
    #            id_check=pytables_node.col("ID")[_Part_ID]
    #            list_columns=[]
    #            list_items=[]
    #            for column_items in _node[1]:
    #                list_columns.append(column_items[0])
    #                list_items.append([column_items[1]])

    #            ## ID-Control
    #            if id_check==_Part_ID:
    #                pytables_node.modify_columns(start=_Part_ID, columns=list_items, names=list_columns)
    #            else:
    #                print("Part_ID and Row are not equal, seek for Row:")
    #                ## Find Row
    #                for item in table.where("ID=={}".format(_Part_ID)):
    #                    i=0
    #                    while i <list_columns.count:
    #                        item[list_columns[i]]=list_items[i][0]
    #                        i+=1
    #                    item.update()
    #            pytables_node.flush()
    #        pytables_file.close()

    def __Write_Table_Data(self, Groupname, Tablename, CSV_File):

        pytables_file = open_file(self.HDF5_Path, "a")
        pytables_node = pytables_file.get_node(
            self.root+Groupname+self.root+Tablename)
        with open(CSV_File, 'rU') as File:
            csv_input = csv.reader(File, delimiter=";")
            column_name_list = []
            for i, row_csv in enumerate(csv_input):
                if i == 0:
                    for item in row_csv:
                        # Some stuff before ID in csv. The BOM does not work with Python 3.X, as python interprets any text as Unicode String. The BOM is not recognized within the string.
                        item = item.replace("ï»¿", "")
                        column_name_list.append(str(item))
                elif len(row_csv) != 0:
                    column = pytables_node.row
                    column["Part_ID"] = utility.generateid()
                    for j, item in enumerate(row_csv):
                        column_curr = column_name_list[j]
                        # default value of column "datum" is a byte object
                        pytables_column_curr = column[column_curr]
                        if isinstance(pytables_column_curr, (int)):
                            item_formated = int(item)
                        elif isinstance(pytables_column_curr, (float)):
                            item_formated = float(item)
                        elif isinstance(pytables_column_curr, (str)):
                            item_formated = str(item)
                        # Need to add this due to default value of StringCol in row pointer of pytables (which is b'')
                        elif isinstance(pytables_column_curr, (bytes)):
                            item_formated = str(item)
                        else:
                            print(
                                "Reading CSV: Error, unknown file format (Integer, Float, String)")
                            print("Type= {}".format(type(pytables_column_curr)))
                            print("{} = {}, Typ Pytables = {}".format(
                                column_name_list[j], item_formated, type(item_formated)))

                        column[column_curr] = item_formated
                    column.append()
            pytables_node.flush()
        pytables_file.close()
