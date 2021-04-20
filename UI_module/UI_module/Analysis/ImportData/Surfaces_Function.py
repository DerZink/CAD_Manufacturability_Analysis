# -*- coding: utf-8 -*-
import os
from PySide2 import QtCore, QtGui
from PySide2.QtCore import Slot, Signal

# import ptvsd

from Analysis.Utility import QtWaitClass
import Shared.Preferences as Preferences
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class surfaces_tool_class(QtCore.QObject):

    sig_finished = Signal(object)
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
        part_name = self.part.partName_physicalDatabase
        part_path = self.part.path_physicalDirectory
        part_format = self.part.partFormat
        data_Name = self.paths.namedata_surfaces

        ######## Path tool - Boundingbox ########
        path_exe_surfaces = self.paths.path_surfaces

        ######## Path NX - run_managed ########
        path_NX = self.paths.path_nxrunmanaged

        ######## Mode ########
        self.draftMode = self.calcPrefs.draft_mode

        ######## Creation of the minimal bounding box ########
        self.QProcess = QtCore.QProcess()
        self.QProcess.finished.connect(self.surface_signal)
        self.QProcess.started.connect(self.waitFunction)
        self.QProcess.start(
            path_NX,
            [
                path_exe_surfaces,
                u"--part_path={}".format(part_path),
                u"--part_name={}".format(part_name),
                u"--part_format={}".format("." + part_format),
                u"--data_name={}".format(data_Name),
                u"--draft_mode={}".format(self.draftMode),
            ],
        )

    def surface_signal(self, exitCode, exitStatus):
        if not self.timeOutStatus:
            self.processStatus.emit(False)
            self.QProcess.close()
            self.sig_finished.emit((exitCode, exitStatus))

    def waitFunction(self):
        self.waitClass.thread.start()

    @Slot(int)
    def timeOut(self):
        if not self.timeOutStatus:
            self.timeOutStatus = True
            self.sig_finished.emit((1, "Timeout"))
            self.QProcess.close()
