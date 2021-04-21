import itertools
import math
import operator
import os
import shutil
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.spatial.transform import Rotation as RotationClass

from Shared.Preferences import calcPrefClass


class BoundingBox:
    def __init__(self):

        self.boxOrigin = None
        self.boxEnd = None

        self.box_x_dir = None
        self.box_y_dir = None
        self.box_z_dir = None

        self.delta_x = None
        self.delta_y = None
        self.delta_z = None

    def setData(self, boxData: Tuple[List[float], List[float], List[float]]):
        boxDeltas = boxData[0]
        boxCoords = boxData[1]
        boxDirs = boxData[2]

        self.boxOrigin = np.array(boxCoords[0:3])
        self.boxEnd = np.array(boxCoords[3:6])

        self.box_x_dir = np.array(boxDirs[0:3])
        self.box_y_dir = np.array(boxDirs[3:6])
        self.box_z_dir = np.array(boxDirs[6:9])

        self.delta_x = boxDeltas[0]
        self.delta_y = boxDeltas[1]
        self.delta_z = boxDeltas[2]

    def getBoundingBox(self):
        return self


class TransformationClass:
    def __init__(self, NumVotes: int = 1, round_pos: float = 1, round_dir: float = 3):
        self.numVotes = NumVotes
        self.residual = 0

        self.round_pos = round_pos
        self.round_dir = round_dir

        self.__resetAttributes__()

    def __resetAttributes__(self):
        self.Rcalc = None
        self.tcalc = None
        self.axis_Rcalc = None
        self.tracecalc = None
        self.anglecalc = None
        self.qcalc = None

        self.poseCalc = None  # np.zeros((4, 4))
        self.rotCalcClass = None

    def setPose(self, pose):
        RPomp, tPomp = TransformationFunctions.poseToRT(pose)
        self.setRT(RPomp, tPomp)

    def setRT(self, _R: np.ndarray, _t: np.ndarray):
        self.__resetAttributes__()
        self.rotCalcClass = RotationClass.from_matrix(_R)
        self.tcalc = np.around(_t, self.round_pos)

    def setQuatT(self, NewQ, NewT):
        self.__resetAttributes__()
        self.tcalc = np.around(NewT, self.round_pos)
        self.rotCalcClass = RotationClass.from_quat(NewQ)

    def setT(self, _t: np.ndarray):
        self.tcalc = np.around(_t, self.round_pos).reshape(3)
        self.poseCalc = TransformationFunctions.rtToPose(self.R, self.t)

    def poseComposition(self, poseClassNew):
        # columnwise rotation matrix are combined with pre-multiplication.
        # See https://en.wikipedia.org/wiki/Rotation_matrix#Ambiguities
        poseComp = poseClassNew.pose.dot(self.pose)
        self.setPose(poseComp)

    def setSimilarity(self, geometric_similarity: float):
        self.geometric_similarity = geometric_similarity

    @property
    def status(self):
        if not self.rotCalcClass is None:
            return True
        else:
            return False

    @property
    def R(self):
        if self.Rcalc is None and self.status == True:
            self.Rcalc = np.around(self.rotCalcClass.as_matrix(), self.round_dir)
        if self.status == True:
            return self.Rcalc
        else:
            return None

    @property
    def t(self):
        if not self.tcalc is None:
            return self.tcalc
        return None

    @property
    def angle(self):
        if self.anglecalc is None and self.status == True:
            self.anglecalc = np.around(
                np.linalg.norm(self.rotCalcClass.as_rotvec()), self.round_pos
            )
        if self.status == True:
            return self.anglecalc
        else:
            None

    @property
    def axis_R(self):
        if self.axis_Rcalc is None and self.status == True:
            axis_Rcalc = np.around(self.rotCalcClass.as_rotvec(), self.round_dir)
            for R_pos in range(3):
                if abs(axis_Rcalc[R_pos]) >= 0.1:
                    if axis_Rcalc[R_pos] < 0:
                        axis_Rcalc *= -1
                    break
            self.axis_Rcalc = axis_Rcalc
        if self.status == True:
            return self.axis_Rcalc
        else:
            return None

    @property
    def pose(self) -> np.ndarray:
        if self.poseCalc is None and self.status == True:
            self.poseCalc = TransformationFunctions.rtToPose(self.R, self.t)
        return self.poseCalc

    @property
    def q(self):
        if self.qcalc is None and self.status == True:
            qcalc = np.around(self.rotCalcClass.as_quat(), self.round_dir)
            # check qcalc sign of first non zero for qw, qx, qy, qz
            for q_pos in [3, 0, 1, 2]:
                if abs(qcalc[q_pos]) >= 0.1:
                    if qcalc[q_pos] < 0:
                        qcalc *= -1
                    break
            self.qcalc = qcalc
        return self.qcalc

    @property
    def poseClass(self):
        return self


