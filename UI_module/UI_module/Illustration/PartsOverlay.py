import os
import copy
from shutil import copyfile, rmtree
from typing import Tuple, List

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

from Analysis.Utility import QtWaitClass
from Analysis.Pytable.Pytables_Detail_Analysis import (
    Detail_Input_Class,
    Detail_Transformation_Class,
)
from Analysis.Evaluation.DetailSimilarity import CalcDetailSimilarity
from Illustration.Utility import PDFBuilder, PDFViewerClass

from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass

from Analysis.Evaluation.DetailSimilarityClasses.RoughTransformation import (
    RoughTransformationCalc,
)
from Analysis.Evaluation.DetailSimilarityClasses.TransformationClasses import (
    TransformationFunctions,
    TransformationClass,
    BoxTransformationCloudData,
    TransformationClassCluster,
    BoundingBox,
    PointCloudFunctions,
)
from Analysis.Evaluation.DetailSimilarityClasses.PartPairClass import GS_PartPairclass

# import ptvsd


class overlay_parts_batch(QtCore.QObject):

    sig_finished = Signal(object)
    processStatus = Signal(object)

    def __init__(
        self,
        pathsInput: PathsClass,
        pathOutput: str,
        calcPrefs: calcPrefClass,
        part_a_ID: str,
        part_b_ID: str,
        partEnding: str,
        transformationData: Tuple[
            Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], bool
        ],
        parent=None,
    ):
        super().__init__()

        self.paths = pathsInput
        self.calcPrefs = calcPrefs

        ######## Path output ########
        self.pathOutput = pathOutput

        self.part_a_ID = part_a_ID
        self.part_b_ID = part_b_ID

        self.partEnding = partEnding

        self.a_translate = transformationData[0][0]
        self.b_translate = transformationData[0][1]
        self.a_rotate = transformationData[1][0]
        self.b_rotate = transformationData[1][1]

        self.timeOutStatus = False

        self.waitClass = QtWaitClass(self.calcPrefs.msec_wait_qprocess)
        self.processStatus.connect(self.waitClass.statusSlot)
        self.waitClass.timeOutSignal.connect(self.timeOut)

    def _start(self):
        # ptvsd.debug_this_thread()

        ######## Path tool - images ########
        path_exe_overlay = self.paths.path_overlaygeneration

        ######## Path NX - run_managed ########
        path_NX = self.paths.path_nxrunmanaged

        ######## perform the image creation ########
        self.process = QtCore.QProcess()
        self.process.finished.connect(self.overlay_signal)
        self.process.started.connect(self.waitFunction)

        self.process.start(
            path_NX,
            [
                path_exe_overlay,
                u"--path_output={}".format(self.pathOutput),
                u"--part_id_a={}".format(self.part_a_ID),
                u"--part_id_b={}".format(self.part_b_ID),
                u"--part_ending={}".format(self.partEnding),
                u"--translation_a={}".format(self.__translateStr(self.a_translate)),
                u"--translation_b={}".format(self.__translateStr(self.b_translate)),
                u"--rotation_a={}".format(self.__rotateStr(self.a_rotate)),
                u"--rotation_b={}".format(self.__rotateStr(self.b_rotate)),
            ],
        )

    def __translateStr(self, vec: np.ndarray):
        return ", ".join(str(v) for v in list(vec))

    def __rotateStr(self, mat: np.ndarray):
        return ", ".join(
            str(v) for v in list(mat[0, :]) + list(mat[1, :]) + list(mat[2, :])
        )

    @Slot(object)
    def overlay_signal(self, exitCode, exitStatus):
        if not self.timeOutStatus:
            self.processStatus.emit(False)
            self.process.close()
            self.sig_finished.emit((exitCode, exitStatus))

    def waitFunction(self):
        self.waitClass.thread.start()

    @Slot(int)
    def timeOut(self):
        if not self.timeOutStatus:
            self.timeOutStatus = True
            self.sig_finished.emit((1, "Timeout"))
            self.process.close()


