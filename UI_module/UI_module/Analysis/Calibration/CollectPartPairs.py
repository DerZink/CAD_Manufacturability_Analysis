CADTool_path = (
    r"D:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module"
)
configPath = r"D:\04_Arbeitsordner_lokal_sync\CAD_Manufacturability_Analysis\UI_module\UI_module\Shared"

import itertools
import sys
import os
import pickle as _pi
import numpy as np
from typing import List, Tuple, Dict

sys.path.append(CADTool_path)
from Analysis.Pytable.Pytables_Management_Functions import Pytables_Update_Class
from Analysis.Calibration.GeometricSimilarityClasses.FEM_PartPairClass import (
    FEM_BodyPairClass,
)
from Shared.Preferences import PreferencesClass, calcPrefClass, detailColumnsClass
from Shared.Paths import PathsClass


class PairLoader:
    def __init__(self):
        ## set config ##
        self.preferences = PreferencesClass(path=configPath)
        # Paths
        self.paths = self.preferences.getPaths()
        # Calculation preferences

        self.featureH5 = Pytables_Update_Class(self.paths, "similarity_h5")
        self.columns_calibrationTable = np.dtype(
            [
                (self.paths.part_a, bytes, self.paths.IDLength),
                (self.paths.part_b, bytes, self.paths.IDLength),
                (self.paths.manufacturing_similarity_gs, np.float64),
                (self.paths.manufacturing_similarity_fs, np.float64),
            ]
        )

    def clearTable(self):
        self.featureH5.Clear_Table(self.paths.calibration_table)

    def fillTable(self, data: List[Tuple]):

        arrayData = np.array(data, dtype=self.columns_calibrationTable)
        self.featureH5.appendTable(self.paths.calibration_table, arrayData)

    def getBodiesInfos(self, dataBasePath):
        filesInFolder = os.listdir(dataBasePath)  # type: List[str]
        bodyFiles = [
            fileX.split(".prt")[0] for fileX in filesInFolder if fileX.endswith(".prt")
        ]
        bodyNamesIDs = self.__getBodyIDs__(bodyFiles)

        # translationDict = {
        #     "Box": "Wuerfel",
        #     "Hemisphere": "Hemisphaere",
        #     "Pyramid": "Pyramide",
        #     "Pyramid4": "Pyramide4",
        # }
        # bodyNamesIDs = {}
        # # bodyClasses.add(name.split("_")[0])
        # if len(translationDict) > 0:
        #     for bodyName in bodyNamesIDs_input.keys():
        #         bodyClass = bodyName.split("_")[0]
        #         translation = translationDict[bodyClass]
        #         newName = translation + "_" + "_".join(bodyName.split("_")[1:])
        #         bodyNamesIDs[newName] = bodyNamesIDs_input[bodyName]
        # else:
        #     bodyNamesIDs = bodyNamesIDs_input

        bodyClasses = {}
        for bodyName in bodyNamesIDs.keys():
            bodyClass = bodyName.split("_")[0]
            if bodyClass in bodyClasses:
                bodyClasses[bodyClass].append(bodyName)
            else:
                bodyClasses[bodyClass] = [bodyName]

        return bodyNamesIDs, bodyClasses

    def __getBodyIDs__(self, bodyNames: List[str]) -> Dict[str, str]:

        condition = condition = "|".join(
            [
                "({} == b'".format(self.paths.part_name) + str(NameX) + "')"
                for NameX in bodyNames
            ]
        )
        bodyData = self.featureH5.Read_table_readWhere(
            self.paths.features_table, condition
        )
        bodyIDs = np.char.decode(bodyData[self.paths.part_id], "utf-8")
        bodyNamesTable = np.char.decode(bodyData[self.paths.part_name], "utf-8")

        bodyDict = {}
        for x, name in enumerate(bodyNamesTable):
            bodyDict[name] = bodyIDs[x]

        return bodyDict

    def closeTable(self):
        self.featureH5.closeTable()


def bodyPairPermutation(bodyClasses: Dict[str, List[str]]):
    bodyPairList = []

    deltaDict = {
        "Box": 10,
        "Hemisphere": 30,
        "Pyramid": 15,
        "Pyramid4": 15,
        "Freiform": 1,
        "Unsymmetrisch": 1,
        "Ellipsoidenstumpf": 1,
    }
    for bodyClass in bodyClasses.keys():
        combinations = list(itertools.combinations(bodyClasses[bodyClass], 2))
        for comb in combinations:
            val_A = int(comb[0].split("_")[-1][1:])
            val_B = int(comb[1].split("_")[-1][1:])
            delta = abs(val_A - val_B)
            if delta <= deltaDict[bodyClass]:
                bodyPairList.append(comb)
                bodyPairList.append((comb[1], comb[0]))

    return bodyPairList


def bodyPairComparison(
    paths: PathsClass,
    bodyPairList: List[Tuple[str, str]],
    bodyNamesIDs: Dict[str, str],
):
    bodyPairResults = []

    bodyPairIDset = set(
        [
            (bodyNamesIDs[bodyPair[0]], bodyNamesIDs[bodyPair[0]])
            for bodyPair in bodyPairList
        ]
    )
    FEM_BodyPairclass_list = loadPickledBodyPairs(
        paths.fem_calibrationpairs, bodyPairIDset
    )

    if FEM_BodyPairclass_list is None:
        FEM_BodyPairclass_list = []
        for bodyPair in bodyPairList:
            bodyName_1 = bodyPair[0]
            bodyID_1 = bodyNamesIDs[bodyName_1]
            bodyName_2 = bodyPair[1]
            bodyID_2 = bodyNamesIDs[bodyName_2]

            bodyPairClass = FEM_BodyPairClass(
                bodyID_1=bodyID_1,
                bodyID_2=bodyID_2,
                paths=paths,
                bodyName_1=bodyName_1,
                bodyName_2=bodyName_2,
            )

            FEM_BodyPairclass_list.append(bodyPairClass)

            bodyPairResults.append(
                (
                    bodyID_1,
                    bodyID_2,
                    bodyPairClass.calcManufacturabilityMean((1, 1)),
                    np.mean(bodyPairClass.shear_rated),
                )
            )
        savePickledBodyPairs(paths.fem_calibrationpairs, FEM_BodyPairclass_list)
    else:
        for bodyPairClass in FEM_BodyPairclass_list:
            bodyPairResults.append(
                (
                    bodyPairClass.ID_a,
                    bodyPairClass.ID_b,
                    bodyPairClass.calcManufacturabilityMean((1, 1)),
                    np.mean(bodyPairClass.shear_rated),
                )
            )

    return bodyPairResults


def savePickledBodyPairs(filePath, data):
    pickleGSPairs = open(filePath, "wb")
    _pi.dump(
        (data), pickleGSPairs, _pi.HIGHEST_PROTOCOL,
    )
    pickleGSPairs.close()


def loadPickledBodyPairs(filePath, bodyPairIDset=None):
    if os.path.isfile(filePath):
        pickleGSPairs = open(filePath, "rb")
        savedClass = _pi.load(pickleGSPairs)
        if len(savedClass) == 2:
            savedClass = savedClass[0]
        pickleGSPairs.close()
        if bodyPairIDset is None:
            return savedClass
        else:
            return checkPartPairIDs(savedClass, bodyPairIDset)
    else:
        return None


def checkPartPairIDs(BodyPairsList, bodyPairIDset):
    for BodyPairClass in BodyPairsList:
        bodyPairIDs = (BodyPairClass.ID_a, BodyPairClass.ID_b)
        if not bodyPairIDs in bodyPairIDset:
            return None
    return BodyPairsList