class TransformationClassCluster:
    def __init__(self, _pose=None, hashKey=None, calcPrefs: calcPrefClass = None):
        self.numVotes = 0
        self.id = 0
        self.hashKey = hashKey
        self.qAvg = np.zeros((4,))
        self.tAvg = np.zeros((3,))
        self.poseCount = 0
        self.poseClasscalc = TransformationClass(
            1, calcPrefs.digits_round_pos, calcPrefs.digits_round_dir
        )
        self.calcPrefs = calcPrefs

        self.poseList = []
        if _pose != None:
            self.addPose(_pose)

    def addPose(self, _pose):
        self.poseList.append(_pose)
        self.numVotes += _pose.numVotes
        self.poseCount += 1
        self.qAvg += _pose.numVotes * _pose.q
        self.tAvg += _pose.numVotes * _pose.t

    def setPoseICP(self, poseICP):
        self.poseClasscalc.poseComposition(poseICP)
        self.qAvg = self.poseClasscalc.q * self.numVotes
        self.tAvg = self.poseClasscalc.t * self.numVotes
        self.hashKey = PointCloudFunctions.poseHash(self.poseClass)

    @property
    def q(self):
        return np.around(self.qAvg / self.numVotes, self.calcPrefs.digits_round_dir)

    @property
    def t(self):
        return np.around(self.tAvg / self.numVotes, self.calcPrefs.digits_round_pos)

    @property
    def poseClass(self):
        if self.poseClasscalc.q is None:
            self.poseClasscalc.setQuatT(self.q, self.t)
        return self.poseClasscalc


