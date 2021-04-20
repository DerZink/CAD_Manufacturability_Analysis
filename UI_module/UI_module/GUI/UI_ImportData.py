# -*- coding: utf-8 -*-
"""
Import CAD data and save in H5
"""
import os
import math
import copy
import sys
from typing import List, Tuple
import time
import numpy as np

# import ptvsd

from PySide2 import QtCore, QtGui
from PySide2.QtCore import Signal, Slot, QModelIndex

from Analysis.ImportData.CAD_MainImport import (
    AssemblyDecomposition,
    Build3DPDFs,
    ImportCADData,
    dummy,
)
from Analysis.ImportData.WriteH5Data import WriteH5Data
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class ImportClass(QtCore.QObject):
    """Class for managing Import of CAD data"""

    freezeStatusUI = Signal(bool)
    updateDatabase = Signal(bool)
    deletePartsFromList = Signal(list)
    outputMsg = Signal(str)

    def __init__(
        self,
        pathsInput: PathsClass,
        calcPrefs: calcPrefClass,
        partInputList: List[PartInfoClass],
        featureColumns: List[Tuple[str, str]],
    ):
        super().__init__()
        self.paths = pathsInput
        self.calcPrefs = calcPrefs
        self.partInputList = partInputList
        self.featureColumns = featureColumns

    def start(self):
        self.handleHugeImport()

    def __packageGenerator__(
        self, partList_in: List[PartInfoClass], processes: int = 1
    ) -> List[List[PartInfoClass]]:
        nrOfCPUsPerPart = int(os.cpu_count() / processes)
        nrOfCPUPackages = int(math.ceil(len(partList_in) / nrOfCPUsPerPart))
        partListPackages = [0] * nrOfCPUPackages
        for p in range(nrOfCPUPackages):
            partList = partList_in[nrOfCPUsPerPart * p : nrOfCPUsPerPart * (p + 1)]
            partListPackages[p] = partList

        return partListPackages

    def handleHugeImport(self):

        self.globalPartListPackages = []
        self.maxPartsInLoop = 6
        if len(self.partInputList) > self.maxPartsInLoop:
            processes = os.cpu_count() / self.maxPartsInLoop
            self.globalPartListPackages = self.__packageGenerator__(
                self.partInputList, processes
            )
        else:
            self.globalPartListPackages.append(self.partInputList)

        self.numberOfglobalPartListPackages = len(self.globalPartListPackages)
        self.globalPartListPackagePosition = 0

        self.outputMsg.emit(
            "Analyze part package {} of {}".format(
                self.globalPartListPackagePosition + 1,
                self.numberOfglobalPartListPackages,
            )
        )

        self.partPackagesAssembly(
            self.globalPartListPackages[self.globalPartListPackagePosition]
        )

    def partPackagesAssembly(self, globalPartListPackage: List[PartInfoClass]):

        self.partCountAssembly = len(globalPartListPackage)
        self.partListPackagesAssembly = self.__packageGenerator__(
            globalPartListPackage, 1
        )
        self.numberOfPackagesAssembly = len(self.partListPackagesAssembly)
        self.packagePositionAssembly = 0

        self.importThreadsAssemblyDecomposition = []
        self.partListFromAssemblyDecomposition = []
        self.assemblyWorker(self.packagePositionAssembly)

    def assemblyWorker(self, position: int):

        self.partCountPackageAssembly = len(self.partListPackagesAssembly[position])
        self.pdfBuilderClass = Build3DPDFs(self.paths, self.calcPrefs)
        self.pdfBuilderClass.finishedSignal.connect(self.finishAssemblyStep)
        self.pdfBuilderClass.outputMsg.connect(self.outputMsg.emit)

        for part in self.partListPackagesAssembly[position]:

            self.outputMsg.emit(
                "Assembly decomposition of {} with ID {} started.".format(
                    part.partName, part.assemblyId
                )
            )
            # put every part on a own QThread and save them in a list
            # for import CAD Data in parallel
            importThreadAssembly = QtCore.QThread(parent=self)
            importCADAssemblyDecomposition = AssemblyDecomposition(
                self.paths, part, self.calcPrefs
            )
            importCADAssemblyDecomposition.moveToThread(importThreadAssembly)
            importCADAssemblyDecomposition.errorSignal.connect(self.errorSignalAssembly)
            importCADAssemblyDecomposition.partListSignal.connect(self.collectParts)
            self.importThreadsAssemblyDecomposition.append(
                (importThreadAssembly, importCADAssemblyDecomposition)
            )
            importThreadAssembly.started.connect(importCADAssemblyDecomposition.run)
            importThreadAssembly.start()

    @Slot(list)
    def collectParts(self, partList_in: List[PartInfoClass]):
        self.partCountAssembly -= 1
        self.partCountPackageAssembly -= 1
        self.partListFromAssemblyDecomposition.extend(partList_in)
        if len(partList_in) > 0:
            self.outputMsg.emit(
                "Assembly decomposition of {} with ID {} finished.".format(
                    partList_in[0].partName, partList_in[0].assemblyId
                )
            )
            # self.pdfBuilderClass.start(partList_in)
            self.pdfBuilderClass.statusFinished = True

        self.finishAssemblyStep()

    @Slot(list)
    def errorSignalAssembly(self, Msg: str):
        self.partCountAssembly -= 1
        self.partCountPackageAssembly -= 1
        self.outputMsg.emit(Msg)

        self.finishAssemblyStep()

    def finishAssemblyStep(self):
        # ptvsd.debug_this_thread()
        if (
            self.partCountPackageAssembly == 0
            and self.packagePositionAssembly < self.numberOfPackagesAssembly - 1
            and self.pdfBuilderClass.statusFinished == True
        ):
            self.packagePositionAssembly += 1
            for it in range(len(self.importThreadsAssemblyDecomposition)):
                self.importThreadsAssemblyDecomposition[0][0].quit()
                self.importThreadsAssemblyDecomposition[0][0].wait()

            time.sleep(2.0)
            print("clear importThreadsAssemblyDecomposition")
            self.importThreadsAssemblyDecomposition = []
            self.assemblyWorker(self.packagePositionAssembly)

        if self.partCountAssembly == 0 and self.pdfBuilderClass.statusFinished == True:
            self.outputMsg.emit(
                "Assembly decomposition of package {} finished".format(
                    self.globalPartListPackagePosition + 1
                )
            )
            for it in range(len(self.importThreadsAssemblyDecomposition)):
                self.importThreadsAssemblyDecomposition[0][0].quit()
                self.importThreadsAssemblyDecomposition[0][0].wait()

            time.sleep(2.0)
            print("del importThreadsAssemblyDecomposition")
            del self.importThreadsAssemblyDecomposition
            if len(self.partListFromAssemblyDecomposition) > 0:
                self.partPackagesAnalysis()
            else:
                self.outputMsg.emit("No part output from Assembly decomposition")

    def partPackagesAnalysis(self):

        self.partListAnalysis = []

        self.partCountAnalysis = len(self.partListFromAssemblyDecomposition)
        self.partListPackagesAnalysis = self.__packageGenerator__(
            self.partListFromAssemblyDecomposition, 3
        )
        self.numberOfPackagesAnalysis = len(self.partListPackagesAnalysis)
        self.packagePositionAnalysis = 0

        self.partListFromAnalysis = []
        self.importThreadsAnalysis = []
        self.AnalysisWorker(self.packagePositionAnalysis)

    def AnalysisWorker(self, position: int):
        self.outputMsg.emit(
            "Analysis package {} of {}.".format(
                position + 1, self.numberOfPackagesAnalysis
            )
        )
        self.partCountPackageAnalysis = len(self.partListPackagesAnalysis[position])
        for part in self.partListPackagesAnalysis[position]:
            self.outputMsg.emit("CAD analysis of {} started.".format(part.getTotalID()))
            # put every part on a own QThread an save them in a list
            # for import CAD Data in parallel
            importThreadAnalysis = QtCore.QThread(parent=self)
            importCADAnalysis = ImportCADData(self.paths, part, self.calcPrefs)
            importCADAnalysis.moveToThread(importThreadAnalysis)
            importCADAnalysis.errorSignal.connect(self.errorSignalAnalysis)
            importCADAnalysis.partListSignal.connect(self.catchAnalysisResults)
            importCADAnalysis.picFailSignal.connect(self.outputMsg.emit)
            self.importThreadsAnalysis.append((importThreadAnalysis, importCADAnalysis))
            importThreadAnalysis.started.connect(importCADAnalysis.run)
            importThreadAnalysis.start()

    @Slot(object)
    def catchAnalysisResults(self, part_in: PartInfoClass):
        self.partCountAnalysis -= 1
        self.partCountPackageAnalysis -= 1
        self.partListAnalysis.append(part_in)
        self.outputMsg.emit("CAD analysis of {} finished.".format(part_in.getTotalID()))

        self.finishAnalysisStep()

    @Slot(str)
    def errorSignalAnalysis(self, Msgs: List[str]):
        self.partCountAnalysis -= 1
        self.partCountPackageAnalysis -= 1
        for Msg in Msgs:
            self.outputMsg.emit(Msg)

        self.finishAnalysisStep()

    def finishAnalysisStep(self):

        if (
            self.partCountPackageAnalysis == 0
            and self.packagePositionAnalysis < self.numberOfPackagesAnalysis - 1
        ):
            self.deletePartsFromList.emit(
                self.partListPackagesAnalysis[self.packagePositionAnalysis]
            )
            self.packagePositionAnalysis += 1
            for it in range(len(self.importThreadsAnalysis)):
                self.importThreadsAnalysis[0][0].quit()
                self.importThreadsAnalysis[0][0].wait()
                time.sleep(0.5)

            print("clear importThreadsAnalysis")
            self.importThreadsAnalysis = []
            self.AnalysisWorker(self.packagePositionAnalysis)

        if self.partCountAnalysis == 0:

            self.deletePartsFromList.emit(
                self.partListPackagesAnalysis[self.packagePositionAnalysis]
            )
            # collect features
            writeDataClass = WriteH5Data(
                self.paths, self.featureColumns, self.partListAnalysis
            )
            writeDataClass.outputImportError.connect(self.outputMsg.emit)
            writeDataClass.start()

            self.updateDatabase.emit(True)

            for it in range(len(self.importThreadsAnalysis)):
                self.importThreadsAnalysis[0][0].quit()
                self.importThreadsAnalysis[0][0].wait()
                time.sleep(0.5)

            print("del importThreadsAnalysis")
            del self.importThreadsAnalysis

            if (
                self.globalPartListPackagePosition
                < self.numberOfglobalPartListPackages - 1
            ):
                self.globalPartListPackagePosition += 1
                self.outputMsg.emit(
                    "Analyze part package {} of {}".format(
                        self.globalPartListPackagePosition + 1,
                        self.numberOfglobalPartListPackages,
                    )
                )
                self.partPackagesAssembly(
                    self.globalPartListPackages[self.globalPartListPackagePosition]
                )

            else:
                self.outputMsg.emit("Analyzed CAD Data of all selected parts")
                self.freezeStatusUI.emit(False)


