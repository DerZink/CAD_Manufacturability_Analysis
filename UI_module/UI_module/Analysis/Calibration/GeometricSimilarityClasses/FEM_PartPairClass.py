import copy
import os
import pickle as _pi
import sys
from typing import Dict, List, Tuple
import numpy as np
from sklearn.neighbors import NearestNeighbors

from Shared.Paths import PathsClass
from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from Analysis.Calibration.erhf5_Data import erhf5_Data

# translationDict = {
#     "Box": "Wuerfel",
#     "Hemisphere": "Hemisphaere",
#     "Pyramid": "Pyramide",
#     "Pyramid4": "Pyramide4",
# }


class FEM_BodyPairClass:
    def __init__(
        self,
        bodyID_1: str,
        bodyID_2: str,
        paths: PathsClass,
        bodyName_1: str = None,
        bodyName_2: str = None,
    ):
        self.paths = paths
        self.FEMFolder = self.paths.path_fem

        self.ID_a = bodyID_1
        self.ID_b = bodyID_2

        if bodyName_1 is None or bodyName_2 is None:
            bodyID2NameDict = self.__getNamesFromIDs__([bodyID_1, bodyID_2])
            self.bodyName_1 = bodyID2NameDict[self.ID_a]
            self.bodyName_2 = bodyID2NameDict[self.ID_b]
        else:
            self.bodyName_1 = bodyName_1
            self.bodyName_2 = bodyName_2

        self.bodyFEMdata_1, self.bodyFEMdata_2 = self.__readBodyFEMdata__(
            [self.bodyName_1, self.bodyName_2]
        )

        self.__initComparison__()

    def __getNamesFromIDs__(self, bodyIDs: List[str]) -> Dict[str, str]:
        featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")
        condition = condition = "|".join(
            [
                "({} == b'".format(self.paths.part_id) + str(IDX) + "')"
                for IDX in bodyIDs
            ]
        )
        bodysData = featureH5.Read_table_readWhere(self.paths.features_table, condition)

        bodyIDs = np.char.decode(bodysData[self.paths.part_id], "utf-8")
        bodyNamesTable = np.char.decode(bodysData[self.paths.part_name], "utf-8")

        featureH5.closeTable()

        bodyID2NameDict = {}
        for x, ID in enumerate(bodyIDs):
            bodyID2NameDict[ID] = bodyNamesTable[x]

        return bodyID2NameDict

    def __readBodyFEMdata__(self, bodyNames: List[str]) -> List[Dict[str, np.ndarray]]:
        resultEnding = "_RESULT.erfh5"
        resultList = []
        for name in bodyNames:
            bodyClass = name.split("_")[0]
            # if bodyClass in translationDict:
            #     bodyClass = translationDict[bodyClass]

            bodyFolder = os.path.join(self.FEMFolder, bodyClass)

            bodyName = bodyClass + "_" + "_".join(name.split("_")[1:])
            bodyFEMdata_raw = erhf5_Data(
                bodyFolder, os.path.join(bodyFolder, bodyName + resultEnding)
            ).formedNodesTextile_list

            resultList.append(self.__transformFEMData__(bodyFEMdata_raw))

        return resultList

    def __transformFEMData__(
        self, bodyFEMdata: List[Tuple[np.array, np.array, float, float]]
    ) -> Dict[str, np.ndarray]:
        nodes = len(bodyFEMdata)
        startCoords = np.empty(shape=(nodes, 2))
        endCoords = np.empty(shape=(nodes, 3))
        shearValues = np.empty(shape=(nodes,))
        distanceValues = np.empty(shape=(nodes,))
        for i, dataRow in enumerate(bodyFEMdata):
            startCoords[i][0] = dataRow[0][0]
            startCoords[i][1] = dataRow[0][1]
            endCoords[i][0] = dataRow[1][0]
            endCoords[i][1] = dataRow[1][1]
            endCoords[i][2] = dataRow[1][2]
            shearValues[i] = abs(dataRow[2])
            distanceValues[i] = abs(dataRow[3])

        return {
            "startCoords": startCoords,
            "endCoords": endCoords,
            "shearValues": shearValues,
            "distanceValues": distanceValues,
        }

    def __initComparison__(self):
        # learn as for GS data
        # nbrs_endCoords2 = NearestNeighbors(
        #     n_neighbors=1, algorithm="auto", n_jobs=-1
        # ).fit(self.bodyFEMdata_2["endCoords"])

        # distances_endCoords, indices_endCoords2 = nbrs_endCoords2.kneighbors(
        #     self.bodyFEMdata_1["endCoords"]
        # )

        nbrs_endCoords1 = NearestNeighbors(
            n_neighbors=1, algorithm="auto", n_jobs=-1
        ).fit(self.bodyFEMdata_1["endCoords"])

        distances_endCoords, self.indices_endCoords1 = nbrs_endCoords1.kneighbors(
            self.bodyFEMdata_2["endCoords"]
        )

        # distances_endCoords = distances_endCoords.reshape(len(indices_endCoords2))
        distances_endCoords = distances_endCoords.reshape(len(self.indices_endCoords1))

        # self.dataShear_2 = self.bodyFEMdata_2["shearValues"][
        #     indices_endCoords2
        # ].reshape(len(indices_endCoords2))

        self.dataShear_1 = self.bodyFEMdata_1["shearValues"][
            self.indices_endCoords1
        ].reshape(len(self.indices_endCoords1))

        minDistance = min(distances_endCoords)
        maxDistance = max(distances_endCoords)

        distances_endCoords[distances_endCoords > maxDistance] = maxDistance
        self.distances_rated = (maxDistance - distances_endCoords) / (
            maxDistance - minDistance
        )
        # self.minShearValue = 5
        # changedShearValues = copy.deepcopy(self.bodyFEMdata_1["shearValues"])
        # changedShearValues[changedShearValues < self.minShearValue] = self.minShearValue
        # self.shear_ratedOld = (
        #     1
        #     - np.abs(self.bodyFEMdata_1["shearValues"] - dataShear_2)
        #     / self.bodyFEMdata_1["shearValues"]
        # )
        # self.shear_rated = (
        #     1
        #     - np.abs(self.bodyFEMdata_1["shearValues"] - dataShear_2)
        #     / changedShearValues
        # )
        # self.shear_rated[self.shear_rated < 0] = 0
        # maxShear = np.max(self.bodyFEMdata_1["shearValues"])
        # minShear = np.min(self.bodyFEMdata_1["shearValues"])
        # self.shearValRating = (maxShear - self.bodyFEMdata_1["shearValues"]) / (
        #     maxShear - minShear
        # )

        # self.shear_rated = 1 - (
        #     np.abs(self.bodyFEMdata_1["shearValues"] - self.dataShear_2) / 20
        # )
        self.shear_rated = 1 - (
            np.abs(self.dataShear_1 - self.bodyFEMdata_2["shearValues"]) / 20
        )

        self.shear_rated[self.shear_rated < 0] = 0

        self.shearTextileStructure = self.shearTextileStructureFunc()
        # self.shearTextileStructure = (
        #     self.bodyFEMdata_2["shearValues"] - self.dataShear_1
        # ) / 20

        # self.shearTextileStructure[self.shearTextileStructure < -1] = -1
        # self.shearTextileStructure[self.shearTextileStructure > 1] = 1

        # self.shearTextileStructure += 1
        # self.shearTextileStructure = self.shearTextileStructure * 0.5

        self.OC_tuple = [
            self.distances_rated,
            self.shear_rated,
        ]

        self.OC_ln_tuple = [
            self.ln(self.distances_rated),
            self.ln(self.shear_rated),
        ]

    def shearTextileStructureFunc(self):
        shearTextileStructure = self.bodyFEMdata_2["shearValues"] - self.dataShear_1
        shearTextileStructure[shearTextileStructure > 20] = 20
        shearTextileStructure[shearTextileStructure < -20] = -20
        shearTextileStructure = 1 / 40 * shearTextileStructure + 0.5
        return shearTextileStructure

    def calcManufacturability(self, x=(1, 1)):
        if x[0] < 0.0 or x[1] < 0.0:
            print("MINUS: ", x)
            return 1e40

        return np.average(
            self.shear_rated ** x[1], weights=(self.distances_rated) ** x[0],
        )

    def calcManufacturabilityMean(self, x=(1, 1)):
        if x[0] < 0.0 or x[1] < 0.0:
            print("MINUS: ", x)
            return 1e40

        return np.sum((1 * self.shear_rated ** x[1] + self.distances_rated ** x[0])) / (
            2 * self.shear_rated.shape[0]
        )

    def getJacobian_X(self, x_in):
        jacobian = np.empty(len(x_in))

        OC_d = self.OC_tuple[0] ** x_in[0]
        OC_s = self.OC_tuple[1] ** x_in[1]

        OC_d_sum = np.sum(OC_d)

        OC_d_OC_s_lnOC_d_sum = np.sum(OC_d * OC_s * self.OC_ln_tuple[0])
        OC_d_OC_s_sum = np.sum(OC_d * OC_s)

        OC_d_OC_s_lnOC_s_sum = np.sum(OC_d * OC_s * self.OC_ln_tuple[1])

        # f'g:
        fg = OC_d_OC_s_lnOC_d_sum * OC_d_sum
        # g'f:
        OC_d_lnOC_d = np.sum(OC_d * self.OC_ln_tuple[0])
        gf = OC_d_lnOC_d * OC_d_OC_s_sum
        # (f/g)'
        jacobian[0] = (fg - gf) / (OC_d_sum ** 2)

        jacobian[1] = OC_d_OC_s_lnOC_s_sum / OC_d_sum

        return jacobian

    def getHessian_X(self, x_in):
        hessian = np.empty((len(x_in), len(x_in)))

        OC_d = self.OC_tuple[0] ** x_in[0]
        OC_s = self.OC_tuple[1] ** x_in[1]

        OC_d_sum = np.sum(OC_d)

        OC_d_lnOC_d2 = np.sum(OC_d * (self.OC_ln_tuple[0] ** 2))
        OC_d_OC_s_lnOC_d2_sum = np.sum(OC_d * OC_s * (self.OC_ln_tuple[0] ** 2))
        OC_d_OC_s_sum = np.sum(OC_d * OC_s)
        OC_d_lnOC_d_sum = np.sum(OC_d * self.OC_ln_tuple[0])
        OC_d_OC_s_lnOC_d_sum = np.sum(OC_d * OC_s * self.OC_ln_tuple[0])

        OC_d_OC_s_lnOC_d_lnOC_s = np.sum(
            OC_d * OC_s * self.OC_ln_tuple[0] * self.OC_ln_tuple[1]
        )
        OC_d_OC_s_lnOC_s_sum = np.sum(OC_d * OC_s * self.OC_ln_tuple[1])

        OC_d_OC_s_lnOC_s2 = np.sum(OC_d * OC_s * (self.OC_ln_tuple[1] ** 2))

        hessian[0, 0] = (
            1
            / OC_d_sum ** 4
            * (
                (OC_d_OC_s_lnOC_d2_sum * OC_d_sum - OC_d_lnOC_d2 * OC_d_OC_s_sum)
                * OC_d_sum ** 2
                - 2
                * OC_d_sum
                * OC_d_lnOC_d_sum
                * (OC_d_OC_s_lnOC_d_sum * OC_d_sum - OC_d_lnOC_d_sum * OC_d_OC_s_sum)
            )
        )

        hessian[0, 1] = hessian[1, 0] = (1 / OC_d_sum ** 2) * (
            OC_d_OC_s_lnOC_d_lnOC_s * OC_d_sum - OC_d_lnOC_d_sum * OC_d_OC_s_lnOC_s_sum
        )

        hessian[1, 1] = OC_d_OC_s_lnOC_s2 / OC_d_sum

        return hessian

    def ln(self, array: np.ndarray):
        return np.log(array, where=(array != 0.0))
