# -*- coding: utf-8 -*-
"""
Imports CAD Data
"""

import copy
import multiprocessing as mp
import os
import shutil
import time
from multiprocessing import Process
from typing import List, Tuple

from PySide2 import QtCore
from PySide2.QtCore import Signal, Slot

import Analysis.ImportData.Assembly_Function as Assembly_Function
import Analysis.ImportData.Images_Function as Images_Function
import Analysis.ImportData.Box_Function as Box_Function
import Analysis.ImportData.Surfaces_Function as Surfaces_Function
import Analysis.ImportData.PointCloud_Function as PointCloud_Function

from Illustration.Utility import PDFBuilder

# import ptvsd
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class AssemblyDecomposition(QtCore.QObject):

    partListSignal = Signal(list)
    errorSignal = Signal(str)

    def __init__(
        self, pathsInput: PathsClass, partInput: PartInfoClass, calcPrefs: calcPrefClass
    ):
        super().__init__()
        # input
        self.paths = pathsInput
        self.part = partInput
        self.calcPrefs = calcPrefs

        # part/subpart list
        self.partList = []  # type: List[PartInfoClass]
        self.partList_failed = []  # type: List[ParPartInfoClasstInfo]

    def run(self):
        """ Check if part is Assembly and save all sub parts """
        # ptvsd.debug_this_thread()
        self.statusMsg = "Problem in AssemblyDecomposition"
        self.checkAssembly = Assembly_Function.assembly_tool_class(
            self.paths, self.part, self.calcPrefs
        )
        self.checkAssembly.sig_finished.connect(self._PartCount)
        self.checkAssembly._start()

    @Slot(list)
    def _PartCount(self, exitCode):
        """ Check how many parts are saved"""
        # ptvsd.debug_this_thread()
        if exitCode == 0:
            partDirectory = self.part.path_physicalDirectory
            for folder in os.listdir(partDirectory):
                partID = folder
                part_i = copy.deepcopy(self.part)
                part_i.updateDecomposition(str(partID))
                part_i.partFormat = "prt"  # used file format is NX .prt
                self.partList.append(part_i)
            self.partListSignal.emit(self.partList)
            self.thread().quit()

        else:
            if exitCode == 2:
                self.statusMsg = "Problem in AssemblyDecomposition: timeout"
            self._failed()

    @Slot(str)
    def _failed(self):
        """all parts/subparts failed"""
        self.statusCalc = False
        # self._clearData(self.part.path_physicalDirectory)
        self.errorSignal.emit(
            "CADimport of {} failed. {} ".format(self.part.partName, self.statusMsg)
        )
        self.thread().quit()


class Build3DPDFs(QtCore.QObject):
    finishedSignal = Signal()
    outputMsg = Signal(str)

    def __init__(self, paths: PathsClass, calcPrefs: calcPrefClass):
        super().__init__()

        self.threadList = []
        self.threadpos = 0

        self.threadfinished = 0
        self.statusFinished = True

        self.assemblyIDs = []

        self.tempFolder = "Temp3DPDF"
        self.paths = paths
        self.calcPrefs = calcPrefs

    def start(self, partList_in: List[PartInfoClass]):
        self.statusFinished = False
        assemblyID = partList_in[0].assemblyId
        self.assemblyIDs.append(assemblyID)

        self.outputMsg.emit(
            "3D PDF building of assembly with ID {} started.".format(assemblyID)
        )

        assemblyPath = os.path.join(self.paths.path_physicaldatabase, assemblyID)

        calcFolder = os.path.join(assemblyPath, self.tempFolder)

        partPathList = [
            os.path.join(assemblyPath, pa_x.partId, pa_x.partId + ".prt")
            for pa_x in partList_in
        ]

        pdfThread = QtCore.QThread()
        takePDF = PDFBuilder(self.paths, self.calcPrefs, calcFolder, partPathList)

        takePDF.moveToThread(pdfThread)
        pdfThread.started.connect(takePDF._start)
        takePDF.sig_finished.connect(self.pdfFinished)
        pdfThread.start()

        self.threadList.append((pdfThread, takePDF))
        self.threadpos += 1

    def pdfFinished(self, output: Tuple[int, str]):
        self.threadfinished += 1
        # ptvsd.debug_this_thread()
        if self.threadfinished == self.threadpos:

            self.outputMsg.emit("3D PDF building finished.")

            for thread, classPDF in self.threadList:
                thread.quit()
                thread.wait()

            for assemblyID in self.assemblyIDs:
                assemblyPath = os.path.join(
                    self.paths.path_physicaldatabase, assemblyID
                )
                calcFolder = os.path.join(assemblyPath, self.tempFolder)
                partIDs = os.listdir(assemblyPath)
                for partID in partIDs:
                    pdfFile = os.path.join(calcFolder, partID + ".pdf")
                    if os.path.isfile(pdfFile):
                        newPDFPath = os.path.join(assemblyPath, partID, partID + ".pdf")
                        os.replace(pdfFile, newPDFPath)
                shutil.rmtree(calcFolder)

            del self.threadList
            self.statusFinished = True
            self.finishedSignal.emit()