class partsOverlay_Class(QtCore.QObject):
    finishedSignal = Signal()

    def __init__(
        self,
        pathsInput: PathsClass,
        calcPrefs: calcPrefClass,
        detailColumns: detailColumnsClass,
        transformation: bool = True,
    ):
        super().__init__()
        self.thread = QtCore.QThread()
        self.thread.started.connect(self.checkStatus)
        self.paths = pathsInput
        self.calcPrefs = calcPrefs
        self.detailColumns = detailColumns

        self.transformationStatus = transformation
        self.partEnding = self.paths.namedata_overlay

        self.pathPartTransformations = self.paths.path_parttransformations
        os.makedirs(self.pathPartTransformations, exist_ok=True)

    def setParts(self, part_a: PartInfoClass, part_b: PartInfoClass):
        self.part_a = part_a
        self.part_b = part_b
        self.partPath = os.path.join(
            self.pathPartTransformations,
            self.part_a.getTotalID() + "_vs_" + self.part_b.getTotalID(),
        )

    def start(self):
        self.thread.start()

    def checkStatus(self):
        # ptvsd.debug_this_thread()
        self.similarityH5 = Detail_Transformation_Class(
            self.paths, "similarity_h5"
        )  # type: Detail_Transformation_Class

        self.transformationData = self.__getTransformationData()
        if len(self.transformationData) > 0:
            statusFile = self.transformationData[2]
            if statusFile == True:
                self.openPDF()
            else:
                self.create()

        else:
            self.similarityH5.closeTable()
            self.finishedSignal.emit()
            self.thread.quit()

    def create(self):
        self.copyParts()

        self.overlayThread = QtCore.QThread()
        self.overlayBatch = overlay_parts_batch(
            self.paths,
            self.pathPartTransformations,
            self.calcPrefs,
            self.part_a.getTotalID(),
            self.part_b.getTotalID(),
            self.partEnding,
            self.transformationData,
        )
        self.overlayBatch.moveToThread(self.overlayThread)
        self.overlayBatch.sig_finished.connect(self.__overlayFinished)
        self.overlayThread.started.connect(self.overlayBatch._start)
        self.overlayThread.start()

    def copyParts(self):

        for part in [self.part_a, self.part_b]:
            file_part = os.path.join(
                part.path_physicalDirectory, part.partId + self.partEnding
            )
            output_part = os.path.join(
                self.pathPartTransformations, part.getTotalID() + self.partEnding
            )
            copyfile(file_part, output_part)

    def __getTransformationData(
        self,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], bool]:

        if self.transformationStatus == True:
            outputDict = self.similarityH5.outputTransformations(
                [(self.part_a, self.part_b)]
            )
            if len(outputDict) == 0:
                self.GSCalcClass = CalcDetailSimilarity(
                    [self.part_a],
                    self.paths,
                    self.detailColumns,
                    self.calcPrefs,
                    calibration=True,
                )
                self.GS_PartPair = self.GSCalcClass.start_forOverlay(self.part_b)

                return (
                    (self.GS_PartPair.pose_a.t, self.GS_PartPair.pose_b.t),
                    (self.GS_PartPair.pose_a.R, self.GS_PartPair.pose_b.R),
                    False,
                )

            return outputDict[(self.part_a.getTotalID(), self.part_b.getTotalID())]
        else:
            return (
                (
                    np.zeros(
                        3,
                    ),
                    np.zeros(
                        3,
                    ),
                ),
                (np.eye(3), np.eye(3)),
                False,
            )

    def __overlayFinished(self, exitMsg: Tuple[float, str]):
        self.overlayThread.quit()
        if exitMsg[0] == 0:
            self.build3DPDF()
        else:
            print("Overlay batch failed")
            print(exitMsg[1])
            self.closeThread()

    def build3DPDF(self):

        self.pdfThread = QtCore.QThread()

        self.pdfClass = PDFBuilder(
            self.paths,
            self.calcPrefs,
            self.pathPartTransformations,
            [self.partPath + ".prt"],
        )

        self.pdfClass.moveToThread(self.pdfThread)
        self.pdfClass.sig_finished.connect(self.openPDF)
        self.pdfThread.started.connect(self.pdfClass._start)
        self.pdfThread.start()

    def openPDF(self, exitMsg: Tuple[float, str] = (0, "Good")):
        # ptvsd.debug_this_thread()
        if exitMsg[1] != "Good":
            self.pdfThread.quit()
        if exitMsg[0] == 0 and exitMsg[1] == QtCore.QProcess.ExitStatus.NormalExit:
            # set file status in H5
            self.similarityH5.setFileStatus([(self.part_a, self.part_b)], [True])

            # view PDF
            self.viewPDF = PDFViewerClass()  # type: PDFViewerClass
            self.viewPDF.setPath(self.partPath + ".pdf")
            self.viewPDF.start()
        else:
            print("Overlay PDF generation failed")
            print(exitMsg[1])

        self.closeThread()

    @Slot()
    def closeThread(self):
        self.similarityH5.closeTable()
        self.finishedSignal.emit()
        self.thread.quit()