class TransformationFunctions:
    @staticmethod
    def rtToPose(_R, _t):
        P = np.hstack((_R, _t.reshape((3, 1))))
        P_v = np.zeros((1, 4))
        P_v[0][3] = 1
        Pose = np.vstack((P, P_v))
        return Pose

    @staticmethod
    def poseToRT(
        _Pose,
    ) -> Tuple[np.ndarray, np.ndarray]:
        R = TransformationFunctions.poseToR(_Pose)
        t = _Pose[:3, 3:4].reshape(3)
        return R, t

    @staticmethod
    def poseToR(_Pose):
        R = _Pose[:3, :3]
        return R

    @staticmethod
    def transformPCPose(pc, PoseClass: TransformationClass) -> np.ndarray:
        """
        data pc as array: shape = [i, 3] or [i, 6] or [i, 9]
        i = number of points
        output = np.ndarray(i,3 or 6 or 9)
        """
        if PoseClass.status == True:
            if pc.shape == (3,):
                pc = pc.reshape(1, 3)
            elif pc.shape == (6,):
                pc = pc.reshape(1, 6)
            elif pc.shape == (9,):
                pc = pc.reshape(1, 9)

            if pc.shape[1] == 3:
                return TransformationFunctions.transformPCPose_worker_RotTrans(
                    pc, PoseClass
                )
            elif pc.shape[1] == 6:
                return np.column_stack(
                    (
                        TransformationFunctions.transformPCPose_worker_RotTrans(
                            pc[:, 0:3], PoseClass
                        ),
                        TransformationFunctions.transformPCPose_worker_Rot(
                            pc[:, 3:6], PoseClass
                        ),
                    )
                )
            elif pc.shape[1] == 9:
                return np.column_stack(
                    (
                        TransformationFunctions.transformPCPose_worker_RotTrans(
                            pc[:, 0:3], PoseClass
                        ),
                        TransformationFunctions.transformPCPose_worker_Rot(
                            pc[:, 3:6], PoseClass
                        ),
                        TransformationFunctions.transformPCPose_worker_RotTrans(
                            pc[:, 6:9], PoseClass
                        ),
                    )
                )

    @staticmethod
    def transformPCPose_worker_RotTrans(pc, PoseClass: TransformationClass):
        """
        data pc as array: shape = [i, 3] i = number of points
        output = np.ndarray(i,3)
        """

        R = PoseClass.R
        t = PoseClass.t

        check_det = math.fabs(np.linalg.det(R))
        if round(abs(check_det), 1) != 1.0:
            print("No Red-Matrix")
            R = np.eye(3)

        pc_R = R.dot(pc.T).T
        return pc_R + t.T

    @staticmethod
    def transformPCPose_worker_Rot(pc, PoseClass: TransformationClass):
        """
        data pc as array: shape = [i, 3] i = number of points
        output = np.ndarray(i,3)
        """

        R = PoseClass.R

        check_det = math.fabs(np.linalg.det(R))
        if round(abs(check_det), 1) != 1.0:
            print("No Red-Matrix")
            R = np.eye(3)

        return R.dot(pc.T).T

    @staticmethod
    def meanGridDelta(
        _pointCloud_a: np.ndarray,
        _pointCloud_b: np.ndarray,
        _gridLocations_a: np.ndarray,
        _gridLocations_b: np.ndarray,
    ):
        def GridDelta(gridLocations, pointCloud):
            gridStr = np.char.decode(gridLocations, "utf-8")
            gridDict = {}
            deltasList = [
                [0, np.array([1, 0, 0])],
                [0, np.array([0, 1, 0])],
                [0, np.array([0, 0, 1])],
            ]

            gridTuple_0 = (0, 0, 0)
            for i, gridPoint in enumerate(gridStr):
                gridTuple = eval(gridPoint)
                gridDict[gridTuple] = pointCloud[i]
                if i > 0:
                    gridDeltas = [
                        gridTuple[0] - gridTuple_0[0],
                        gridTuple[1] - gridTuple_0[1],
                        gridTuple[2] - gridTuple_0[2],
                    ]
                    for ide, delta in enumerate(deltasList):
                        if gridDeltas[ide] == 0 and not delta[0] is None:
                            delta[0] = 0
                        elif not delta[0] is None:
                            delta[0] = None

                gridTuple_0 = gridTuple

            dirInts = [-1, 1]
            finished = False
            for gridPoint in gridDict.keys():
                gP_array = np.array(gridPoint)
                gP_point = gridDict[gridPoint]
                for step in range(1, 100):
                    trueCount = 0
                    for deltaTup in deltasList:
                        if deltaTup[0] is None:
                            for dirInt in dirInts:
                                nextPointPlus = tuple(
                                    gP_array + dirInt * step * deltaTup[1]
                                )
                                if nextPointPlus in gridDict:
                                    deltaTup[0] = (
                                        np.linalg.norm(
                                            gP_point - gridDict[nextPointPlus]
                                        )
                                        / step
                                    )
                                    break
                        else:
                            trueCount += 1
                    if trueCount == 3:
                        finished = True
                        break
                if finished == True:
                    break

            deltaMean = 0
            for delta in deltasList:
                deltaMean += delta[0]
            return deltaMean / 3

        PCDeltaA = GridDelta(_gridLocations_a, _pointCloud_a)
        PCDeltaB = GridDelta(_gridLocations_b, _pointCloud_b)

        return (PCDeltaA + PCDeltaB) * 4 / 2


