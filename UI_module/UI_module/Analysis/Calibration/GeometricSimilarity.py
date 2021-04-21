import copy
import os
import pickle as _pi
import sys
from typing import Dict, List, Tuple

import cProfile, pstats, io
from pstats import SortKey

import matplotlib.pyplot as plt
import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot
from scipy.optimize import (
    Bounds,
    NonlinearConstraint,
    brute,
    differential_evolution,
    dual_annealing,
    basinhopping,
    minimize,
    shgo,
)
from sklearn.neighbors import NearestNeighbors
from skopt import gp_minimize
from skopt.utils import use_named_args
from skopt.plots import plot_convergence, plot_objective
from skopt.learning import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF,
    Matern,
    RationalQuadratic,
    ExpSineSquared,
    DotProduct,
    ConstantKernel,
)
import multiprocessing as mp

from Analysis.Evaluation.DetailSimilarity import CalcDetailSimilarity
from Analysis.Evaluation.DetailSimilarityClasses.PartPairClass import GS_PartPairclass
from Analysis.Pytable.Pytables_Management_Functions import Pytables_Read_Class
from Shared.PartInfo import PartInfoClass
from Shared.Paths import PathsClass
from Shared.Preferences import calcPrefClass, detailColumnsClass
from Analysis.Calibration.GeometricSimilarityClasses.FEM_PartPairClass import (
    FEM_BodyPairClass,
)


# def buildSimilarityVector(
#     x, GS_BodyPairclass_list: List[GS_PartPairclass], numberOfPartPairs: int,
# ):
#     similarityValues = np.empty(numberOfPartPairs)

#     for pairPos in range(numberOfPartPairs):
#         similarityValues[pairPos] = GS_BodyPairclass_list[pairPos].getGS_x(x)

#     return similarityValues


# def residualFunc(x, *args):

#     GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
#     objectiveValues = args[1]  # type: np.ndarray
#     numberOfPartPairs = args[2]  # type: int

#     if all(x_i > 0 for x_i in x):  # np.all(x > 0):
#         val = np.sum(
#             np.abs(
#                 buildSimilarityVector(x, GS_BodyPairclass_list, numberOfPartPairs)
#                 - objectiveValues
#             )
#         )
#         return val
#     else:
#         return False


# def jacobianFunc(x, *args):

#     GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
#     objectiveValues = args[1]  # type: np.ndarray
#     numberOfPartPairs = args[2]  # type: int

#     jacobian = np.zeros(len(x))
#     if np.all(x > 0):
#         SimilarityValues = buildSimilarityVector(
#             x, GS_BodyPairclass_list, numberOfPartPairs
#         )
#         ValueDiff = SimilarityValues - objectiveValues
#         signs = ValueDiff / np.abs(ValueDiff)
#         for pairPos in range(numberOfPartPairs):
#             jacobian += signs[pairPos] * np.nan_to_num(
#                 GS_BodyPairclass_list[pairPos].getJacobian_X(x)
#             )

#         return np.nan_to_num(jacobian)
#     else:
#         jacobian[:] = False
#         return jacobian


# def hessianFunc(x, *args):

#     GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
#     objectiveValues = args[1]  # type: np.ndarray
#     numberOfPartPairs = args[2]  # type: int

#     hessian = np.zeros((len(x), len(x)))
#     if np.all(x > 0):
#         SimilarityValues = buildSimilarityVector(
#             x, GS_BodyPairclass_list, numberOfPartPairs
#         )
#         ValueDiff = SimilarityValues - objectiveValues
#         signs = ValueDiff / np.abs(ValueDiff)
#         for pairPos in range(numberOfPartPairs):
#             hessian += signs[pairPos] * np.nan_to_num(
#                 GS_BodyPairclass_list[pairPos].getHessian_X(x)
#             )
#         return np.nan_to_num(hessian, posinf=1e100, neginf=-1e100)
#     else:
#         hessian[:, :] = False
#         return hessian


# def residualFuncObjective(
#     x,
#     FEM_BodyPairclass_list: List,
#     similarityValues: np.ndarray,
#     numberOfPartPairs: int,
# ):
#     objectiveValues = np.empty(numberOfPartPairs)
#     for pairPos in range(numberOfPartPairs):
#         objectiveValues[pairPos] = FEM_BodyPairclass_list[
#             pairPos
#         ].calcManufacturability(x)
#     val = np.linalg.norm(similarityValues - objectiveValues)
#     return val


