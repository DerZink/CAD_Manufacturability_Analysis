from typing import List, Tuple, Dict

import numpy as np
from tables import *

from Analysis.Pytable.Pytables_Management_Functions import (
    Pytables_Read_Class,
    Pytables_Update_Class,
)
from Analysis.Evaluation.DetailSimilarityClasses.PartPairClass import GS_PartPairclass
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass

# import ptvsd


class Detail_Input_Class(Pytables_Read_Class):
    def __init__(self, paths: PathsClass, name: str, calcPrefs: calcPrefClass):

        self.calcPrefs = calcPrefs
        super().__init__(paths, name)

    def getPointCloudData(
        self,
        part: PartInfoClass,
        detailColumns: List[str],
        curvColumns: List[str],
        gridLocationColumn: str,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        partID = part.getTotalID()
        nrOfPoints = self.getNrOfEntriesNode(partID)

        # point cloud coordinates and normals
        np_posColumnData = np.empty((nrOfPoints, len(detailColumns)))
        for i, column in enumerate(detailColumns):
            columnData = self.Read_table_column(partID, column)
            np_posColumnData[:, i] = columnData

        # curvature data of points
        np_curvColumnData = np.empty((nrOfPoints, len(curvColumns)))
        for j, curvColumn in enumerate(curvColumns):
            curvColumnData = self.Read_table_column(partID, curvColumn)
            np_curvColumnData[:, j] = curvColumnData

        np_locationColumnData = self.Read_table_column(partID, gridLocationColumn)

        # prepare curvature data

        # delete points with no curvature information
        indexOfNan = np.argwhere(np.isnan(np_curvColumnData))
        if indexOfNan.size > 0:
            np_curvColumnData = np.delete(np_curvColumnData, indexOfNan[0, :], axis=0)
            # don't forget the points in the cloud
            np_posColumnData = np.delete(np_posColumnData, indexOfNan[0, :], axis=0)
        # replace too low and high values
        np_curvColumnData[
            np_curvColumnData > self.calcPrefs.max_curvature
        ] = self.calcPrefs.max_curvature
        np_curvColumnData[
            np_curvColumnData < -self.calcPrefs.max_curvature
        ] = -self.calcPrefs.max_curvature

        return np_posColumnData, np_curvColumnData, np_locationColumnData

    def getBoxData(
        self,
        part: PartInfoClass,
        boxDeltaColumns: List[str],
        boxCoordColumns: List[str],
        boxDirColumns: List[str],
    ) -> Tuple[np.ndarray, np.ndarray]:

        partID = part.getTotalID()
        boxData = self.Read_single_row_table(
            self.paths.namedata_minimalboundingbox, partID
        )  # type: Table.row

        boxDeltas = []
        for colName in boxDeltaColumns:
            boxDeltas.append(
                np.around(boxData[colName], self.calcPrefs.digits_round_pos)
            )
        boxCoords = []
        for colName in boxCoordColumns:
            boxCoords.append(
                np.around(boxData[colName], self.calcPrefs.digits_round_pos)
            )
        boxDirs = []
        for colName in boxDirColumns:
            boxDirs.append(boxData[colName])

        return boxDeltas, boxCoords, boxDirs


class Detail_Transformation_Class(Pytables_Update_Class):
    def __init__(self, paths: PathsClass, name: str):
        self.paths = paths
        super().__init__(self.paths, name)
        self.transformationColumns = self.__transformationColumns__()

    def saveTransformations(
        self,
        part_a: PartInfoClass,
        parts_b: List[PartInfoClass],
        parts_b_old: List[PartInfoClass],
        GS_PartPairclass_list: List[GS_PartPairclass],
    ):
        numberOfNewParts = len(parts_b) - len(parts_b_old)
        if numberOfNewParts > 0:
            IDSet = self.__IDSet__(parts_b_old)

            # build np.ndarray for new transformation data
            transformationData = np.ndarray(
                numberOfNewParts, dtype=self.transformationColumns
            )
            partCounter = 0

            for partPair in GS_PartPairclass_list:
                if not partPair.ID_b in IDSet:
                    transformationData[partCounter] = self.__writeTransformationRow__(
                        partPair.ID_a,
                        partPair.ID_b,
                        (partPair.pose_a.t, partPair.pose_a.R),
                        (partPair.pose_b.t, partPair.pose_b.R),
                        False,
                    )
                    partCounter += 1

            # get table
            transformationTable = self.BuildOrOpenTable(
                "", self.paths.transformation_table, self.transformationColumns
            )  # type: Table
            transformationTable.append(transformationData)
            transformationTable.flush()

    def __transformationColumns__(self) -> np.dtype:
        return np.dtype(
            [
                (self.paths.part_id + "_a", bytes, self.paths.IDLength),
                (self.paths.part_id + "_b", bytes, self.paths.IDLength),
                ("t1_a", np.float),
                ("t2_a", np.float),
                ("t3_a", np.float),
                ("t1_b", np.float),
                ("t2_b", np.float),
                ("t3_b", np.float),
                ("r1_a", np.float),
                ("r2_a", np.float),
                ("r3_a", np.float),
                ("r4_a", np.float),
                ("r5_a", np.float),
                ("r6_a", np.float),
                ("r7_a", np.float),
                ("r8_a", np.float),
                ("r9_a", np.float),
                ("r1_b", np.float),
                ("r2_b", np.float),
                ("r3_b", np.float),
                ("r4_b", np.float),
                ("r5_b", np.float),
                ("r6_b", np.float),
                ("r7_b", np.float),
                ("r8_b", np.float),
                ("r9_b", np.float),
                (self.paths.transformation_file, np.int),
            ]
        )

    def __writeTransformationRow__(
        self, part_0, part_1, part_0_data, part_1_data, fileStatus
    ) -> np.ndarray:
        rowArray = np.ndarray(1, dtype=self.transformationColumns)

        rowArray[self.paths.part_id + "_a"] = part_0
        rowArray[self.paths.part_id + "_b"] = part_1

        # -
        part_0_t = part_0_data[0]
        rowArray["t1_a"] = part_0_t[0]
        rowArray["t2_a"] = part_0_t[1]
        rowArray["t3_a"] = part_0_t[2]
        # -
        part_1_t = part_1_data[0]
        rowArray["t1_b"] = part_1_t[0]
        rowArray["t2_b"] = part_1_t[1]
        rowArray["t3_b"] = part_1_t[2]
        # -
        part_0_r = part_0_data[1]
        part_0_r0 = part_0_r[:, 0]
        rowArray["r1_a"] = part_0_r0[0]
        rowArray["r2_a"] = part_0_r0[1]
        rowArray["r3_a"] = part_0_r0[2]

        part_0_r1 = part_0_r[:, 1]
        rowArray["r4_a"] = part_0_r1[0]
        rowArray["r5_a"] = part_0_r1[1]
        rowArray["r6_a"] = part_0_r1[2]

        part_0_r2 = part_0_r[:, 2]
        rowArray["r7_a"] = part_0_r2[0]
        rowArray["r8_a"] = part_0_r2[1]
        rowArray["r9_a"] = part_0_r2[2]
        # -
        part_1_r = part_1_data[1]
        part_1_r0 = part_1_r[:, 0]
        rowArray["r1_b"] = part_1_r0[0]
        rowArray["r2_b"] = part_1_r0[1]
        rowArray["r3_b"] = part_1_r0[2]

        part_1_r1 = part_1_r[:, 1]
        rowArray["r4_b"] = part_1_r1[0]
        rowArray["r5_b"] = part_1_r1[1]
        rowArray["r6_b"] = part_1_r1[2]

        part_1_r2 = part_1_r[:, 2]
        rowArray["r7_b"] = part_1_r2[0]
        rowArray["r8_b"] = part_1_r2[1]
        rowArray["r9_b"] = part_1_r2[2]

        # -
        rowArray[self.paths.transformation_file] = int(fileStatus)

        return rowArray

    def __IDSet__(self, parts: List[PartInfoClass]) -> set:
        IDSet = set()
        for part in parts:
            IDSet.add(part.getTotalID())
        return IDSet

    def assignPartData(
        self,
        partPairs: List[Tuple[PartInfoClass, PartInfoClass]],
        transformationData: np.ndarray,
    ) -> Dict[
        Tuple[str, str],
        Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], bool],
    ]:
        """Output = {
            (PartID_0, PartID_1): (
                ( Translation_0 (3,), Translation_1 (3,) ),
                ( Rotation_0 (3,3), Rotation_1 (3,3) ),
                bool existence of overlay file
            )
        }"""

        part_a_List = []
        part_b_List = []
        outputDict = {}
        for pair in partPairs:
            part_a_ID = pair[0].getTotalID()
            part_b_ID = pair[1].getTotalID()
            part_a_List.append(part_a_ID.encode("utf-8"))
            part_b_List.append(part_b_ID.encode("utf-8"))
            part_a_sort = part_a_ID.encode("utf-8")
            part_b_sort = part_b_ID.encode("utf-8")
            posRows_a = np.where(
                transformationData[self.paths.part_id + "_a"] == part_a_sort
            )[0]
            for posRow_a in posRows_a:
                dataRow_a = transformationData[posRow_a]
                if dataRow_a[self.paths.part_id + "_b"] == part_b_sort:
                    tR = dataRow_a

                    part_0_ID = tR[self.paths.part_id + "_a"].decode("utf-8")
                    pos_a = "_a"
                    pos_b = "_b"
                    if part_a_ID != part_0_ID:
                        pos_a = "_b"
                        pos_b = "_a"

                    part_a_t = np.array(
                        [tR["t1" + pos_a], tR["t2" + pos_a], tR["t3" + pos_a]]
                    )
                    part_b_t = np.array(
                        [tR["t1" + pos_b], tR["t2" + pos_b], tR["t3" + pos_b]]
                    )

                    part_a_r = np.array(
                        [
                            [tR["r1" + pos_a], tR["r4" + pos_a], tR["r7" + pos_a]],
                            [tR["r2" + pos_a], tR["r5" + pos_a], tR["r8" + pos_a]],
                            [tR["r3" + pos_a], tR["r6" + pos_a], tR["r9" + pos_a]],
                        ]
                    )
                    part_b_r = np.array(
                        [
                            [tR["r1" + pos_b], tR["r4" + pos_b], tR["r7" + pos_b]],
                            [tR["r2" + pos_b], tR["r5" + pos_b], tR["r8" + pos_b]],
                            [tR["r3" + pos_b], tR["r6" + pos_b], tR["r9" + pos_b]],
                        ]
                    )

                    outputDict[(part_a_ID, part_b_ID)] = (
                        (part_a_t, part_b_t),
                        (part_a_r, part_b_r),
                        bool(tR[self.paths.transformation_file]),
                    )

        return outputDict

    def outputTransformations(
        self, partPairs: List[Tuple[PartInfoClass, PartInfoClass]]
    ) -> Dict[
        Tuple[str, str],
        Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], bool],
    ]:
        """Output = {
            (PartID_0, PartID_1): (
                ( Translation_0 (3,), Translation_1 (3,) ),
                ( Rotation_0 (3,3), Rotation_1 (3,3) ),
                bool existence of overlay file
            )
        }"""

        conditions_Str = self.__partPairConditions(partPairs)

        transformationsParts = self.Read_table_readWhere(
            self.paths.transformation_table, conditions_Str
        )

        outputDict = {}
        if not transformationsParts is None and len(transformationsParts) > 0:
            outputDict = self.assignPartData(partPairs, transformationsParts)
        return outputDict

    def setFileStatus(
        self,
        partPairs: List[Tuple[PartInfoClass, PartInfoClass]],
        status: List[bool] = False,
    ):
        conditions_Str = self.__partPairConditions(partPairs)
        boolValueList = [int(status_i) for status_i in status]

        self.Write_table_where(
            self.paths.transformation_table,
            conditions_Str,
            [self.paths.transformation_file],
            boolValueList,
        )

    def deletePartPairs(self, partPairs: List[Tuple[PartInfoClass, PartInfoClass]]):

        Tablepath = self.root + self.paths.transformation_table
        if self.pytables_file.__contains__(Tablepath):
            conditions_Str = self.__partPairConditions(partPairs)
            table = self.pytables_file.get_node(Tablepath)  # type: Table
            rows_partPairs = table.get_where_list(conditions_Str)  # type: List[int]
            rows_partPairs_sorted = sorted(rows_partPairs, reverse=True)

            for row in rows_partPairs_sorted:
                table.remove_row(row)
            table.flush()
            table.close()

    def __partPairConditions(
        self, partPairs: List[Tuple[PartInfoClass, PartInfoClass]]
    ) -> str:
        conditions = []
        for pair in partPairs:
            if isinstance(pair[0], str):
                part_a_ID = pair[0]
                part_b_ID = pair[1]
            elif isinstance(pair[0], PartInfoClass):
                part_a_ID = pair[0].getTotalID()
                part_b_ID = pair[1].getTotalID()

            condition = "(({} == b'{}') & ({} == b'{}'))".format(
                self.paths.part_id + "_a",
                part_a_ID,
                self.paths.part_id + "_b",
                part_b_ID,
            )
            conditions.append(condition)

        return "|".join(conditions)