class ImportCADData(QtCore.QObject):
    """Class for importing CAD data"""

    errorSignal = Signal(list)
    partListSignal = Signal(object)
    picFailSignal = Signal(str)

    def __init__(
        self, pathsInput: PathsClass, partInput: PartInfoClass, calcPrefs: calcPrefClass
    ):
        """Input:
            - Global paths as PathsClass
            - CAD part data as PartInfoClass
            - Calculationpreferences"""
        super().__init__()
        # input
        self.paths = pathsInput
        # self.part = partInput
        self.calcPrefs = calcPrefs
        # part
        self.part = partInput  # type: PartInfoClass
        self.threadCount = 3
        self.failMsgs = []
        self.picFailMsg = ""

    def run(self):
        """ Analyse parts: BoundingBox and Surface tool"""
        # ------
        importThread_box = QtCore.QThread(parent=self)
        boxTool = Box_Function.box_tool_class(self.paths, self.part, self.calcPrefs)
        boxTool.moveToThread(importThread_box)
        boxTool.sig_finished.connect(self._PointCloudAnalysis)
        importThread_box.started.connect(boxTool._start)

        # ------
        importThread_surface = QtCore.QThread(parent=self)
        surfaceTool = Surfaces_Function.surfaces_tool_class(
            self.paths, self.part, self.calcPrefs
        )
        surfaceTool.moveToThread(importThread_surface)
        surfaceTool.sig_finished.connect(self._finishedSurfaces)
        importThread_surface.started.connect(surfaceTool._start)

        # ------
        importThread_pictures = QtCore.QThread(parent=self)
        takePictures = Images_Function.images_tool_class(
            self.paths, self.part, self.calcPrefs
        )
        takePictures.moveToThread(importThread_pictures)
        takePictures.sig_finished.connect(self._finishedPictures)
        importThread_pictures.started.connect(takePictures._start)

        # -------
        self.classList = [boxTool, surfaceTool, takePictures]
        self.threadList = [
            importThread_box,
            importThread_surface,
            importThread_pictures,
        ]
        for thread_i in self.threadList:
            thread_i.start()

    @Slot(tuple)
    def _PointCloudAnalysis(self, exitMsg: Tuple[str, str]):
        self.threadCount -= 1
        if exitMsg[0] == 0:
            importThread_pointCloud = QtCore.QThread(parent=self)
            self.threadCount += 1
            pointCloud = PointCloud_Function.pointcloud_tool_class(
                self.paths, self.part, self.calcPrefs
            )
            pointCloud.moveToThread(importThread_pointCloud)
            pointCloud.sig_finished.connect(self._finishedPointCloud)
            importThread_pointCloud.started.connect(pointCloud._start)

            self.classList.append(pointCloud)
            self.threadList.append(importThread_pointCloud)
            importThread_pointCloud.start()

        else:
            self.failMsgs.append((exitMsg[1], "BoxAnalysis"))
            self._endPartAnalysis()

    @Slot(tuple)
    def _finishedSurfaces(self, exitMsg: Tuple[str, str]):
        self.threadCount -= 1
        if exitMsg[0] == 0:
            self._endPartAnalysis()
        else:
            self.failMsgs.append((exitMsg[1], "SurfacesAnalysis"))
            self._endPartAnalysis()

    @Slot(tuple)
    def _finishedPictures(self, exitMsg: Tuple[str, str]):
        self.threadCount -= 1
        if exitMsg[0] == 0:
            self._endPartAnalysis()
        else:
            self.picFailMsg = exitMsg[1]
            self._endPartAnalysis()

    @Slot(tuple)
    def _finishedPointCloud(self, exitMsg: Tuple[str, str]):
        self.threadCount -= 1
        if exitMsg[0] == 0:
            self._endPartAnalysis()
        else:
            self.failMsgs.append((exitMsg[1], "PointCloudAnalysis"))
            self._endPartAnalysis()

    @Slot(object)
    def _endPartAnalysis(self):
        if self.threadCount == 0:
            for thread_i in self.threadList:
                thread_i.quit()
                thread_i.wait()
            time.sleep(2)
            del self.threadList, self.classList
            self._checkIfFailed()

    def _checkIfFailed(self):
        """check if some calcs failed"""
        self.resultCheck()
        if len(self.failMsgs) > 0:
            errorMsg = ["CADimport of {} failed.".format(self.part.getTotalID())]
            for failMsg, calcType in self.failMsgs:
                errorMsg.append("Problem in {}. Message: {}".format(calcType, failMsg))
            self.errorSignal.emit(errorMsg)
            # self._clearData(self.part.path_physicalDirectory)
        else:
            if len(self.picFailMsg) > 0:
                self.picFailSignal.emit(
                    "No pictures of part {}. Message: {}".format(
                        self.part.getTotalID(), self.picFailMsg
                    )
                )
            self.partListSignal.emit(self.part)

        self.thread().quit()

    def resultCheck(self):
        partDirectory = self.part.path_physicalDirectory

        csvData_Box = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase
            + self.paths.namedata_minimalboundingbox_csv,
        )
        csvData_connected = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase
            + self.paths.namedata_surfaces_connected_csv,
        )
        csvData_NX = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase + self.paths.namedata_surfaces_nx_csv,
        )
        csvData_distribution_perNumber = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase
            + self.paths.namedata_surfaces_distribution_pernumber_csv,
        )
        csvData_distribution_perArea = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase
            + self.paths.namedata_surfaces_distribution_perarea_csv,
        )
        csvData_PointCloud = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase + self.paths.namedata_pointcloud_csv,
        )
        csvData_PCdistribution = self.paths.getCSVpath(
            partDirectory,
            self.part.partName_physicalDatabase
            + self.paths.namedata_pointcloud_distribution_csv,
        )

        files2have = [
            csvData_Box,
            csvData_connected,
            csvData_NX,
            csvData_distribution_perNumber,
            csvData_distribution_perArea,
            csvData_PointCloud,
            csvData_PCdistribution,
        ]

        for file_i in files2have:
            if not os.path.isfile(file_i):
                self.failMsgs.append(
                    (
                        "File {} is missing".format(file_i.rpartition(os.path.sep)[2]),
                        "NX-Output",
                    )
                )

    def _clearData(self, path: str):
        shutil.rmtree(path)


class dummy(QtCore.QObject):
    emitObject = Signal(object)

    def __init__(self, object_in):
        super().__init__()
        self.object = object_in

    @Slot(object)
    def run(self):
        time.sleep(0.5)
        self.emitObject.emit(self.object)
        self.thread().quit()
