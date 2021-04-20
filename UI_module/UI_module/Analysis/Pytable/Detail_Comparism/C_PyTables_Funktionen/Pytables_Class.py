# -*- coding: utf-8 -*-
"""
@author: Zink
"""
#cpickles
import os, csv, time
#import Work_Functions
import C_PyTables_Funktionen.Work_Functions as Work_Functions
from tables import *
import numpy as np

#class Table_Class(): ### Table or Array Type ###

#    def __init__(self, Property_Tuple): ### "Property_Tuple" is Tuple with Group Properties
#        self.name = Property_Tuple[0]
#        self.position = int(Property_Tuple[1])
#        self.type = "Table" #Property_Tuple[2]
#        self.array_type = "foo" #?
#        self.table_data_dict = dict() ### New Dictionary for every Column containing Table Information
#        if "Table_Data_List" in Property_Tuple:
#            list_pos = Property_Tuple.index("Table_Data_List") ### position of Table_Data_List in Property_Tuple
#            for table_tuple in Property_Tuple[list_pos]: ### for table_tuple in Table_Data_List
#                try: ### Try if Column_Type is given in Input Data, if not use own created Dict
#                    self.table_data_dict[table_tuple[0]] = {table_tuple[1], table_tuple[2]} ### dict(Column_Name) = {Position, Column_Type}
#                except:
#                    print("Error: No Table_Column_Type set")


class Pytables_Class(Work_Functions.Work_Functions_Class):

    def __init__(self, name=None, path=None, group_input_list=None, csv_file=None): ### group_input_list is a List with Tuples: [(Group_Name, Group_Path, [Table_Class1, Table_Class2,...]),(),...]

        if csv_file != None: ### CSV-File given in Pytables_Class Call --> Read CSV and make Column Dictionary
            self.__Get_Attributes_table(csv_file)

        if name != None and path != None and group_input_list != None: ### Input List in Class Call given --> Generate New File with New Groups and Tables
            ### Attributes_table ###
            self.name = name ### Name of New HDF5-File
            self.path = os.path.normpath(path) ### Path to New HDF5-File DESTINATION
            self.HDF5_Path = os.path.normpath(self.path+os.path.sep+self.name) ### Path to New HDF5-File
            self.group_input_list = group_input_list
            self.groups_dict = dict()
            for item in group_input_list: ### "Item" is Tuple with Group Information of ONE Group
                self.groups_dict[item[0]] = {self.Group_Class(item)}

            ### Attributes_common ###
            self.root = "/"
            self.copyright = "Dennis Zink"
            self.date = time.localtime()[0:3]

            ### Generate New File with new Groups and new Tables ###
            self.__Declare_HDF5_File() ### Generate New HDF5-File
            for group_name in self.groups_dict.keys():
                self.__Make_Groups(group_name) ### Generate New Group
                for table_name in next(iter(self.groups_dict[group_name])).table_dict.keys():
                    self.__Make_Table(table_name, self.root+group_name, group_name) ### Generate New Table ### (Table_Name, Table_Path)
                    self.Write_Data(group_name, table_name, csv_file)
                    
    class Group_Class(): ### Class for Folder ###

        def __init__(self, Group_information_tuple):
            self.name = Group_information_tuple[0] ### Name of Folder
            self.path = Group_information_tuple[1] ### Path to Folder
            self.type = "Group"
            self.table_dict = dict() 
            for Table_Class in Group_information_tuple[2]: ### Dictionary: Key: Table_Name, Value: Table_Class
                self.table_dict[Table_Class.name] = (Table_Class)

####### Management Functions #######

    def Read_Table(self, CSV_File): ### Get Table Names and Types ### ### Path and Name in one String to CSV-File ###
        with open(CSV_File, 'rU') as File:
            csv_input = csv.reader(File,delimiter=";") # can only deliver strings
            column_name_list = []
            column_type_list = []
            for i,row_csv in enumerate(csv_input):
                if i == 0:
                    column_name_list.append(str("Part_ID"))
                    for item in row_csv:
                        item = item.replace("ï»¿","")
                        column_name_list.append(str(item))
                elif i == 1:
                    column_type_list.append(Int64Col(pos = 0))
                    for j,item in enumerate(row_csv):
                        try: # EAFP, Easier to ask for Forgiveness than Permission
                            item = float(item)
                            column_type_list.append(Float64Col(pos=j+1))#(int(j), Float64Col(pos=j)))
                        except:
                            try:
                                item = str(item)
                                column_type_list.append(StringCol(itemsize=30, pos = j+1))#(int(j), StringCol(itemsize=30, dflt='', pos = j)))
                            except:
                                print("No valid type in CSV")

            self.column_property_dict = dict(list(zip(column_name_list,column_type_list))) ### {Column_Name:Column_Type,...}
        return self.column_property_dict

    def __Declare_HDF5_File(self):
        if os.path.isfile(self.name):
            print("File '{}' already exists".format(self.name))
            return
        print("HDF5 Databank {} is generated\n".format("\" {} \"".format(self.name)))
        if os.path.isdir(self.path)==False:
            os.makedirs(self.path)
        pytables_file=open_file(os.path.normpath(self.path+os.path.sep+self.name), mode = "w", title = self.name.replace(".h5",""))
        pytables_file.root._v_attrs.Created_on = "{}_{}_{}".format(time.localtime()[0:3][0],time.localtime()[0:3][1],time.localtime()[0:3][2])
        pytables_file.root._v_attrs.Copyright = self.copyright
        pytables_file.root._v_attrs.Root = "/"
        pytables_file.root._v_attrs.Filename = self.name
        pytables_file.close() 


    def __Get_Attributes_table(self, csv_file):
        self.Read_Table(csv_file)

    def Clear_Table_Entries(self, Tablepath): ### Tablepath here means /+Groupname+/+Tablename
        pytables_file = open_file(self.HDF5_Path, mode = "a")
        pytables_file.get_node(Tablepath).remove_rows()
        print("Deleted Table Entries from Table '{}'".format(Tablepath))
        pytables_file.close()

    def __Make_Table(self, Tablename, Tablepath, Groupnname):

        if next(iter(self.groups_dict[Groupnname])).table_dict[Tablename].type == "Table":

            pytables_file=open_file(self.HDF5_Path, mode = "a")
            try:
                pytables_file.create_table(Tablepath,Tablename, self.column_property_dict, next(iter(self.groups_dict[Groupnname])).table_dict[Tablename].type)
            except NodeError:
                print("Table '{}' already exists".format(Tablename))
            pytables_file.close()

    def __Make_Groups(self, Groupname):

        try:
            pytables_file = open_file(self.HDF5_Path, mode = "a")
            group_existing=False
            for node in pytables_file.iter_nodes(next(iter(self.groups_dict[Groupname])).path): # Grouppath
                if Groupname==node._v_name:
                    group_existing=True
            if group_existing==False:
                print("New Group {} is generated\n".format("\" {} \"".format(Groupname)))
                pytables_file.create_group(next(iter(self.groups_dict[Groupname])).path, Groupname, next(iter(self.groups_dict[Groupname])).type) # Grouppath, Groupname, Type
                pytables_file.close()
                return
            else:
                print("Group '{}' already existing".format(Groupname))
                pytables_file.close()
                return

        except:
            print("Gruppe konnte nicht erzeugt werden")
            pytables_file.close()
            return