from typing import Dict, List, Tuple

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot
from scipy.optimize import lsq_linear, minimize, Bounds

from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from Shared.Paths import PathsClass


class CalibrationFeatureSimilarity(QtCore.QObject):
    finished = Signal(object)

    def __init__(self, paths: PathsClass, featureSimilarityColumns: Dict[str, list]):
        super().__init__()
        self.paths = paths
        self.featureSimilarityColumns = featureSimilarityColumns

        self.type = "majorCategories"  # allCategories
        self.limits = [0.01, 1.0]
        self.sumConstraint = {
            "type": "eq",
            "fun": lambda x: round(abs(np.sum(x) - 1), 10),
        }

        self.__countCategories__()

    def __countCategories__(self):
        self.histrogramFeatures = set()

        self.featuresList = []
        self.numberOfAllUsedFeatures = 0
        numberOfHistogrammCategories = 0

        for category in self.featureSimilarityColumns:
            featuresOfCat = self.featureSimilarityColumns[category]
            self.numberOfAllUsedFeatures += len(featuresOfCat)
            if not "value" in category:
                numberOfHistogrammCategories += 1
                self.histrogramFeatures.update(featuresOfCat)

                if self.type == "allCategories":
                    self.featuresList.extend(featuresOfCat)
                else:
                    self.featuresList.append(category)
            else:
                self.featuresList.extend(featuresOfCat)

        self.numberOfFeatures = len(self.featuresList)

    def start(self, calibrationData: np.ndarray = None):

        self.calibrationData = calibrationData
        self.__readData__()
        self.__equationSystem_Ay__()
        self.__regressionCalculation__()
        self.__outputCalibration__()

    def getSavedConfiguration(self) -> Tuple[np.ndarray, np.ndarray]:
        self.calibrationData = None
        self.__readData__()
        self.__equationSystem_Ay__()
        return (self.A, self.y)

    def __readData__(self):
        featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")

        # load calibration part pairs
        if self.calibrationData is None:
            calibrationDataPath = featureH5.root + self.paths.calibration_table
            self.calibrationData = featureH5.Read_entire_table(calibrationDataPath)

        if self.calibrationData.shape[0] > 0:
            partIDs = set()
            for partPair in self.calibrationData:
                partIDs.add(partPair[0])
                partIDs.add(partPair[1])

            # get feature data of parts
            condition = "|".join(
                [
                    "({} == ".format(self.paths.part_id) + str(IDx) + ")"
                    for IDx in partIDs
                ]
            )
            self.featureData = featureH5.Read_table_readWhere(
                self.paths.features_table, condition
            )
        featureH5.closeTable()

    def __equationSystem_Ay__(self):
        self.A = np.ones((len(self.calibrationData), self.numberOfFeatures))
        self.y = np.ones((len(self.calibrationData)))
        for i_pair in range(len(self.calibrationData)):

            bodyPair = self.calibrationData[i_pair]

            row_1 = np.where(self.featureData[self.paths.part_id] == bodyPair[0])[0][0]
            row_2 = np.where(self.featureData[self.paths.part_id] == bodyPair[1])[0][0]

            for i, featureCat in enumerate(self.featuresList):

                if featureCat in self.featureSimilarityColumns:
                    ## if type == majorCategories -> histogram categories are grouped
                    diffValue_cat = 0
                    for histCat in self.featureSimilarityColumns[featureCat]:
                        value_1 = self.featureData[row_1][histCat]
                        value_2 = self.featureData[row_2][histCat]
                        diffValue_cat += self.__diffHistogram__(value_1, value_2)
                else:
                    ## if type == allCategories -> each feature of the histogram categories is taken
                    value_1 = self.featureData[row_1][featureCat]
                    value_2 = self.featureData[row_2][featureCat]
                    if featureCat in self.histrogramFeatures:
                        diffValue_cat = self.__diffHistogram__(value_1, value_2)
                    else:
                        diffValue_cat = self.__diffReferenced__(value_1, value_2)
                self.A[i_pair][i] = diffValue_cat

            self.y[i_pair] = bodyPair[3]

    def __diffReferenced__(self, value_1: float, value_2: float):
        difference = abs(value_2 - value_1)
        if difference >= value_1:
            return 0
        else:
            return min(1, 1 - difference / value_1)

    def __diffHistogram__(self, value_1: float, value_2: float):
        return min(1, min(value_1, value_2))

    def __regressionCalculation__(self):

        ## Scipy least square solver
        lsq_0 = lsq_linear(
            self.A,
            self.y,
            bounds=(self.limits[0], self.limits[1]),
            method="trf",
            verbose=0,
        )

        ## Minimization of vector x to given restrictions self.weightingLimits & self.weightingSum
        boundClass = Bounds(
            [self.limits[0]] * self.numberOfFeatures,
            [self.limits[1]] * self.numberOfFeatures,
            keep_feasible=True,
        )
        lsqSolution = minimize(
            self.MSEcalc,
            lsq_0.x,
            args=(self.A, self.y),
            method="SLSQP",
            bounds=boundClass,
            constraints=self.sumConstraint,
            jac=self.jacCall,
        )
        # lsqSolution = minimize(
        #     self.MSEcalc,
        #     lsq_0.x,
        #     args=(self.A, self.y),
        #     method="trust-constr",
        #     bounds=boundClass,
        #     constraints=self.sumConstraint,
        #     jac=self.jacCall,
        #     hess=self.hessCall,
        # )

        self.weights = lsqSolution.x

    @staticmethod
    def jacCall(x, *args):
        A = args[0]
        y = args[1]
        jacOut = np.zeros(len(x))
        for a_row in range(A.shape[0]):
            jacOut += (A[a_row].dot(x) - y[a_row]) * A[a_row]
        return 2 / A.shape[0] * jacOut

    @staticmethod
    def hessCall(x, *args):
        A = args[0]
        return 2 / A.shape[0] * A.T.dot(A)

    @staticmethod
    def MSEcalc(x, A, y):
        # return np.linalg.norm(A.dot(x) - y)  # Means Squared Error?
        return np.square(A.dot(x) - y).mean(axis=0)

    def MSE_FScalibration(self):
        return self.MSEcalc(self.weights, self.A, self.y)

    @Slot(object)
    def __outputCalibration__(self):
        print("Finished FS calibration")
        self.finished.emit((self.A, self.y, self.weights))