class BoxTransformationClass(TransformationClass, BoundingBox):
    def __init__(self, calcPrefs: calcPrefClass):
        self.calcPrefs = calcPrefs
        TransformationClass.__init__(
            self, 1, self.calcPrefs.digits_round_pos, self.calcPrefs.digits_round_dir
        )
        BoundingBox.__init__(self)

    def setBox(
        self,
        origin: np.ndarray,
        end: np.ndarray,
        _R: np.ndarray,
        _t: np.ndarray,
        delta_x: float,
        delta_y: float,
        delta_z: float,
    ):

        self.setRT(_R, _t)

        self.boxOrigin = np.around(
            TransformationFunctions.transformPCPose(origin, self).reshape(3),
            self.calcPrefs.digits_round_pos,
        )
        self.boxEnd = np.around(
            TransformationFunctions.transformPCPose(end, self).reshape(3),
            self.calcPrefs.digits_round_pos,
        )

        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z

        x_axis = self.R[0].reshape(3)
        y_axis = self.R[1].reshape(3)
        z_axis = self.R[2].reshape(3)

        self.box_x_dir = np.around(
            TransformationFunctions.transformPCPose_worker_Rot(x_axis, self).reshape(3),
            self.calcPrefs.digits_round_dir,
        )
        self.box_y_dir = np.around(
            TransformationFunctions.transformPCPose_worker_Rot(y_axis, self).reshape(3),
            self.calcPrefs.digits_round_dir,
        )
        self.box_z_dir = np.around(
            TransformationFunctions.transformPCPose_worker_Rot(z_axis, self).reshape(3),
            self.calcPrefs.digits_round_dir,
        )

    def getTransformationClassCluster(self) -> TransformationClassCluster:
        poseHash = PointCloudFunctions.poseHash(self.poseClass)
        return TransformationClassCluster(self.poseClass, poseHash, self.calcPrefs)


class BoxTransformationCloudData:
    """
    builds origin, end point and diameter of the minimum bounding box
    and calculates transformations (saved as box poses) from the 8 corners of the box to the absolute coordinate system
    """

    def __init__(self, boxData: BoundingBox, calcPrefs: calcPrefClass):
        self.boxPoses = None
        self.boxData = boxData
        self.calcPrefs = calcPrefs
        self.poseCalcMinBox()

    def poseCalcMinBox(self):

        # 8 corner points of box as possible origins

        box_XO = self.boxData.boxOrigin + self.boxData.box_x_dir * self.boxData.delta_x
        box_YO = self.boxData.boxOrigin + self.boxData.box_y_dir * self.boxData.delta_y
        box_XYO = box_YO + self.boxData.box_x_dir * self.boxData.delta_x

        box_Z = self.boxData.boxOrigin + self.boxData.box_z_dir * self.boxData.delta_z
        box_XZ = box_Z + self.boxData.box_x_dir * self.boxData.delta_x
        box_YZ = box_Z + self.boxData.box_y_dir * self.boxData.delta_y

        # point triples for origins
        points_origin = np.vstack(
            (
                self.boxData.boxOrigin,
                self.boxData.boxOrigin + self.boxData.box_x_dir,
                self.boxData.boxOrigin + self.boxData.box_y_dir,
            )
        )

        points_End = np.vstack(
            (
                self.boxData.boxEnd,
                self.boxData.boxEnd - self.boxData.box_y_dir,
                self.boxData.boxEnd - self.boxData.box_x_dir,
            )
        )

        points_XO = np.vstack(
            (box_XO, box_XO + self.boxData.box_y_dir, box_XO - self.boxData.box_x_dir)
        )

        points_YO = np.vstack(
            (box_YO, box_YO - self.boxData.box_y_dir, box_YO + self.boxData.box_x_dir)
        )

        points_XYO = np.vstack(
            (
                box_XYO,
                box_XYO - self.boxData.box_x_dir,
                box_XYO - self.boxData.box_y_dir,
            )
        )

        points_Z = np.vstack(
            (box_Z, box_Z + self.boxData.box_y_dir, box_Z + self.boxData.box_x_dir)
        )

        points_XZ = np.vstack(
            (box_XZ, box_XZ + self.boxData.box_x_dir, box_XZ - self.boxData.box_y_dir)
        )

        points_YZ = np.vstack(
            (box_YZ, box_YZ - self.boxData.box_x_dir, box_YZ + self.boxData.box_y_dir)
        )

        pointAbsCoordSys = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        self.boxPoses = []  # type: List[BoxTransformationClass]
        self.poseClusters = []
        for pointTriple in [
            points_origin,
            points_XO,
            points_YO,
            points_XYO,
            points_Z,
            points_XZ,
            points_YZ,
            points_End,
        ]:

            R_i, t_i = PointCloudFunctions.rigitMotion(
                pointTriple, pointAbsCoordSys, 0.0
            )
            boxPose_i = BoxTransformationClass(self.calcPrefs)
            boxPose_i.setBox(
                self.boxData.boxOrigin,
                self.boxData.boxEnd,
                R_i,
                t_i,
                self.boxData.delta_x,
                self.boxData.delta_y,
                self.boxData.delta_z,
            )
            self.boxPoses.append(boxPose_i)
            self.poseClusters.append(boxPose_i.getTransformationClassCluster())

    def calcTransformationPose(
        self, data: np.ndarray, pose: TransformationClass
    ) -> np.ndarray:
        """
        data as array: shape = [i, 3] or [i, 6] or [i, 9]
        """
        return TransformationFunctions.transformPCPose(data, pose)