class GetSelectedParts(QtCore.QObject):
    selectionFinished = Signal(tuple)
    outputSignal = Signal(str)

    def __init__(
        self,
        tableModel: QtGui.QStandardItemModel,
        selectionPackages: np.ndarray,
        paths: PathsClass,
    ):
        super().__init__()
        self.tableModel = tableModel
        self.selectionPackages = selectionPackages
        self.paths = paths
        self.selectionThreads = []
        self.partList = []
        self.partSet = set()

    def start(self):
        self.packageCount = len(self.selectionPackages)
        for selection in self.selectionPackages:
            selectionThread = QtCore.QThread()
            selectionThread.quit()
            selectCADs = PartSelector(self.tableModel, selection, self.paths)
            selectCADs.moveToThread(selectionThread)
            selectCADs.errorSignal.connect(self.threadMsg)
            selectCADs.partListSignal.connect(self.startImport)
            self.selectionThreads.append((selectionThread, selectCADs))
            selectionThread.started.connect(selectCADs.run)
            selectionThread.start()

    @Slot(object)
    def startImport(self, partTuple):
        self.packageCount -= 1
        self.partList.extend(partTuple[0])
        self.partSet.update(partTuple[1])
        if self.packageCount == 0:
            del self.selectionThreads
            self.selectionFinished.emit((self.partList, self.partSet))

    @Slot(object)
    def threadMsg(self, msg):
        self.outputSignal.emit("Reading CAD import data failed: {}".format(msg))


class PartSelector(QtCore.QObject):

    partListSignal = Signal(object)
    errorSignal = Signal(object)

    def __init__(
        self,
        tableModel: QtGui.QStandardItemModel,
        indexPackage: List[QModelIndex],
        paths: PathsClass,
    ):
        try:
            super().__init__()
            self.tableModel = tableModel
            self.indexPackage = indexPackage
            self.paths = paths
        except:
            self.errorSignal.emit(sys.exc_info())

    @Slot()
    def run(self):
        try:
            self.partList = []
            self.partIDsSet = set()
            for index in self.indexPackage:
                row_i = index.row()
                tmpPart = PartInfoClass(
                    self.tableModel.item(row_i, 1).text(),
                    self.tableModel.item(row_i, 0).text(),
                    self.tableModel.item(row_i, 2).text(),
                    self.tableModel.item(row_i, 3).text(),
                    self.tableModel.item(row_i, 3).text(),
                )
                tmpPart.defineOutputPaths(self.paths)
                self.partList.append(tmpPart)
                self.partIDsSet.add(tmpPart.assemblyId)
            self.partListSignal.emit((self.partList, self.partIDsSet))
            self.thread().quit()

        except:
            self.errorSignal.emit(sys.exc_info())
            self.thread().quit()
