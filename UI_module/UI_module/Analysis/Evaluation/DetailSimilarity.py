"""
Calculating Detail Similarity of Point Clouds
"""
import os
import copy
from typing import Dict, List, Tuple

import numpy as np
import tables.tableextension as tableextension
from PySide2 import QtCore
from PySide2.QtCore import Signal
from tables import *

# import ptvsd

from Analysis.Pytable.Pytables_Detail_Analysis import (
    Detail_Input_Class,
    Detail_Transformation_Class,
)
from Analysis.Pytable.Pytables_Management_Functions import (
    Pytables_Read_Class,
    Pytables_Update_Class,
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

from Analysis.Evaluation.DetailSimilarityClasses.RoughTransformation import (
    RoughTransformationCalc,
)

from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass


class CalcDetailSimilarity(QtCore.QObject):
    """Class for calculation of detail similarity of point clouds
        Input:
                - Global paths as PathsClass
                - Detail features
                - calculation preferences"""

    updateDatabase = Signal(bool)

    def __init__(
        self,
        partInputList: List[PartInfoClass],
        pathsInput: PathsClass,
        detailColumns: detailColumnsClass,
        calcPrefs: calcPrefClass,
        calibration: bool = False,
    ):
        super().__init__()
        # ptvsd.debug_this_thread()
        self.partInputList = partInputList
        self.paths = pathsInput
        self.calcPrefs = calcPrefs

        self.definitions(detailColumns)

        if calibration == False:
            self.thread = QtCore.QThread()
            self.moveToThread(self.thread)
            self.thread.started.connect(self.start)

    def definitions(self, detailColumns: detailColumnsClass):
        ### Definition of points for pointCloud ###
        # *_face = on part, *_box = coord of reffering point in bounding box system
        # norm is always calculated on the part face

        self.grid_location = detailColumns.grid_location

        self.pointCloudColumns = [
            detailColumns.x_box,  # detailColumns.x_box,
            detailColumns.y_box,  # detailColumns.y_box,
            detailColumns.z_box,  # detailColumns.z_box,
            detailColumns.norm_x,
            detailColumns.norm_y,
            detailColumns.norm_z,
            detailColumns.x_face,  # detailColumns.x_face
            detailColumns.y_face,  # detailColumns.y_face
            detailColumns.z_face,  # detailColumns.z_face
        ]

        self.pointCloudCurvatureColumns = [detailColumns.curv_1, detailColumns.curv_2]

        self.boxDeltaColumns = [
            detailColumns.box_delta_1,
            detailColumns.box_delta_2,
            detailColumns.box_delta_3,
        ]

        self.boxCoordColumns = [
            detailColumns.box_coord_1x,
            detailColumns.box_coord_1y,
            detailColumns.box_coord_1z,
            detailColumns.box_coord_2x,
            detailColumns.box_coord_2y,
            detailColumns.box_coord_2z,
        ]

        self.boxDirColumns = [
            detailColumns.box_dir_1x,
            detailColumns.box_dir_1y,
            detailColumns.box_dir_1z,
            detailColumns.box_dir_2x,
            detailColumns.box_dir_2y,
            detailColumns.box_dir_2z,
            detailColumns.box_dir_3x,
            detailColumns.box_dir_3y,
            detailColumns.box_dir_3z,
        ]

        self.similarityH5 = Detail_Transformation_Class(self.paths, "similarity_h5")

        self.detailCloudDataH5 = Detail_Input_Class(
            self.paths, "pointclouddata_h5", self.calcPrefs
        )

        self.detailBoxDataH5 = Detail_Input_Class(
            self.paths, "boxdata_h5", self.calcPrefs
        )

        self.RoughTransformationCalc = RoughTransformationCalc(self.calcPrefs)

    def start(self):
        """ Start calculation:
            First point clouds of parts must be orientated best to each other
            Second differences between parts can be measured"""
        # ptvsd.debug_this_thread()
        for part_a in self.partInputList:
            print("DetailCalc a = {}".format(part_a.getTotalID()))
            # get similar parts from feature analysis
            parts_b = self.__getFeatureSimilarParts(part_a)
            if len(parts_b) > 0:
                (
                    part_b_output,
                    parts_b_Old,
                    GS_PartPairclass_list,
                ) = self.geometricSimilarityWorker(part_a, parts_b)

                # save results in h5
                self.updateH5Table(
                    part_a, part_b_output, parts_b_Old, GS_PartPairclass_list
                )

        self.closeAll()
        self.thread.quit()
        self.updateDatabase.emit(True)

    def start_forOverlay(self, partB: PartInfoClass):

        part_a = self.partInputList[0]
        (
            part_b_output,
            parts_b_Old,
            GS_PartPairclass_list,
        ) = self.geometricSimilarityWorker(part_a, [partB])

        # save results in h5
        self.updateH5Table(part_a, part_b_output, parts_b_Old, GS_PartPairclass_list)
        self.closeAll()

        return GS_PartPairclass_list[0]

    def start_forCalibration(
        self, parts_b: List[PartInfoClass], distanceRating: bool = False,
    ):
        GS_PartPairclass_list = []
        for partPos, part_a in enumerate(self.partInputList):
            part_b = parts_b[partPos]
            print(partPos, ": ", part_a.getTotalID(), " vs ", part_b.getTotalID())

            # read data from H5 file
            (
                (part_a_CloudPoints, part_a_Curvature, part_a_GridLocations),
                part_a_BoundingBox,
            ) = self.getH5Data(part_a)
            (
                (part_b_CloudPoints, part_b_Curvature, part_b_GridLocations),
                part_b_BoundingBox,
            ) = self.getH5Data(part_b)

            PartPair = GS_PartPairclass(
                self.calcPrefs,
                part_a.getTotalID(),
                part_b.getTotalID(),
                part_a_CloudPoints,
                part_b_CloudPoints,
                part_a_Curvature,
                part_b_Curvature,
                part_a_GridLocations,
                part_b_GridLocations,
                distanceRating=distanceRating,
            )
            PartPair.evaluatePointPairs()

            GS_PartPairclass_list.append(PartPair)

        self.closeAll()
        return GS_PartPairclass_list

    def closeAll(self):
        self.detailCloudDataH5.closeTable()
        self.detailBoxDataH5.closeTable()
        self.similarityH5.closeTable()

    def geometricSimilarityWorker(
        self, part_a: PartInfoClass, parts_b: List[PartInfoClass]
    ):
        # ptvsd.debug_this_thread()
        # check if this pair was calculated before
        parts_b, parts_b_Old, pairResults = self.__checkIfPairResultsExist(
            part_a, parts_b
        )

        GS_PartPairclass_list = []
        part_b_output = []

        # read data from H5 file
        (part_a_CloudData, part_a_BoundingBox) = self.getH5Data(part_a)

        if len(parts_b) > 0:

            # transform data from minimum bounding box coordinates
            boxTransformations_a = BoxTransformationCloudData(
                part_a_BoundingBox, self.calcPrefs
            )

            # save transformation of part a
            pose_a = TransformationClass(
                1, self.calcPrefs.digits_round_pos, self.calcPrefs.digits_round_dir
            )
            pose_a.setRT(
                boxTransformations_a.boxPoses[0].R, boxTransformations_a.boxPoses[0].t
            )

            # use bounding box coordinate system for transformation to global coordinate system
            part_a_CloudPoints = part_a_CloudData[0]
            part_a_CloudPoints = boxTransformations_a.calcTransformationPose(
                part_a_CloudPoints, boxTransformations_a.boxPoses[0]
            )
            part_a_CloudData = (
                part_a_CloudPoints,
                part_a_CloudData[1],
                part_a_CloudData[2],
            )

            # train data of part_a
            self.trainPartData(
                part_a,
                part_a_CloudPoints[:, :6],
                boxTransformations_a.boxPoses[0].getBoundingBox(),
            )

            for part_b in parts_b:
                print("DetailCalc b = {}".format(part_b.getTotalID()))

                # read data from H5 file
                (part_b_CloudData, part_b_BoundingBox) = self.getH5Data(part_b)

                # match data
                partPairclass = self.__matchPartData(
                    part_a,
                    part_a_CloudData,
                    part_b,
                    part_b_CloudData,
                    part_b_BoundingBox,
                )

                partPairclass.pose_a = pose_a

                GS_PartPairclass_list.append(partPairclass)

            part_b_output = parts_b

        if len(pairResults) > 0:
            # build dict of parts b
            b_dict = {}
            for part_b_old in parts_b_Old:
                b_dict[part_b_old.getTotalID()] = part_b_old

            for pairResult in pairResults.keys():

                # calculate similarity value
                part_b = b_dict[pairResult[1]]
                part_b_output.append(part_b)

                print("Detail-re-Calc b = {}".format(part_b.getTotalID()))

                # read data from H5 file
                (part_b_CloudData, part_b_BoundingBox) = self.getH5Data(part_b)
                (a_t, b_t), (a_r, b_r), fileStatus = pairResults[pairResult]

                partPairclass = self.similarityParts(
                    part_a,
                    part_a_CloudData,
                    part_b,
                    part_b_CloudData,
                    (b_t, b_r),
                    (a_t, a_r),
                )

                GS_PartPairclass_list.append(partPairclass)

        return (
            part_b_output,
            parts_b_Old,
            GS_PartPairclass_list,
        )

    def getH5Data(
        self, part: PartInfoClass, box: bool = True
    ) -> Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], BoundingBox]:

        part_BoundingBox = None
        if box == True:
            boxDeltas, boxCoords, boxDirs = self.detailBoxDataH5.getBoxData(
                part, self.boxDeltaColumns, self.boxCoordColumns, self.boxDirColumns
            )
            part_BoundingBox = BoundingBox()
            part_BoundingBox.setData((boxDeltas, boxCoords, boxDirs))

        (
            cloudPoints,
            curvature,
            gridLocations,
        ) = self.detailCloudDataH5.getPointCloudData(
            part,
            self.pointCloudColumns,
            self.pointCloudCurvatureColumns,
            self.grid_location,
        )

        return (cloudPoints, curvature, gridLocations), part_BoundingBox

    def trainPartData(
        self,
        part_a: PartInfoClass,
        part_a_CloudPoints: np.ndarray,
        part_a_BoundingBox: BoundingBox,
        noSave=False,
    ):

        self.RoughTransformationCalc.trainModel(
            part_a, part_a_CloudPoints, part_a_BoundingBox, noSave
        )

    def __getFeatureSimilarParts(self, part_a: PartInfoClass) -> List[PartInfoClass]:

        featureSimilarityTable = (
            self.paths.similarity_results_group
            + self.similarityH5.root
            + part_a.getTotalID()
        )

        ## get parts which have a feature similarity value above threshold
        thresholdValue = self.similarityH5.Read_single_row_table(
            self.paths.similarity_results_info, part_a.getTotalID()
        )[self.paths.detail_threshold]

        condition_highFeatureSimilarity = "({0} >= {1}) & ({0} < 0.9999)".format(
            self.paths.feature_similarity, thresholdValue
        )

        partList = []
        for part_b in self.similarityH5.Read_table_where(
            featureSimilarityTable, condition_highFeatureSimilarity
        ):
            totalID = part_b[self.paths.part_id].decode("utf-8")
            detailValue = part_b[self.paths.detail_similarity]
            if (
                totalID != part_a.getTotalID()
                and detailValue == self.calcPrefs.default_detailsimilarity
            ):
                partName = self.similarityH5.Read_single_row_table(
                    self.paths.features_table, totalID
                )[self.paths.part_name].decode("utf-8")

                name_i = partName + ".db"
                tmpPart = PartInfoClass(
                    partName=name_i, partIDstr=totalID, pathClass=self.paths
                )
                partList.append(tmpPart)

        return partList

    def __checkIfPairResultsExist(
        self, part_a: PartInfoClass, parts_b: List[PartInfoClass]
    ) -> Tuple[
        List[PartInfoClass],
        List[PartInfoClass],
        Dict[
            Tuple[str, str],
            Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], bool],
        ],
    ]:

        partPairs = []
        for part_b in parts_b:
            partPairs.append((part_a, part_b))
        pairResults = self.similarityH5.outputTransformations(partPairs)
        if len(pairResults) > 0:
            parts_b_New = []  # type: List[PartInfoClass]
            parts_b_Old = []  # type: List[PartInfoClass]
            bParts_inResults = set([key[1] for key in pairResults.keys()])
            for part_b in parts_b:
                part_b_ID = part_b.getTotalID()
                if not part_b_ID in bParts_inResults:
                    parts_b_New.append(part_b)
                else:
                    parts_b_Old.append(part_b)
            return parts_b_New, parts_b_Old, pairResults
        else:
            return parts_b, [], {}

    def __matchPartData(
        self,
        part_a: PartInfoClass,
        part_a_CloudData: Tuple[np.ndarray, np.ndarray, np.ndarray],
        part_b: PartInfoClass,
        part_b_CloudData: Tuple[np.ndarray, np.ndarray, np.ndarray],
        part_b_BoundingBox: BoundingBox,
    ) -> GS_PartPairclass:

        part_a_CloudPoints, part_a_Curvature, part_a_GridLocations = part_a_CloudData
        part_b_CloudPoints, part_b_Curvature, part_b_GridLocations = part_b_CloudData

        PartPair = GS_PartPairclass(
            self.calcPrefs,
            part_a.getTotalID(),
            part_b.getTotalID(),
            part_a_CloudPoints,
            part_b_CloudPoints,
            part_a_Curvature,
            part_b_Curvature,
            part_a_GridLocations,
            part_b_GridLocations,
            distanceRating=True,
        )

        PartPair.learnBodyAPointCloud()
        # list of TransformationClassClusters
        poseClusters = []  # type: List[TransformationClassCluster]

        # transform data from minimum bounding box coordinates
        part_b_boxTransformations = BoxTransformationCloudData(
            part_b_BoundingBox, self.calcPrefs
        )

        # first try to match by transforming with box coordinate systems
        posesClustersBox_sorted = PartPair.check_poses(
            part_b_boxTransformations.poseClusters
        )

        poseClusters.extend(posesClustersBox_sorted[0:3])

        if poseClusters[0].poseClass.geometric_similarity < 0.95:
            # positioning by point cloud triple positioning follows
            roughPoseClusters = self.RoughTransformationCalc.roughMatch(
                part_b,
                part_b_CloudPoints[:, :6],
                part_b_BoundingBox,
                posesClustersBox_sorted,
            )  # type: List[TransformationClass]

            roughPoseClusters_sorted = PartPair.check_poses(roughPoseClusters)

            poseClusters.extend(roughPoseClusters_sorted[0:7])

        PartPair.setPosesBodyB(poseClusters)
        PartPair.findBest_pose_b()

        PartPair.evaluatePointPairs()

        return PartPair

    def similarityParts(
        self,
        part_a: PartInfoClass,
        part_a_CloudData: Tuple[np.ndarray, np.ndarray],
        part_b: PartInfoClass,
        part_b_CloudData: Tuple[np.ndarray, np.ndarray],
        part_b_transformation: Tuple[np.ndarray, np.ndarray],
        part_a_transformation: Tuple[np.ndarray, np.ndarray] = None,
    ) -> float:
        """If part_a_transformation is given, transformation of the part_a point cloud is done. Otherwise part_a_CloudData is regarded as transformed data."""

        part_a_CloudPoints, part_a_Curvature, part_a_GridLocations = part_a_CloudData
        part_b_CloudPoints, part_b_Curvature, part_b_GridLocations = part_b_CloudData
        PartPair = GS_PartPairclass(
            self.calcPrefs,
            part_a.getTotalID(),
            part_b.getTotalID(),
            part_a_CloudPoints,
            part_b_CloudPoints,
            part_a_Curvature,
            part_b_Curvature,
            part_a_GridLocations,
            part_b_GridLocations,
        )

        if not part_a_transformation is None:
            # Transform cloud data of part a
            pose_a = TransformationClass(
                1, self.calcPrefs.digits_round_pos, self.calcPrefs.digits_round_dir
            )
            pose_a.setRT(part_a_transformation[1], part_a_transformation[0])
            PartPair.transformation_bodyX(pose_a, body="a")

        # Define pose for part b
        pose_b = TransformationClass(
            1, self.calcPrefs.digits_round_pos, self.calcPrefs.digits_round_dir
        )
        pose_b.setRT(part_b_transformation[1], part_b_transformation[0])
        PartPair.transformation_bodyX(pose_b, body="b")

        PartPair.evaluatePointPairs()

        return PartPair

    def updateH5Table(
        self,
        part_a: PartInfoClass,
        parts_b: List[PartInfoClass],
        parts_b_old: List[PartInfoClass],
        GS_PartPairclass_list: List[GS_PartPairclass],
    ):
        if len(parts_b) > 0:
            # update similarity values of part a
            similarityResults = [partPair.getGS() for partPair in GS_PartPairclass_list]
            self.__updateSimilarityTable(part_a, parts_b, similarityResults)

            # save transformations between parts
            self.similarityH5.saveTransformations(
                part_a, parts_b, parts_b_old, GS_PartPairclass_list
            )

            # update calculation status of part a
            self.__updateCalculationStatus(part_a)

            # delete existing diagram
            diagramPath = os.path.join(
                part_a.path_physicalDirectory, self.paths.namedata_feature_diagramm
            )

            if os.path.isfile(diagramPath):
                os.remove(diagramPath)

    def __updateSimilarityTable(
        self,
        part_a: PartInfoClass,
        parts_b: List[PartInfoClass],
        similarityResults: List[float],
    ):
        tablePath = (
            self.paths.similarity_results_group
            + self.similarityH5.root
            + part_a.getTotalID()
        )

        self.similarityH5.updateTable(
            tablePath, self.paths.detail_similarity, similarityResults, parts_b
        )

        self.__outputDetailTextFile(part_a, parts_b, similarityResults)

    def __updateCalculationStatus(self, part_a: PartInfoClass):
        partID = part_a.getTotalID()
        infoExpr = "{} == b'{}'".format(self.paths.part_id, partID)
        self.similarityH5.Write_table_where(
            self.paths.similarity_results_info,
            infoExpr,
            [self.paths.detail_similarity],
            ["Done"],
        )

    def __outputDetailTextFile(
        self,
        part_a: PartInfoClass,
        parts_b: List[PartInfoClass],
        similarityResults: List[float],
    ):
        outFilePath = os.path.join(os.getcwd(), "DetailSimResults.txt")
        with open(outFilePath, mode="a") as outFile:
            for i, partB in enumerate(parts_b):
                outFile.write(
                    "{0} vs. {1} : {2} \n".format(
                        part_a.getTotalID(), partB.getTotalID(), similarityResults[i]
                    )
                )
