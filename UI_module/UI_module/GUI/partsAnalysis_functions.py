from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QFileDialog

# import Shared.GlobalVariables as GV
import os
import numpy as np
import Analysis.Utility
import copy
from typing import List, Tuple, Set


def openFileNameDialog(self, file_endings: str):
    file_endingsList = file_endings.split(",")
    options = QFileDialog.Options()
    part_filter = "Part ( "
    for ending in file_endingsList:
        part_filter += "*" + ending + " "
    part_filter += ")"
    fileNames, _ = QFileDialog.getOpenFileNames(
        self.centralwidget,
        "Selection of parts to be analyzed",
        "",
        part_filter,
        options=options,
    )
    curr_date = str(Analysis.Utility.converdate(Analysis.Utility.generatedate()))

    for file_i in fileNames:
        absfilepath = file_i.rpartition("/")
        id_i = str(Analysis.Utility.generateid())
        parts_tableview_insert(self, absfilepath[2], id_i, absfilepath[0], curr_date)

    self.tableView_partsAnalysis.show()


def openDirectoryNameDialog(self, file_endings: str):
    file_endingsList = file_endings.split(",")
    # options = QFileDialog.Options()
    folder = str(
        QFileDialog.getExistingDirectory(
            self.centralwidget, "Folder of the parts to be analyzed"
        )
    )

    if len(folder) != 0:
        files_in_directory = os.listdir(folder)
        # print(files_in_directory)
        curr_date = str(Analysis.Utility.converdate(Analysis.Utility.generatedate()))
        for file_zw in files_in_directory:
            if file_zw.endswith(tuple(file_endingsList)):
                id_i = str(Analysis.Utility.generateid())
                parts_tableview_insert(self, file_zw, id_i, folder, curr_date)


def parts_tableview_insert(self, _partName, _ID, _pfad, _createDate):
    row_entry = [
        QtGui.QStandardItem(_partName),
        QtGui.QStandardItem(_ID),
        QtGui.QStandardItem(_pfad),
        QtGui.QStandardItem(_createDate),
    ]
    # needs to update (manual then uncomment)
    row_entry[0].setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
    row_entry[1].setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
    row_entry[2].setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
    row_entry[3].setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    self.model_partsAnalysis.appendRow(row_entry)


def delete_partslist(self, flag=False, partList: Set[str] = None):

    row_len = self.model_partsAnalysis.rowCount()

    # find row of part in partList
    if not flag and not partList is None:
        allIds = np.array(
            [self.model_partsAnalysis.item(row_i, 1).text() for row_i in range(row_len)]
        )
        if len(allIds) > 0 and len(partList) > 0:
            partRows = []
            for part in partList:
                row = np.where(allIds == part)[0]
                if len(row) > 0:
                    partRows.append(row[0])

            partRows.sort()
            rowCount = 0
            for partRow in partRows:
                self.model_partsAnalysis.removeRow(partRow - rowCount)
                rowCount += 1

    # clear all
    if flag:
        self.model_partsAnalysis.clear()

    self.tableView_partsAnalysis.show()
    if self.selectAll_checkBox.isChecked():
        self.selectAll_checkBox.setChecked(False)