# def combinedResidual(
#     x,
#     GS_BodyPairclass_list: List[GS_PartPairclass],
#     FEM_BodyPairclass_list: List,
#     numberOfPartPairs: int,
# ):
#     objectiveValues = np.empty(numberOfPartPairs)
#     similarityValues = np.empty(numberOfPartPairs)
#     for pairPos in range(numberOfPartPairs):
#         similarityValues[pairPos] = GS_BodyPairclass_list[pairPos].getGS_x(x[:11])
#         objectiveValues[pairPos] = FEM_BodyPairclass_list[
#             pairPos
#         ].calcManufacturability(x[11:])
#     # val = np.linalg.norm(similarityValues - objectiveValues)
#     val = np.max(np.abs(similarityValues - objectiveValues))
#     return val


# def constraintFunc(x):
#     return abs(np.sum(x[:4]) - 1)


# class MyBounds(object):
#     def __init__(self, xmin=[-1.1, -1.1], xmax=[1.1, 1.1]):

#         self.xmax = np.array(xmax)
#         self.xmin = np.array(xmin)

#     def __call__(self, **kwargs):

#         x = kwargs["x_new"]

#         tmax = bool(np.all(x <= self.xmax))
#         tmin = bool(np.all(x >= self.xmin))
#         xSum = bool(np.around(np.sum(x[:4]), 3) == 1)

#         return tmax and tmin and xSum


# def residualFuncConstraint(
#     x,
#     GS_BodyPairclass_list: List[GS_PartPairclass],
#     GS_Objective: List[float],
#     numberOfPartPairs: int,
# ):
#     if all(x_i > 0 for x_i in x):  # np.all(x > 0):
#         return residualFunc(
#             x, GS_BodyPairclass_list, GS_Objective, numberOfPartPairs
#         ) + constraintFunc(x)
#     else:
#         return False


