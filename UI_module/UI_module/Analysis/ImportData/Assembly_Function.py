# -*- coding: utf-8 -*-
import os

from PySide2 import QtCore, QtGui
from PySide2.QtCore import Signal, Slot

# import ptvsd
from Analysis.Utility import QtWaitClass
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class assembly_tool_class(QtCore.QObject):

    # class assembly_tool_class(QtCore.QRunnable):

    sig_finished = Signal(int)
    processStatus = Signal(object)

    def __init__(
        self,
        pathsInput: PathsClass,
        partInput: PartInfoClass,
        calcPrefs: calcPrefClass,
        parent=None,
    ):
        super().__init__()

        self.paths = pathsInput
        self.part = partInput
        self.calcPrefs = calcPrefs
        self.timeOutStatus = False

        self.waitClass = QtWaitClass(self.calcPrefs.msec_wait_qprocess)
        self.processStatus.connect(self.waitClass.statusSlot)
        self.waitClass.timeOutSignal.connect(self.timeOut)

    def _start(self):
        # __endings = os.path.sep

        part_ID_str = self.part.assemblyId
        part_name = self.part.partName
        part_path = self.part.partPath
        part_format = self.part.partFormat

        ######## Path Tool - Assembly ########
        path_exe_assembly = self.paths.path_assemblydecomposition

        ######## Path NX - run_managed ########
        path_NX = self.paths.path_nxrunmanaged

        ######## Path Output ########
        part_OutputPath = self.part.path_physicalDirectory

        ######## Creation of the minimal bounding box ########
        # ptvsd.debug_this_thread()
        self.process = QtCore.QProcess(self)
        self.process.finished.connect(self.assembly_signal)
        self.process.started.connect(self.waitFunction)
        self.process.start(
            path_NX,
            [
                path_exe_assembly,
                u"--part_path={}".format(part_path),
                u"--part_name={}".format(part_name),
                u"--part_format={}".format("." + part_format),
                u"--part_ID={}".format(part_ID_str),
                u"--output_path_part={}".format(part_OutputPath),
            ],
        )

    @Slot(int)
    def assembly_signal(self, exitCode, exitStatus):
        # ptvsd.debug_this_thread()
        if not self.timeOutStatus:
            self.processStatus.emit(False)
            self.process.close()
            self.sig_finished.emit(exitCode)

    def waitFunction(self):
        self.waitClass.thread.start()

    @Slot(int)
    def timeOut(self):
        if not self.timeOutStatus:
            self.timeOutStatus = True
            self.sig_finished.emit(2)
            self.process.close()
