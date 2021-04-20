# -*- coding: utf-8 -*-
"""
Calculating Feature Similarity
"""
import multiprocessing as mp
import os
from typing import Dict, List, Tuple

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import Signal
from tables import *

from Analysis.Pytable.Pytables_Feature_Analysis import Feature_Similarity_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass


class CalcFeatureSimilarity(QtCore.QObject):
    """Class for calculation of feature similarity in H5 data (PyTables)
        Input:
                - Global paths as PathsClass
                - Similarity features"""

    updateDatabase = Signal(bool)

    def __init__(
        self,
        partList: List[PartInfoClass],
        pathsInput: PathsClass,
        calcPrefs: calcPrefClass,
        featureColumns: List[Tuple[str, str]],
        featureSimilarityColumns: Dict[str, list],
    ):
        super().__init__()
        self.partList = partList
        self.paths = pathsInput
        self.calcPrefs = calcPrefs
        self.featureWeights = {
            f[0]: f[1] for f in featureColumns
        }  # type: Dict[str, str]
        self.featureSimilarityColumns = (
            featureSimilarityColumns
        )  # type: Dict[str, list]

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.start)

    def start(self):

        partIDList = []
        for partInput in self.partList:
            partIDList.append(partInput.getTotalID())

        self.Similarity_H5 = Feature_Similarity_Class(
            partIDList,
            self.paths,
            self.calcPrefs,
            self.featureWeights,
            self.featureSimilarityColumns,
        )

        self.simCalcExpr()

        self.Similarity_H5.buildSimilarityTables(self.poolResults)

        self.thread.quit()
        self.updateDatabase.emit(True)

    def simCalcExpr(self):
        """Use Numexpr with Pytables to calculate Feature Similarity"""
        calcFeatureSumPool = mp.Pool(2)
        poolResults = []
        for i in range(len(self.Similarity_H5.featureCalcVariablesList)):
            poolResults.append(
                calcFeatureSumPool.apply_async(
                    self.Similarity_H5.runCalculation, args=(i,)
                )
            )
        calcFeatureSumPool.close()
        calcFeatureSumPool.join()
        self.poolResults = []
        for result in poolResults:
            self.poolResults.append(result.get())

    def __indexNewParts(self, partList: List[PartInfoClass]) -> List[int]:
        partIDs = [x.getTotalID() for x in partList]  # type: List[str]

        HDF5_Path = os.path.join(
            self.paths.path_analyticaldatabase, self.paths.similarity_h5
        )
        pytables_file = open_file(HDF5_Path, mode="r")
        path_FeatureTable = pytables_file.root._v_name + self.paths.features_table
        featureTable = pytables_file.get_node(path_FeatureTable)  # type: Table
        condotionStr = ""
        for partID in partIDs:
            condotionStr += "({} == b'{}') | ".format(self.paths.part_id, partID)
        condotionStr = condotionStr[:-3]
        rows_newParts = featureTable.get_where_list(condotionStr, sort=True)
        rows_oldParts = np.setxor1d(np.arange(0, featureTable.nrows, 1), rows_newParts)
        ids_oldParts = featureTable.read_coordinates(
            rows_oldParts, field=self.paths.part_id
        )
        pytables_file.close()
        return rows_newParts, ids_oldParts