class debugOverlay_Class(CalcDetailSimilarity, partsOverlay_Class, QtCore.QObject):
    def __init__(
        self,
        pathsInput: PathsClass,
        calcPrefs: calcPrefClass,
        detailColumns: detailColumnsClass,
    ):

        self.paths = pathsInput
        self.calcPrefs = calcPrefs

        self.detailColumns = detailColumns

        QtCore.QObject.__init__(self)
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.debug)

    def setParts(self, part_a: PartInfoClass, part_b: PartInfoClass):

        self.pathPartTransformations = os.path.join(
            self.paths.path_parttransformations,
            "D_{}_vs_{}".format(part_a.getTotalID(), part_b.getTotalID()),
        )
        if os.path.isdir(self.pathPartTransformations):
            rmtree(self.pathPartTransformations)
        os.makedirs(self.pathPartTransformations, exist_ok=True)

        self.partEnding = self.paths.namedata_overlay

        partsOverlay_Class.setParts(self, part_a, part_b)

    def start(self):
        self.thread.start()

    def debug(self):
        # ptvsd.debug_this_thread()
        self.definitions(self.detailColumns)
        self.partInputList = [self.part_a]

        self.GS_PartPair = self.GSCalcClass.start_forOverlay(
            self.part_b
        )  # type: GS_PartPairclass

        poseClustersBoxChecked = self.GS_PartPair.check_poses(
            self.GS_PartPair.poses_b[0:8]
        )
        poseClustersRoughChecked = self.GS_PartPair.check_poses(
            self.GS_PartPair.poses_b[8:]
        )
        fineTransformationsChecked = self.GS_PartPair.fineTransformationsChecked(
            poseClustersBoxChecked[:3] + poseClustersRoughChecked[:7]
        )
        self.GS_PartPair.setPosesBodyB(
            poseClustersBoxChecked[:3]
            + poseClustersRoughChecked[:7]
            + fineTransformationsChecked
        )
        self.debugTransformations()
        # poseClustersSave.extend(finePoseClusters_sorted)
        # self.debugTransformations(boxTransformations_a.boxPoses[0], poseClustersSave)

    def debugTransformations(
        self,
    ):

        self.copyParts()

        # rename parts
        self.renameParts()

        self.assemblyList = []
        # output poses
        self.outputPoses()

        self.pose_b_pos = 0
        self.assemblyRunner()

    def outputPoses(self):
        filePath = os.path.join(self.pathPartTransformations, "Transformations.txt")
        with open(filePath, "w") as outFile:
            At = self.GS_PartPair.pose_a.t
            ARx = self.GS_PartPair.pose_a.R[:, 0]
            ARy = self.GS_PartPair.pose_a.R[:, 1]
            ARz = self.GS_PartPair.pose_a.R[:, 2]
            strA = "Part A: tx={0}, ty={1}, tz={2}, Rx1={3}, Rx2={4}, Rx3={5}, Ry1={6}, Ry2={7}, Ry3={8}, Rz1={9}, Rz2={10}, Rz3={11}\n".format(
                At[0],
                At[1],
                At[2],
                ARx[0],
                ARx[1],
                ARx[2],
                ARy[0],
                ARy[1],
                ARy[2],
                ARz[0],
                ARz[1],
                ARz[2],
            )
            outFile.write(strA)
            for i, poseB in enumerate(self.GS_PartPair.poses_b):
                Bt = poseB.poseClass.t
                BRx = poseB.poseClass.R[:, 0]
                BRy = poseB.poseClass.R[:, 1]
                BRz = poseB.poseClass.R[:, 2]
                strB = "Part B {12}: tx={0}, ty={1}, tz={2}, Rx1={3}, Rx2={4}, Rx3={5}, Ry1={6}, Ry2={7}, Ry3={8}, Rz1={9}, Rz2={10}, Rz3={11}\n".format(
                    Bt[0],
                    Bt[1],
                    Bt[2],
                    BRx[0],
                    BRx[1],
                    BRx[2],
                    BRy[0],
                    BRy[1],
                    BRy[2],
                    BRz[0],
                    BRz[1],
                    BRz[2],
                    i,
                )
                outFile.write(strB)

    def renameParts(self):
        names = ["A", "B"]

        for i_p, part in enumerate([self.part_a, self.part_b]):
            saved_part = os.path.join(
                self.pathPartTransformations, part.getTotalID() + self.partEnding
            )
            renamed_part = os.path.join(
                self.pathPartTransformations, names[i_p] + ".prt"
            )

            os.rename(saved_part, renamed_part)

        self.partEnding = ".prt"

    def assemblyRunner(self):
        # ptvsd.debug_this_thread()
        b_pose = self.GS_PartPair.poses_b[self.pose_b_pos]

        transformationData = (
            (self.GS_PartPair.pose_a.t, b_pose.poseClass.t),
            (self.GS_PartPair.pose_a.R, b_pose.poseClass.R),
        )

        self.assemblyEnding = "_{}_{}".format(
            self.pose_b_pos, round(b_pose.poseClass.geometric_similarity, 3)
        )
        self.overlayThread = QtCore.QThread()
        self.overlayBatch = overlay_parts_batch(
            self.paths,
            self.pathPartTransformations,
            self.calcPrefs,
            "A",
            "B",
            self.partEnding,
            transformationData,
        )
        self.overlayBatch.moveToThread(self.overlayThread)
        self.overlayBatch.sig_finished.connect(self.renameAssembly)
        self.overlayThread.started.connect(self.overlayBatch._start)
        self.overlayThread.start()

    def renameAssembly(self, exitMsg: Tuple[float, str]):
        # ptvsd.debug_this_thread()
        savedName = os.path.join(self.pathPartTransformations, "A_vs_B" + ".prt")
        newName = os.path.join(
            self.pathPartTransformations, "A_vs_B" + self.assemblyEnding + ".prt"
        )
        os.rename(savedName, newName)

        self.assemblyList.append(newName)
        # self.overlayThread.quit()
        self.overlayThread.requestInterruption()
        self.overlayThread.terminate()
        self.overlayThread.wait()
        if self.pose_b_pos == len(self.GS_PartPair.poses_b) - 1:
            self.build3DPDF(self.assemblyList)
        else:
            self.pose_b_pos += 1
            self.assemblyRunner()

    def build3DPDF(self, partName):
        # ptvsd.debug_this_thread()
        self.pdfThread = QtCore.QThread()

        self.pdfClass = PDFBuilder(
            self.paths, self.calcPrefs, self.pathPartTransformations, partName
        )

        self.pdfClass.moveToThread(self.pdfThread)
        self.pdfClass.sig_finished.connect(self.closeThread)
        self.pdfThread.started.connect(self.pdfClass._start)
        self.pdfThread.start()

    def closeThread(self):
        self.pdfThread.quit()
        partsOverlay_Class.closeThread(self)
