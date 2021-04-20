import os
import subprocess
import xml.etree.ElementTree as etree
from typing import List

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

from Analysis.Utility import QtWaitClass
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass

# import ptvsd


class PDFViewerClass(QtCore.QObject):
    path = ""

    def __init__(self):
        super().__init__()
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__openPDF__)

    def setPath(self, path: str):

        self.path = path

    def start(self):
        self.thread.start()

    def __openPDF__(self):
        self.process = subprocess.Popen([self.path], shell=True)
        self.thread.quit()


class PDFBuilder(QtCore.QObject):
    sig_finished = Signal(object)
    processStatus = Signal(object)

    def __init__(
        self,
        paths: PathsClass,
        calcPrefs: calcPrefClass,
        calcFolder: str,
        partPathList: List[str],
    ):
        super().__init__()

        self.paths = paths
        self.calcPrefs = calcPrefs

        self.partList = partPathList
        self.calcFolder = calcFolder

        self.timeOutStatus = False

        self.waitClass = QtWaitClass(self.calcPrefs.msec_wait_qprocess)
        self.processStatus.connect(self.waitClass.statusSlot)
        self.waitClass.timeOutSignal.connect(self.timeOut)

        ######## Build Partsfile ########
        self.buildPartsFile()
        ######## Build XML ########
        self.buildXML()

    def _start(self):
        # ptvsd.debug_this_thread()
        ######## Path NX - run_managed ########
        path_TPD = os.path.join(self.paths.path_nx, r"TDP/batch/PublishTDPNative.exe")
        pathUGIIbat = os.path.join(self.paths.path_nx, r"UGII/ugiicmd.bat")
        pathUGII = self.paths.path_nx

        ######## perform the pdf creation ########
        self.process = QtCore.QProcess()
        # print("init process")

        self.process.finished.connect(self.pdfs_signal)
        self.process.started.connect(self.waitFunction)
        self.process.errorOccurred.connect(self.printError)
        self.process.start(
            'cmd /c " "{0}" "{1}" && call "" "{2}" -config_file="{3}""'.format(
                pathUGIIbat, pathUGII, path_TPD, self.xmlPath
            )
        )

    def buildPartsFile(self):
        os.makedirs(self.calcFolder, exist_ok=True)
        self.partsFilePath = os.path.join(self.calcFolder, "partIDs.txt")
        with open(self.partsFilePath, "w") as partsFile:
            for part in self.partList:
                partsFile.write(part + "\n")

    def buildXML(self):
        xmlRoot = etree.parse(
            os.path.join(self.paths.path_tools, "Template3DPart_database.xml")
        )
        dataset = xmlRoot.find(".//dataset")
        dataset.text = self.partsFilePath
        template_part = xmlRoot.find(".//template_part")
        template_part.text = os.path.join(
            self.paths.path_tools, "Template3DPart_database.prt"
        )
        output_directory = xmlRoot.find(".//output_directory")
        output_directory.text = self.calcFolder
        self.xmlPath = os.path.join(self.calcFolder, "3DPDF.xml")
        xmlRoot.write(self.xmlPath)

    @Slot(object)
    def printError(self, object_in=""):
        if object_in != "":
            print(self.calcFolder, object_in)
            self.sig_finished.emit((1, "Error"))

    @Slot(object)
    def pdfs_signal(self, exitCode, exitStatus):
        # print("process finished")
        if not self.timeOutStatus:
            # print(self.process.readAllStandardOutput())
            # print(self.process.readAllStandardError())
            self.processStatus.emit(False)
            self.process.close()
            self.sig_finished.emit((0, exitStatus))

    def waitFunction(self):
        self.waitClass.thread.start()

    @Slot(int)
    def timeOut(self):
        if not self.timeOutStatus:
            self.timeOutStatus = True
            self.sig_finished.emit((1, "Timeout"))
            self.process.close()