class PointCloudFunctions:
    @staticmethod
    def computeBboxStd(_data=np.array):
        pos_data = _data[:, :3]
        num = pos_data.shape[0]
        xRange = [0, 0]
        yRange = [0, 0]
        zRange = [0, 0]
        xRange[0] = np.min(pos_data[:, 0])
        xRange[1] = np.max(pos_data[:, 0])
        yRange[0] = np.min(pos_data[:, 1])
        yRange[1] = np.max(pos_data[:, 1])
        zRange[0] = np.min(pos_data[:, 2])
        zRange[1] = np.max(pos_data[:, 2])

        return xRange, yRange, zRange

    @staticmethod
    def samplePCByQuantization(
        _data: np.ndarray, BoundingBox: BoundingBox, calcPrefs: calcPrefClass
    ) -> np.ndarray:

        objectiveSampling = calcPrefs.samplingpoints_detail_roughcalc
        objective_in = min(objectiveSampling, float(len(_data)))

        xr = BoundingBox.delta_x
        yr = BoundingBox.delta_y
        zr = BoundingBox.delta_z

        pro_range = xr * yr * zr
        xr_p = xr / (pro_range ** (1.0 / 3.0))
        yr_p = yr / (pro_range ** (1.0 / 3.0))
        zr_p = zr / (pro_range ** (1.0 / 3.0))

        sample_objective = float(objective_in)

        # convergence criteria:
        objective_tol = int(objective_in * 0.05)
        # ax**2+b=f(x) con_ult_min -> 1, f(g)=1, f(b)=con_ult_min
        con_max_status = np.inf
        con_min_status = 0.0
        con_none = 0
        con_threshold = 20
        delta_div_objective_old = np.inf
        samples_objective_reached = False

        while samples_objective_reached == False:

            dim_x = int(round(sample_objective ** (1.0 / 3.0) * xr_p, 0))
            dim_y = int(round(sample_objective ** (1.0 / 3.0) * yr_p, 0))
            dim_z = int(round(sample_objective ** (1.0 / 3.0) * zr_p, 0))

            map_ = {}
            for i, pointData in enumerate(_data):

                point = np.around(pointData[:3], 0)
                vectorPoint = point - np.around(
                    BoundingBox.boxOrigin
                )  # type: np.ndarray

                projectionOnBoxX = round(np.dot(vectorPoint, BoundingBox.box_x_dir), 0)
                projectionOnBoxY = round(np.dot(vectorPoint, BoundingBox.box_y_dir), 0)
                projectionOnBoxZ = round(np.dot(vectorPoint, BoundingBox.box_z_dir), 0)

                xCell = int(float(dim_x) * projectionOnBoxX / xr)
                yCell = int(float(dim_y) * projectionOnBoxY / yr)
                zCell = int(float(dim_z) * projectionOnBoxZ / zr)

                if not (xCell, yCell, zCell) in map_:
                    map_[(xCell, yCell, zCell)] = [i]
                else:
                    map_[(xCell, yCell, zCell)].append(i)

            numPoints = len(map_)
            if int(abs(numPoints - objective_in)) <= objective_tol:
                samples_objective_reached = True
            else:

                # print("Num", numPoints)
                div_objective = float(objective_in) / float(numPoints)
                delta_div_objective = abs(float(1.0) - float(div_objective))
                if delta_div_objective > delta_div_objective_old:
                    delta_div_objective = delta_div_objective_old * 0.9
                # print("Delta_ber", delta_div_objective)
                if div_objective > 1.0:
                    sample_objective = int(
                        round(sample_objective * (1.0 + delta_div_objective))
                    )
                    if numPoints > con_min_status:
                        con_min_status = numPoints
                        map_save_min = map_
                        con_none = 0
                    else:
                        con_none += 1
                else:
                    sample_objective = int(
                        round(sample_objective * (1.0 - delta_div_objective))
                    )
                    if numPoints < con_max_status:
                        con_max_status = numPoints
                        map_save_max = map_
                        con_none = 0
                    else:
                        con_none += 1

                if con_none >= con_threshold or delta_div_objective < 0.05:
                    delta_max = abs(con_max_status - objective_in)
                    delta_min = abs(con_min_status - objective_in)
                    if delta_max <= delta_min:
                        map_ = map_save_max
                        numPoints = con_max_status
                    else:
                        map_ = map_save_min
                        numPoints = con_min_status
                    samples_objective_reached = True

                delta_div_objective_old = delta_div_objective

        pcSampled = np.empty((numPoints, _data.shape[1]), dtype=float)
        c = 0
        for map_i in map_:
            px = py = pz = 0.0
            nx = ny = nz = 0.0

            map_zeile = map_[map_i]
            cn = len(map_zeile)
            for j in range(cn):
                ptInd = map_zeile[j]
                point = _data[ptInd]

                px += point[0]
                py += point[1]
                pz += point[2]
                nx += point[3]
                ny += point[4]
                nz += point[5]

            px /= cn
            py /= cn
            pz /= cn
            nx /= cn
            ny /= cn
            nz /= cn

            pcData = pcSampled[c]
            pcData[0] = round(float(px), calcPrefs.digits_round_pos)
            pcData[1] = round(float(py), calcPrefs.digits_round_pos)
            pcData[2] = round(float(pz), calcPrefs.digits_round_pos)

            norm = math.sqrt(nx * nx + ny * ny + nz * nz)

            if norm > 0.0:
                pcData[3] = round(float(nx / norm), calcPrefs.digits_round_dir)
                pcData[4] = round(float(ny / norm), calcPrefs.digits_round_dir)
                pcData[5] = round(float(nz / norm), calcPrefs.digits_round_dir)

            c += 1

        return pcSampled

    @staticmethod
    def TAngle3Normalized(_v0, v_1):
        cosang = np.dot(_v0, v_1)
        sinang = np.linalg.norm(PointCloudFunctions.crossProduct_fast(_v0, v_1))
        return np.arctan2(sinang, cosang)

    @staticmethod
    def hashPPF(_f, _angle_step_radians, _distanceStep) -> Tuple[float]:
        angles = _f["angles"]
        lenghts = _f["lenghts"]
        key = []
        for a in angles:
            key.append(int(float(a) / _angle_step_radians))
        for l in lenghts:
            key.append(int(float(l) / _distanceStep))
            # key.append(round(float(l) / _distanceStep, 1))
        # hashvalue=hash(tuple(map(float,key)))
        # return hashvalue,tuple(key)

        return tuple(key)

    @staticmethod
    def crossProduct_fast(v_1, v_2):
        eijk = np.zeros((3, 3, 3))
        eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
        eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1
        return np.einsum(
            "ijk,uj,vk->uvi", eijk, v_1.reshape(1, 3), v_2.reshape(1, 3)
        ).reshape(3)

    @staticmethod
    def rigitMotion(P_is, Q_is, sampling_distanceHash):
        """Rigit motion from p to q
        Input:  P_is, Q_is: np.array([
                                    [point1_x, point1_y, point1_z]
                                    [point2_x, point2_y, point2_z]
                                    [point3_x, point3_y, point3_z]])
        Calculation:    If distances P_is equal to Q_is -> geometric calculation, least squares otherwise (see Arun, K. 1987 Least-squares fitting of two 3-D point sets)
        """

        # check is distances of points are equal
        # equalDist = False
        equalDist = True
        if sampling_distanceHash > 1:  # for small sampling steps d_i always equal
            equalDist = False
            for pointPair in itertools.combinations([0, 1, 2], 2):
                dist_p = np.linalg.norm(P_is[pointPair[0]] - P_is[pointPair[1]])
                dist_q = np.linalg.norm(Q_is[pointPair[0]] - Q_is[pointPair[1]])
                dev_pq = abs(dist_p - dist_q)
                if dev_pq > 1.0:
                    equalDist = False
                    break
                else:
                    equalDist = True

        if equalDist == True:
            # coordinate transformation

            # calc 1st & 2nd axis for p coord sys
            P_23 = P_is[1:] - P_is[0]
            # calc 1st & 2nd axis for q coord sys
            Q_23 = Q_is[1:] - Q_is[0]

            # define 3rd axis p
            # P_4 = np.cross(*P_23)
            P_4 = PointCloudFunctions.crossProduct_fast(P_23[0], P_23[1])
            # define 3rd axis q
            # Q_4 = np.cross(*Q_23)
            Q_4 = PointCloudFunctions.crossProduct_fast(Q_23[0], Q_23[1])

            # construc coord sys p
            P_m = np.column_stack((P_23.T, P_4))
            # construc coord sys q
            Q_m = np.column_stack((Q_23.T, Q_4))

            # calculate rotation matrix
            # P_m_inv = np.linalg.inv(P_m)
            P_m_inv = np.linalg.pinv(P_m)  # pseudo-inverse with svd
            R_calc = np.dot(Q_m, P_m_inv)

            # calculate translation vector
            t_calc = Q_is[0] - np.dot(R_calc, P_is[0])

        else:
            # least square aproximation of R and t
            P_is_T = P_is.T
            Q_is_T = Q_is.T

            p_centroid = np.mean(P_is_T, axis=1)
            q_centroid = np.mean(Q_is_T, axis=1)

            pDeltaCentroid = P_is_T - p_centroid.reshape(3, 1)
            qDeltaCentroid = Q_is_T - q_centroid.reshape(3, 1)

            dimension = len(P_is_T)
            H = np.zeros((3, 3))
            for i in range(dimension):
                pcqcT = (
                    pDeltaCentroid[:, i]
                    .reshape(3, 1)
                    .dot(qDeltaCentroid[:, i].reshape(1, 3))
                )
                H += pcqcT

            U, D, V = np.linalg.svd(H)
            V = V.T
            X = V.dot(U.T)
            detX = np.linalg.det(X)
            if round(detX, 0) == -1:
                Vs = np.column_stack((V[:, 0], V[:, 1], -V[:, 2]))
                X = Vs.dot(U.T)

            R_calc = X
            t_calc = q_centroid.reshape(3, 1) - X.dot(p_centroid.reshape(3, 1))
            t_calc = t_calc.reshape(3)

        ## points Ps must be columnwise -> R.dot(Ps).T + T with Ps = [P1(3,1), P2(3,1), ..]
        return R_calc, t_calc

    @staticmethod
    def poseHash(pose: TransformationClass):
        """Hash for pose definition.
        Replaces:
            d_t = pose.t - pose_new.t
            d_norm = np.linalg.norm(d_t)
            d_axis = pose.axis_R - pose_new.axis_R
            d_angle = math.fabs(pose.angle - pose_new.angle)"""

        sample_translation = 1
        sample_axes = 10 * np.pi / 180
        sample_angle = 10 * np.pi / 180

        norm_t = np.linalg.norm(pose.t)
        if norm_t == 0:
            value_translation = 0
            t_angle_x_sample = 0
            t_angle_y_sample = 0
            t_angle_z_sample = 0
        else:
            t_normed = pose.t / norm_t

            # length translation
            value_translation = int(round(norm_t / sample_translation, 0))

            # direction translation
            t_angle_x = PointCloudFunctions.TAngle3Normalized(
                t_normed, np.array([1, 0, 0])
            )
            t_angle_x_sample = int(round(t_angle_x / sample_axes, 0))
            t_angle_y = PointCloudFunctions.TAngle3Normalized(
                t_normed, np.array([0, 1, 0])
            )
            t_angle_y_sample = int(round(t_angle_y / sample_axes, 0))
            t_angle_z = PointCloudFunctions.TAngle3Normalized(
                t_normed, np.array([0, 0, 1])
            )
            t_angle_z_sample = int(round(t_angle_z / sample_axes, 0))

        # eigenvector R = rotation axis R -> direction
        R_angle_x = PointCloudFunctions.TAngle3Normalized(
            pose.axis_R, np.array([1, 0, 0])
        )
        R_angle_x_sample = int(round(R_angle_x / sample_axes, 0))
        R_angle_y = PointCloudFunctions.TAngle3Normalized(
            pose.axis_R, np.array([0, 1, 0])
        )
        R_angle_y_sample = int(round(R_angle_y / sample_axes, 0))
        R_angle_z = PointCloudFunctions.TAngle3Normalized(
            pose.axis_R, np.array([0, 0, 1])
        )
        R_angle_z_sample = int(round(R_angle_z / sample_axes, 0))

        # rotation angle
        value_angle = int(round(abs(pose.angle) / sample_angle, 0))

        return (
            value_translation,
            t_angle_x_sample,
            t_angle_y_sample,
            t_angle_z_sample,
            R_angle_x_sample,
            R_angle_y_sample,
            R_angle_z_sample,
            value_angle,
        )

    @staticmethod
    def _plot_export(Src_Moved, DstPCOrig, _name, pathexport=None, partNamesList=None):
        fig = (
            plt.figure()
        )  ################################## Rahmen nicht im Modul ##########################################################
        ax_0 = fig.add_subplot(121, projection="3d")
        ax_0.scatter(
            Src_Moved[:, 0], Src_Moved[:, 1], Src_Moved[:, 2], c="r", marker="o"
        )
        # ax.quiver(Src_Moved[:,0], Src_Moved[:,1], Src_Moved[:,2],
        #          SrcN_Moved[:,0],SrcN_Moved[:,1],SrcN_Moved[:,2],
        #          length=0.1,colors="r")
        ax_1 = fig.add_subplot(122, projection="3d")
        ax_1.scatter(
            DstPCOrig[:, 0], DstPCOrig[:, 1], DstPCOrig[:, 2], c="b", marker="."
        )
        # ax.quiver(DstPCOrig[:,0], DstPCOrig[:,1], DstPCOrig[:,2],
        #          DstNOrig.T[:,0],DstNOrig.T[:,1],DstNOrig.T[:,2],
        #          length=0.1,colors="b")
        if pathexport == None:
            pathexport = r"X:\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging\Bauteil_Karte\01_Daten-Bauteil"  # D:\Bauteil_Karte\01_Daten-Bauteil"
        if partNamesList == None:
            partNamesList = ["NaN", "NaN"]
        path_export_spez = pathexport + r"/{}vs{}_ICP_export".format(
            partNamesList[0], partNamesList[1]
        )
        if os.path.isdir(path_export_spez) == False:
            os.makedirs(path_export_spez)
        elif _name == "00_Training":
            shutil.rmtree(path_export_spez)
            os.makedirs(path_export_spez)

        plt.savefig(path_export_spez + r"/{}.png".format(_name))
        # plt.show()
        plt.close()