class CalibrationGeometricSimilarity(QtCore.QObject):
    finished = Signal(object)

    def __init__(
        self,
        paths: PathsClass,
        detailColumns: detailColumnsClass,
        calcPrefs: calcPrefClass,
    ):
        super().__init__()
        self.paths = paths
        self.detailColumns = detailColumns
        self.calcPrefs = calcPrefs

        self.boundsLists = ([0.01] * 11, [1.0] * 4 + [1e4] * 7)
        self.boundsMin = self.boundsLists[0]
        self.boundsMax = self.boundsLists[1]
        self.boundClass = Bounds(self.boundsMin, self.boundsMax, keep_feasible=False)

        self.constraintClass = NonlinearConstraint(
            self.constraintFunc,
            0.0,
            0.0,
            jac=self.constraintJac,
            hess=self.constraintHess,
        )

        self.startParameter = [0.25] * 4 + [1.0] * 7

        self.calibrationTypes_FEM = "Mean_ShearDistMean"
        # "DistWeighted_Shear"
        # "Mean_ShearDistMean"
        # "Mean_Shear"

    def start(self, calibrationData: np.ndarray = None):
        self.calibrationData = calibrationData
        self.__getPartPairs__()
        self.__setStartParameters__()
        # self.optimizeObjective()
        self.optimizeCalibration()

    def __getPartPairs__(self):
        if self.calibrationData is None:
            featureH5 = Pytables_Read_Class(self.paths, "similarity_h5")

            # load calibration part pairs
            calibrationDataPath = featureH5.root + self.paths.calibration_table
            self.calibrationData = featureH5.Read_entire_table(calibrationDataPath)
            featureH5.closeTable()

        self.numberOfPartPairs = self.calibrationData.shape[0]
        self.part_a_IDs = np.char.decode(
            self.calibrationData[self.paths.part_a], "utf-8"
        )
        self.part_a_list = self.__IDstoPartClasses__(self.part_a_IDs)
        self.part_b_IDs = np.char.decode(
            self.calibrationData[self.paths.part_b], "utf-8"
        )
        self.part_b_list = self.__IDstoPartClasses__(self.part_b_IDs)

        self.GS_BodyPairclass_list = self.__loadPartPairs__(
            self.paths.gs_calibrationpairs
        )

        if self.GS_BodyPairclass_list is None:

            self.GSCalcClass = CalcDetailSimilarity(
                self.part_a_list,
                self.paths,
                self.detailColumns,
                self.calcPrefs,
                calibration=True,
            )
            self.GS_BodyPairclass_list = self.GSCalcClass.start_forCalibration(
                self.part_b_list, distanceRating=True
            )
            self.__savePartPairs__(
                self.paths.gs_calibrationpairs,
                (self.GS_BodyPairclass_list),
            )

        self.FEM_BodyPairclass_list = self.__loadPartPairs__(
            self.paths.fem_calibrationpairs
        )

        if self.FEM_BodyPairclass_list is None:
            self.FEM_BodyPairclass_list = []
            for i, part_a in enumerate(self.part_a_IDs):
                part_b = self.part_b_IDs[i]
                FEM_BodyPairClass_i = FEM_BodyPairClass(part_a, part_b, self.paths)
                self.FEM_BodyPairclass_list.append(FEM_BodyPairClass_i)

            self.__savePartPairs__(
                self.paths.fem_calibrationpairs, self.FEM_BodyPairclass_list
            )
        self.GS_Objective = np.empty(self.numberOfPartPairs)
        for partPos in range(self.numberOfPartPairs):
            self.GS_Objective[partPos] = self.FEM_BodyPairclass_list[
                partPos
            ].calcManufacturability((0, 1))

    def __savePartPairs__(self, filePath, data):
        pickleGSPairs = open(filePath, "wb")
        _pi.dump(
            (data),
            pickleGSPairs,
            _pi.HIGHEST_PROTOCOL,
        )
        pickleGSPairs.close()

    def __loadPartPairs__(self, filePath):
        if os.path.isfile(filePath):
            pickleGSPairs = open(filePath, "rb")
            savedClass = _pi.load(pickleGSPairs)
            if len(savedClass) == 2:
                savedClass = savedClass[0]
            pickleGSPairs.close()
            return self.__checkPartPairIDs__(savedClass)
        else:
            return None

    def __checkPartPairIDs__(self, BodyPairclass_list: List[GS_PartPairclass]):
        partPairSet = set(zip(self.part_a_IDs, self.part_b_IDs))
        for BodyPairClass in BodyPairclass_list:
            bodyPairIDs = (BodyPairClass.ID_a, BodyPairClass.ID_b)
            if not bodyPairIDs in partPairSet:
                return None
        return BodyPairclass_list

    def __IDstoPartClasses__(self, partIDs) -> List[PartInfoClass]:
        partClassList = []
        for partID in partIDs:
            partClass = PartInfoClass(partIDstr=partID, pathClass=self.paths)
            partClassList.append(partClass)
        return partClassList

    def __setStartParameters__(self):
        self.changeCountOjective = 3
        self.changeCount = 0
        self.xParameters = [
            self.calcPrefs.weight_point_distance_detail_calc,
            self.calcPrefs.weight_normal_angle_detail_calc,
            self.calcPrefs.weight_curv_radius_1_detail_calc,
            self.calcPrefs.weight_curv_radius_2_detail_calc,
            self.calcPrefs.exponent_d_point_distance_detail_calc,
            self.calcPrefs.exponent_d_normal_angle_detail_calc,
            self.calcPrefs.exponent_e_normal_angle_detail_calc,
            self.calcPrefs.exponent_d_curv_radius_min_detail_calc,
            self.calcPrefs.exponent_e_curv_radius_min_detail_calc,
            self.calcPrefs.exponent_d_curv_radius_max_detail_calc,
            self.calcPrefs.exponent_e_curv_radius_max_detail_calc,
        ]

    @staticmethod
    def constraintFunc(x):
        return round(abs(np.sum(x[:4]) - 1), 4)

    @staticmethod
    def constraintJac(x):
        return np.array([1] * 4 + [0] * (len(x) - 4))

    @staticmethod
    def constraintHess(x, v):
        l = len(x)
        return np.zeros((l, l))

    class boundsContainer(object):
        def __init__(self, xmin=[-1.1, -1.1], xmax=[1.1, 1.1]):

            self.xmax = np.array(xmax)
            self.xmin = np.array(xmin)

        def __call__(self, **kwargs):

            x = kwargs["x_new"]

            tmax = bool(np.all(x <= self.xmax))
            tmin = bool(np.all(x >= self.xmin))
            xSum = bool(CalibrationGeometricSimilarity.constraintFunc(x) == 0)

            return tmax and tmin and xSum

    @staticmethod
    def args(*args):
        FEM_BodyPairclass_list = args[0]  # type: List[FEM_BodyPairClass]
        GS_BodyPairclass_list = args[1]  # type: List[GS_PartPairclass]
        calibrationTypes_FEM = args[2]

        return (
            GS_BodyPairclass_list,
            CalibrationGeometricSimilarity.objectiveValues(
                FEM_BodyPairclass_list, calibrationTypes_FEM
            ),
            len(GS_BodyPairclass_list),
        )

    @staticmethod
    def objectiveValues(
        FEM_BodyPairclass_list: List[FEM_BodyPairClass], calibrationTypes_FEM
    ):

        if calibrationTypes_FEM == "DistWeighted_Shear":
            return np.array(
                [
                    bodyPair.calcManufacturability((1, 1))
                    for bodyPair in FEM_BodyPairclass_list
                ]
            )
        elif calibrationTypes_FEM == "Mean_ShearDistMean":
            return np.array(
                [
                    bodyPair.calcManufacturabilityMean((1, 1))
                    for bodyPair in FEM_BodyPairclass_list
                ]
            )
        elif calibrationTypes_FEM == "Mean_Shear":
            return np.array(
                [
                    bodyPair.calcManufacturability((0, 1))
                    for bodyPair in FEM_BodyPairclass_list
                ]
            )

    @staticmethod
    def buildSimilarityVector(
        x,
        GS_BodyPairclass_list: List[GS_PartPairclass],
        numberOfPartPairs: int,
    ):
        similarityValues = np.empty(numberOfPartPairs)

        for pairPos in range(numberOfPartPairs):
            similarityValues[pairPos] = GS_BodyPairclass_list[pairPos].getGS_x(x)

        return similarityValues

    @staticmethod
    def checkXpositive(x: np.ndarray) -> bool:
        return all(x_i > 0 for x_i in x)

    ##### Squared Loss ######
    @staticmethod
    def residual_squaredLoss(x, *args):

        GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
        objectiveValues = args[1]  # type: np.ndarray
        numberOfPartPairs = args[2]  # type: int

        if CalibrationGeometricSimilarity.checkXpositive(x):
            val = np.sum(
                (
                    CalibrationGeometricSimilarity.buildSimilarityVector(
                        x, GS_BodyPairclass_list, numberOfPartPairs
                    )
                    - objectiveValues
                )
                ** 2
            )
            return val
        else:
            return False

    @staticmethod
    def jacobian_squaredLoss(x, *args):

        GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
        objectiveValues = args[1]  # type: np.ndarray
        numberOfPartPairs = args[2]  # type: int

        jacobian = np.zeros(len(x))
        if CalibrationGeometricSimilarity.checkXpositive(x):
            SimilarityValues = CalibrationGeometricSimilarity.buildSimilarityVector(
                x, GS_BodyPairclass_list, numberOfPartPairs
            )
            ValueDiff = SimilarityValues - objectiveValues
            for pairPos in range(numberOfPartPairs):
                jacobian += ValueDiff[pairPos] * np.nan_to_num(
                    GS_BodyPairclass_list[pairPos].getJacobian_X(x)
                )

            return 2 * np.nan_to_num(jacobian)
        else:
            jacobian[:] = False
            return jacobian

    @staticmethod
    def hessian_squaredLoss(x, *args):

        GS_BodyPairclass_list = args[0]  # type: List[GS_PartPairclass]
        objectiveValues = args[1]  # type: np.ndarray
        numberOfPartPairs = args[2]  # type: int

        hessian = np.zeros((len(x), len(x)))
        if CalibrationGeometricSimilarity.checkXpositive(x):
            SimilarityValues = CalibrationGeometricSimilarity.buildSimilarityVector(
                x, GS_BodyPairclass_list, numberOfPartPairs
            )
            ValueDiff = SimilarityValues - objectiveValues

            for pairPos in range(numberOfPartPairs):
                jacobean = np.nan_to_num(
                    GS_BodyPairclass_list[pairPos].getJacobian_X(x)
                ).reshape([len(x), 1])
                hessian += (
                    jacobean.dot(jacobean.T)
                    + np.nan_to_num(GS_BodyPairclass_list[pairPos].getHessian_X(x))
                    * ValueDiff[pairPos]
                )

            return 2 * np.nan_to_num(hessian, posinf=1e100, neginf=-1e100)
        else:
            hessian[:, :] = False
            return hessian

    ##### Mean squared Loss ######
    @staticmethod
    def residual_meanSquaredLoss(x, *args):
        squaredLoss = CalibrationGeometricSimilarity.residual_squaredLoss(x, *args)
        if squaredLoss != False:
            return squaredLoss / args[2]
        else:
            return squaredLoss

    @staticmethod
    def jacobian_meanSquaredLoss(x, *args):
        jacobian_squaredLoss = CalibrationGeometricSimilarity.jacobian_squaredLoss(
            x, *args
        )
        if np.all(jacobian_squaredLoss != False):
            return jacobian_squaredLoss / args[2]
        else:
            return jacobian_squaredLoss

    @staticmethod
    def hessian_meanSquaredLoss(x, *args):
        hessian_squaredLoss = CalibrationGeometricSimilarity.hessian_squaredLoss(
            x, *args
        )
        if np.all(hessian_squaredLoss != False):
            return hessian_squaredLoss / args[2]
        else:
            return hessian_squaredLoss

    def callback_trustConstr(self, xi, state):
        self.callback_trustConstrList.append((xi, state))

    def callback_basinhopping(self, xi, f, accept):
        number_of_iterations = len(self.callback_trustConstrList) - self.nit_trustConstr
        self.callback_basinhoppingList.append((xi, f, accept, number_of_iterations))
        self.nit_trustConstr = len(self.callback_trustConstrList)

    def optimizeCalibration(self):
        self.nit_trustConstr = 0
        self.callback_basinhoppingList = []
        self.callback_trustConstrList = []

        trustConstr_minimizer = {
            "method": "trust-constr",
            "args": self.args(
                self.FEM_BodyPairclass_list,
                self.GS_BodyPairclass_list,
                self.calibrationTypes_FEM,
            ),
            "jac": self.jacobian_meanSquaredLoss,
            "hess": self.hessian_meanSquaredLoss,
            "bounds": self.boundClass,
            # "options": {"verbose": 3},
            "callback": self.callback_trustConstr,
            "constraints": self.constraintClass,
        }

        args_out = (
            self.residual_meanSquaredLoss,
            self.startParameter,
        )

        iterations = 100  # 500
        kwargs_out = {
            "minimizer_kwargs": trustConstr_minimizer,
            "accept_test": self.boundsContainer(self.boundsMin, self.boundsMax),
            "disp": False,
            "niter": iterations,
            "callback": self.callback_basinhopping,
            "seed": 0,
            "niter_success": int(iterations * 0.5),
        }

        self.result = basinhopping(*args_out, **kwargs_out)

    # def calcGSvalues(self, x) -> np.ndarray:
    #     similarityValues = np.empty(self.numberOfPartPairs)
    #     for pairPos in range(self.numberOfPartPairs):
    #         similarityValues[pairPos] = self.GS_BodyPairclass_list[pairPos].getGS_x(x)

    #     return similarityValues

    # def residualFuncWrapper(self, x):
    #     return residualFunc(
    #         x, self.GS_BodyPairclass_list, self.GS_Objective, self.numberOfPartPairs,
    #     )

    # def residualFuncConstraintWrapper(self, x):
    #     return residualFuncConstraint(
    #         x, self.GS_BodyPairclass_list, self.GS_Objective, self.numberOfPartPairs,
    #     )

    # def optimizeObjective(self):

    #     boundsLists = ([1e-40] * 2, [np.inf] * 2)
    #     boundsTuples = list(zip(boundsLists[0], boundsLists[1]))

    #     similarityValues = self.calcGSvalues(self.xParameters)

    #     res_SLSQP = minimize(
    #         residualFuncObjective,
    #         [1.0, 1.0],
    #         bounds=boundsTuples,
    #         args=(
    #             self.FEM_BodyPairclass_list,
    #             similarityValues,
    #             self.numberOfPartPairs,
    #         ),
    #         method="SLSQP",
    #         options={"disp": True},
    #     )
    #     print(
    #         np.around(res_SLSQP.x, 3), res_SLSQP.fun,
    #     )

    #     self.objectiveValues = np.empty(self.numberOfPartPairs)
    #     for partPos in range(self.numberOfPartPairs):
    #         self.objectiveValues[partPos] = self.FEM_BodyPairclass_list[
    #             partPos
    #         ].calcManufacturability(res_SLSQP.x)

    # def optCallback(self, xi, convergence):
    #     evVal = residualFunc(
    #         xi, self.GS_BodyPairclass_list, self.GS_Objective, self.numberOfPartPairs,
    #     )
    #     if evVal < self.MinVal:
    #         print(
    #             "{0:4d} {1: 3.4f} {2: 3.4f} {3: 3.4f} {4: 3.4f} {5: 3.4f} {6: 3.4f} {7: 3.4f} {8: 3.4f}  {9: 3.4f} {10: 3.4f} {11: 3.4f}".format(
    #                 self.Nfeval,
    #                 xi[0],
    #                 xi[1],
    #                 xi[2],
    #                 xi[3],
    #                 xi[4],
    #                 xi[5],
    #                 xi[6],
    #                 xi[7],
    #                 xi[8],
    #                 xi[9],
    #                 xi[10],
    #             )
    #         )
    #         print("evVal: ", evVal)
    #         print("conv: ", convergence)
    #         print("-" * 10)
    #         self.MinVal = evVal
    #     self.Nfeval += 1

    # def basinCallback(self, xi, f, accept):
    #     if f < self.MinVal:  # and accept == True:
    #         print(
    #             "{0:4d} {1: 3.4f} {2: 3.4f} {3: 3.4f} {4: 3.4f} {5: 3.4f} {6: 3.4f} {7: 3.4f} {8: 3.4f}  {9: 3.4f} {10: 3.4f} {11: 3.4f}".format(
    #                 self.Nfeval,
    #                 xi[0],
    #                 xi[1],
    #                 xi[2],
    #                 xi[3],
    #                 xi[4],
    #                 xi[5],
    #                 xi[6],
    #                 xi[7],
    #                 xi[8],
    #                 xi[9],
    #                 xi[10],
    #             )
    #         )
    #         print("evVal: ", f)
    #         print("-" * 10)
    #         self.MinVal = f
    #     self.Nfeval += 1

    # boundsLists = ([0.00] * 11, [1.0] * 4 + [np.inf] * 7)
    # boundsTuples = list(zip(boundsLists[0], boundsLists[1]))
    # boundsListsFloat = ([0.01] * 11, [1.0] * 4 + [1e4] * 7)
    # boundsTuplesFloat = list(zip(boundsListsFloat[0], boundsListsFloat[1]))
    # boundsListsNone = ([0.00] * 11, [1.0] * 4 + [None] * 7)
    # boundsTuplesNone = list(zip(boundsListsNone[0], boundsListsNone[1]))
    # sumConstraint = {"type": "eq", "fun": lambda x: np.sum(x[:4]) - 1}
    # sumConstraintClass = NonlinearConstraint(constraintFunc, 0.0, 0.0,)
    # self.Nfeval = 1
    # self.MinVal = np.inf

    # boundClass = Bounds(
    #     boundsListsFloat[0], boundsListsFloat[1], keep_feasible=True
    # )
    # solOut = None
    # minimizer_kwargs_0 = {
    #     "method": "SLSQP",  # "trust-constr",
    #     "args": (
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     "jac": jacobianFunc,
    #     # "hess": hessianFunc,
    #     "bounds": boundClass,
    #     "constraints": sumConstraintClass,
    # }

    # optimizerPool = mp.Pool()
    # poolResults = []
    # 1############################################################
    # boundsConstraintClass = MyBounds(boundsListsFloat[0], boundsListsFloat[1])
    # print("#" * 10, "1")
    # poolResults.append(
    #     optimizerPool.apply_async(
    #         basinhopping,
    #         args=(residualFunc, self.xParameters,),
    #         kwds={
    #             "minimizer_kwargs": minimizer_kwargs,
    #             "accept_test": boundsConstraintClass,
    #             "disp": False,
    #             "niter": 100,
    #         },
    #     )
    # )
    # sol_basinhopping = basinhopping(
    #     residualFunc,
    #     self.xParameters,
    #     minimizer_kwargs=minimizer_kwargs_0,
    #     accept_test=boundsConstraintClass,
    #     callback=self.basinCallback,
    #     disp=True,
    #     niter=10,
    # )

    # print(
    #     np.around(sol_basinhopping.x, 3), sol_basinhopping.fun,
    # )
    #############################################################

    # 2############################################################
    # print("#" * 10, "2")
    # poolResults.append(
    #     optimizerPool.apply_async(
    #         differential_evolution,
    #         args=(residualFunc,),
    #         kwds={
    #             "bounds": boundClass,
    #             "args": (
    #                 self.GS_BodyPairclass_list,
    #                 self.GS_Objective,
    #                 self.numberOfPartPairs,
    #             ),
    #             "constraints": sumConstraintClass,
    #             "polish": True,
    #             "disp": False,
    #         },
    #     )
    # )
    # sol_differential_evolution = differential_evolution(
    #     residualFunc,
    #     bounds=boundClass,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     callback=self.optCallback,
    #     constraints=sumConstraintClass,
    #     polish=True,
    #     disp=True,
    #     workers=-1,
    # )
    # print(
    #     np.around(sol_differential_evolution.x, 3), sol_differential_evolution.fun,
    # )
    #############################################################

    # 3############################################################
    # print("#" * 10, "3")
    # shgo_constraint = {"type": "eq", "fun": constraintFunc}
    # poolResults.append(
    #     optimizerPool.apply_async(
    #         shgo,
    #         args=(residualFunc, boundsTuplesFloat,),
    #         kwds={
    #             "args": (
    #                 self.GS_BodyPairclass_list,
    #                 self.GS_Objective,
    #                 self.numberOfPartPairs,
    #             ),
    #             "minimizer_kwargs": minimizer_kwargs,
    #             "constraints": shgo_constraint,
    #             "iters": 1,
    #             "options": {"disp": True},
    #         },
    #     )
    # )
    # sol_shgo = shgo(
    #     residualFunc,
    #     boundsTuplesFloat,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     minimizer_kwargs=minimizer_kwargs,
    #     constraints=shgo_constraint,
    #     options={
    #         "disp": True,
    #         "jac": jacobianFunc,
    #         "hess": hessianFunc,
    #         "infty_constraints": False,
    #     },
    # )
    # print(
    #     np.around(sol_shgo.x, 3), sol_shgo.fun,
    # )
    #############################################################

    # 4############################################################
    # print("#" * 10, "4")
    # local_search_options = {
    #     "method": "SLSQP",  # "trust-constr",
    #     "args": (
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     "jac": jacobianFunc,
    #     # "hess": hessianFunc,
    #     "constraints": sumConstraintClass,
    # }

    # poolResults.append(
    #     optimizerPool.apply_async(
    #         dual_annealing,
    #         kwds={
    #             "func": residualFunc,
    #             "x0": self.xParameters,
    #             "bounds": boundsTuplesFloat,
    #             "args": (
    #                 self.GS_BodyPairclass_list,
    #                 self.GS_Objective,
    #                 self.numberOfPartPairs,
    #             ),
    #             "local_search_options": local_search_options,
    #         },
    #     )
    # )

    # sol_dual_annealing = dual_annealing(
    #     func=residualFunc,
    #     x0=self.xParameters,
    #     bounds=boundsTuplesFloat,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     local_search_options=local_search_options,
    #     callback=self.basinCallback,
    # )
    # print(
    #     np.around(sol_dual_annealing.x, 3), sol_dual_annealing.fun,
    # )
    #############################################################

    # 5############################################################
    # print("#" * 10, "5")
    # sol_gp_minimize = gp_minimize(
    #     func=self.residualFuncConstraintWrapper,
    #     dimensions=boundsTuplesFloat,
    #     x0=self.xParameters,
    #     random_state=1,
    #     verbose=True,
    #     n_calls=100,
    #     n_jobs=1,
    # )

    # sol_gp_minimize_1 = gp_minimize(
    #     func=self.residualFuncConstraintWrapper,
    #     dimensions=boundsTuplesFloat,
    #     x0=self.xParameters,
    #     base_estimator="GBRT",
    #     random_state=1,
    #     verbose=True,
    #     n_calls=100,
    #     n_jobs=1,
    # )

    # sol_gp_minimize_2 = gp_minimize(
    #     func=self.residualFuncConstraintWrapper,
    #     dimensions=boundsTuplesFloat,
    #     x0=self.xParameters,
    #     base_estimator="RF",
    #     random_state=1,
    #     verbose=True,
    #     n_calls=100,
    #     n_jobs=1,
    # )

    # sol_gp_minimize_3 = gp_minimize(
    #     func=self.residualFuncConstraintWrapper,
    #     dimensions=boundsTuplesFloat,
    #     x0=self.xParameters,
    #     base_estimator="ET",
    #     random_state=1,
    #     verbose=True,
    #     n_calls=100,
    #     n_jobs=1,
    # )

    # poolResults.append(
    #     optimizerPool.apply_async(
    #         gp_minimize,
    #         args=(self.residualFuncWrapper, boundsTuplesFloat,),
    #         kwds={"verbose": True, "n_jobs": 1, "x0": self.xParameters},
    #     )
    # )
    #############################################################

    # optimizerPool.close()
    # optimizerPool.join()

    # optMin = np.inf
    # optX = self.xParameters
    # for poolResult in [
    #     # sol_basinhopping,
    #     sol_basinhopping,
    # ]:  # poolResults:
    #     optResult = poolResult  # .get()
    #     print("-" * 10)
    #     print(optResult.x, optResult.fun)
    #     if optResult.fun < optMin:
    #         optMin = optResult.fun
    #         optX = optResult.x

    # print("*" * 10)
    # print(optX, optMin)

    # self.__saveResults__(optX)

    # res_SLSQP = minimize(
    #     residualFunc,
    #     self.xParameters,
    #     bounds=boundsTuples,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.objectiveValues,
    #         self.numberOfPartPairs,
    #     ),
    #     method="SLSQP",
    #     constraints=sumConstraint,
    #     options={"disp": True, "eps": 0.1},
    # )
    # print(
    #     np.around(res_SLSQP.x, 3), res_SLSQP.fun,
    # )

    # boundsListsCombined = (
    #     [1e-2] * 13,
    #     [1.0] * 4 + [1e2] * 7 + [0.8, 0.8],
    # )
    # boundsTuplesCombined = list(zip(boundsListsCombined[0], boundsListsCombined[1]))

    # testJac = jacobianFunc(
    #     self.xParameters,
    #     self.GS_BodyPairclass_list,
    #     self.GS_Objective,
    #     self.numberOfPartPairs,
    # )

    # testHes = hessianFunc(
    #     self.xParameters,
    #     self.GS_BodyPairclass_list,
    #     self.GS_Objective,
    #     self.numberOfPartPairs,
    # )

    # Sol1 = differential_evolution(
    #     residualFunc,
    #     bounds=boundsTuplesFloat,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     callback=self.optCallback,
    #     constraints=sumConstraintClass,
    #     polish=True,
    #     disp=True,
    #     workers=-1,
    # )
    # print(
    #     np.around(Sol1.x, 3), Sol1.fun,
    # )

    # fig = plt.figure()
    # nrOfPoints = 1000
    # grid = (3, 4)

    # # pr = cProfile.Profile()
    # # pr.enable()
    # for plot_x in range(4, 11):
    #     startParams = [1] * 11
    #     # x_list = np.linspace(
    #     #     boundsTuplesFloat[plot_x][0], boundsTuplesFloat[plot_x][1], nrOfPoints,
    #     # )
    #     if plot_x < 4:
    #         x_list = np.linspace(
    #             boundsTuplesFloat[plot_x][0],
    #             boundsTuplesFloat[plot_x][1],
    #             nrOfPoints,
    #         )

    #     else:
    #         x_list = np.linspace(boundsTuplesFloat[plot_x][0], 100, nrOfPoints,)
    #         # x_list = np.logspace(
    #         #     np.log10(boundsTuplesFloat[plot_x][0]),
    #         #     np.log10(boundsTuplesFloat[plot_x][1]),
    #         #     nrOfPoints,
    #         # )

    #     y = np.empty(nrOfPoints)
    #     dy = np.empty(nrOfPoints)
    #     d2y = np.empty(nrOfPoints)
    #     for i, x in enumerate(x_list):
    #         startParams[plot_x] = x
    #         # y[i] = residualFunc(
    #         #     startParams,
    #         #     self.GS_BodyPairclass_list,
    #         #     self.GS_Objective,
    #         #     self.numberOfPartPairs,
    #         # )
    #         dy[i] = jacobianFunc(
    #             startParams,
    #             self.GS_BodyPairclass_list,
    #             self.GS_Objective,
    #             self.numberOfPartPairs,
    #         )[plot_x]
    #         d2y[i] = hessianFunc(
    #             startParams,
    #             self.GS_BodyPairclass_list,
    #             self.GS_Objective,
    #             self.numberOfPartPairs,
    #         )[plot_x][plot_x]

    #     ax = plt.subplot(grid[0], grid[1], plot_x + 1)

    #     ax.plot(
    #         x_list, dy, color="black",
    #     )

    #     ax2 = ax.twinx()

    #     ax2.plot(x_list, d2y, color="red")

    # if plot_x > 3:
    #     ax.set_xscale("log")
    #     ax2.set_xscale("log")
    # pr.disable()
    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # profFile = open("CodeCheckJacobean.txt", "w")
    # print(s.getvalue())
    # profFile.write(s.getvalue())
    # profFile.close()
    # fig.tight_layout()
    # plt.show()

    # res_SLSQP2 = minimize(
    #     residualFunc,
    #     [
    #         0.25,
    #         0.25,
    #         0.25,
    #         0.25,
    #         1000000,
    #         1000000,
    #         1000000,
    #         1000000,
    #         1000000,
    #         1000000,
    #         1000000,
    #     ],
    #     bounds=boundsTuples,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     method="SLSQP",
    #     constraints=sumConstraint,
    #     options={"disp": True},
    # )
    # print(
    #     np.around(res_SLSQP2.x, 3), res_SLSQP2.fun,
    # )

    # Sol2 = shgo(
    #     self.residualFunc,
    #     boundsTuplesFloat,
    #     constraints=sumConstraint,
    #     options={"disp": True},
    #     sampling_method="sobol",
    #     # options={"maxfevint": 10, "maxiter": 10, "maxevint": 10, "disp": False},
    # )
    # print(
    #     np.around(Sol2.x, 3), Sol2.fun,
    # )

    # Sol5 = gp_minimize(
    #     func=self.residualFuncConstraint,
    #     dimensions=boundsTuplesFloat,
    #     random_state=1,
    #     verbose=False,
    #     n_random_starts=100,
    #     n_calls=1000,
    #     n_jobs=1,
    # )
    # print(
    #     np.around(Sol5.x, 3), Sol5.fun,
    # )

    # Sol6 = dual_annealing(func=self.residualFunc, bounds=boundsTuplesFloat,)
    # print(
    #     np.around(Sol6.x, 3), Sol6.fun,
    # )

    # Sol7 = brute(
    #     func=residualFuncConstraint,
    #     ranges=boundsTuplesFloat,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     Ns=3,
    #     full_output=True,
    #     disp=True,
    #     workers=-1,
    # )
    # print(
    #     np.around(Sol7[0], 3), Sol7[1],
    # )

    # res_SLSQP2 = minimize(
    #     residualFunc,
    #     Sol5.x,
    #     bounds=boundsTuples,
    #     args=(
    #         self.GS_BodyPairclass_list,
    #         self.GS_Objective,
    #         self.numberOfPartPairs,
    #     ),
    #     method="SLSQP",
    #     constraints=sumConstraint,
    #     options={"disp": True},
    # )
    # print(
    #     np.around(res_SLSQP2.x, 3), res_SLSQP2.fun,
    # )

    # fig, ax = plt.subplots()
    # ax = plot_objective(Sol5, n_points=10)
    # plt.show()

    # fig2, ax2 = plt.subplots()
    # ax2 = plot_convergence(Sol5)
    # plt.show()

    # self.__saveResults__(Sol5.x)

    def __saveResults__(self, x):
        self.xSolution = x
        self.finished.emit(x)
