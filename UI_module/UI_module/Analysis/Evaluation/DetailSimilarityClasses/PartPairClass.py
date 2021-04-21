import copy
import operator
from typing import Dict, List, Tuple

import numexpr as ne
import numpy as np
from sklearn.neighbors import NearestNeighbors

from Analysis.Evaluation.DetailSimilarityClasses.FineTransformation import (
    FineTransformationCalc,
)
from Analysis.Evaluation.DetailSimilarityClasses.TransformationClasses import (
    BoxTransformationClass,
    TransformationClass,
    TransformationClassCluster,
    TransformationFunctions,
)
from Shared.Preferences import calcPrefClass


class GS_PartPairclass(object):
    def __init__(
        self,
        calcPrefs: calcPrefClass,
        partID_a: str,
        partID_b: str,
        cloudPoints_a: np.ndarray,
        cloudPoints_b: np.ndarray,
        curvatures_a: np.ndarray,
        curvatures_b: np.ndarray,
        gridLocations_a: np.ndarray,
        gridLocations_b: np.ndarray,
        distanceRating: bool = False,
    ):
        """cloudData: CloudPoints = np.array(n,6), Curvature = np.array(n,2), GridLocations as strings = np.array(n,)
        transformation: Translations = np.array(3,), Rotations = np.array(3,3)"""

        super().__init__()
        self.calcPrefs = calcPrefs
        self.DistanceStatus = True
        self.distanceRating = distanceRating

        self.ID_a = partID_a
        self.ID_b = partID_b

        self.cloudPoints_a = cloudPoints_a[:, :3]
        self.cloudPoints_b = cloudPoints_b[:, :3]
        self.cloudPoints_b_save = copy.deepcopy(self.cloudPoints_b)
        self.normals_a = cloudPoints_a[:, 3:6]
        self.normals_b = cloudPoints_b[:, 3:6]
        self.normals_b_save = copy.deepcopy(self.normals_b)
        self.surfacePoints_a = cloudPoints_a[:, 6:]
        self.surfacePoints_b = cloudPoints_b[:, 6:]
        self.surfacePoints_b_save = copy.deepcopy(self.surfacePoints_b)
        self.curvatures_a = curvatures_a
        self.curvatures_b = curvatures_b
        self.gridLocations_a = gridLocations_a
        self.gridLocations_b = gridLocations_b

        self.maxDistanceDeviation = TransformationFunctions.meanGridDelta(
            self.cloudPoints_a,
            self.cloudPoints_b,
            self.gridLocations_a,
            self.gridLocations_b,
        )

        self.__initParameters__()
        self.learnBodyAPointCloud()

    def setPosesBodyB(self, poses_b: List[TransformationClassCluster]):
        self.poses_b = poses_b

    def check_poses(
        self,
        _poses,  # can be pose clusters or poses
    ) -> List[TransformationClass]:

        poses_ranked = [0] * len(_poses)
        for i, pose in enumerate(_poses):
            pose_i = pose.poseClass
            if not pose_i is None:
                rating = self.__getRating_pose__(pose_b=pose_i)
                pose.poseClass.setSimilarity(rating)
                poses_ranked[i] = (i, rating, float(pose.numVotes))

        self.poses_ranked_sorted = sorted(
            poses_ranked, key=operator.itemgetter(1, 2), reverse=True
        )
        index_poses = [x[0] for x in self.poses_ranked_sorted]
        final_poses = [
            _poses[ind] for ind in index_poses
        ]  # type: List[TransformationClass]

        return copy.deepcopy(final_poses)

    def __getRating_pose__(self, pose_b: TransformationClass) -> float:
        self.transformation_bodyX(pose_b, body="b")
        self.__findPointPairs__()
        if self.DistanceStatus == False:
            return 0
        if self.distanceRating == False:
            self.__calcGeometricCharacteristics__()
            return self.__calcGeometricSimilarity__()
        else:
            return self.__calcPointCloudDistance__()

    def __getDR__pose(self, pose_b: TransformationClass) -> float:
        """Calculate distance rating for pose b"""
        self.transformation_bodyX(pose_b, body="b")
        self.__findPointPairs__()
        if self.DistanceStatus == False:
            return 0.0
        return self.__calcPointCloudDistance__()

    def outputCADdata(self, body="a"):
        if body == "a":
            cloudPoints = self.cloudPoints_a
            normals = self.normals_a
            surfacePoints = self.surfacePoints_a
            curvatures = self.curvatures_a
            gridLocations = self.gridLocations_a
        else:
            cloudPoints = self.cloudPoints_b
            if "normalsBOld" in self.__dict__:
                normals = self.normalsBOld
            else:
                normals = self.normals_b
            surfacePoints = self.surfacePoints_b
            if "curvaturesBOld" in self.__dict__:
                curvatures = self.curvaturesBOld
            else:
                curvatures = self.curvatures_b
            gridLocations = self.gridLocations_b

        normals = self.__correctNormalsWorker__(
            surfacePoints, cloudPoints, cloudPoints, normals
        )
        curvatures = self.__correctCurvaturesWorker__(curvatures)

        return cloudPoints, surfacePoints, normals, curvatures

    def evaluatePointPairs(self):
        self.__findPointPairs__()
        if self.DistanceStatus == True:
            self.__calcGeometricCharacteristics__()

    def getGS_x(self, x):
        self.__setParameters__(x)
        return self.getGS()

    def getJacobian_X(self, x):
        return self.__calcJacobian__(x)

    def getHessian_X(self, x):
        return self.__calcHessian__(x)

    def getGS(self):
        if self.DistanceStatus == False:
            return 0.0
        return round(
            self.__calcGeometricSimilarity__(), self.calcPrefs.digits_round_similarity
        )

    def __initParameters__(self):
        self.w_dist = self.calcPrefs.weight_point_distance_detail_calc
        self.w_norm = self.calcPrefs.weight_normal_angle_detail_calc
        self.w_curvMin = self.calcPrefs.weight_curv_radius_1_detail_calc
        self.w_curvMax = self.calcPrefs.weight_curv_radius_2_detail_calc

        self.e_d_dist = self.calcPrefs.exponent_d_point_distance_detail_calc
        self.e_d_norm = self.calcPrefs.exponent_d_normal_angle_detail_calc
        self.e_e_norm = self.calcPrefs.exponent_e_normal_angle_detail_calc
        self.e_d_curvMin = self.calcPrefs.exponent_d_curv_radius_min_detail_calc
        self.e_e_curvMin = self.calcPrefs.exponent_e_curv_radius_min_detail_calc
        self.e_d_curvMax = self.calcPrefs.exponent_d_curv_radius_max_detail_calc
        self.e_e_curvMax = self.calcPrefs.exponent_e_curv_radius_max_detail_calc

    def transformation_bodyX(self, pose: TransformationClass, body: str = ""):
        if body == "a":
            self.pose_a = pose
            (
                self.cloudPoints_a,
                self.normals_a,
                self.surfacePoints_a,
            ) = self.__transformCloudData__(
                pose, self.cloudPoints_a, self.normals_a, self.surfacePoints_a
            )
            self.learnBodyAPointCloud()

        if body == "b":
            self.pose_b = pose
            (
                self.cloudPoints_b,
                self.normals_b,
                self.surfacePoints_b,
            ) = self.__transformCloudData__(
                pose,
                self.cloudPoints_b_save,
                self.normals_b_save,
                self.surfacePoints_b_save,
            )

    def __transformCloudData__(
        self,
        pose_x: TransformationClass,
        cloudPoints_x: np.ndarray,
        normals_x: np.ndarray,
        surfacePoints_x: np.ndarray,
    ):
        cloudPoints_x = TransformationFunctions.transformPCPose_worker_RotTrans(
            cloudPoints_x, pose_x
        )
        normals_x = TransformationFunctions.transformPCPose_worker_Rot(
            normals_x, pose_x
        )
        surfacePoints_x = TransformationFunctions.transformPCPose_worker_RotTrans(
            surfacePoints_x, pose_x
        )
        return cloudPoints_x, normals_x, surfacePoints_x

    def learnBodyAPointCloud(self):
        self.kdtreeobj_a = NearestNeighbors(
            n_neighbors=1, algorithm="kd_tree", leaf_size=8
        ).fit(self.cloudPoints_a)

    def findBest_pose_b(self):

        poseClusters_sorted = self.check_poses(self.poses_b)
        finalPose = copy.deepcopy(poseClusters_sorted[0].poseClass)
        finePoseClusters_sorted = self.fineTransformation(poseClusters_sorted[:10])
        ## sometimes rough transformations are better
        if (
            finePoseClusters_sorted[0].poseClass.geometric_similarity
            > finalPose.geometric_similarity
        ):
            finalPose = finePoseClusters_sorted[0].poseClass

        self.transformation_bodyX(finalPose, body="b")

    def fineTransformation(self, poseClusters):
        poseClusters_ = copy.deepcopy(poseClusters)
        fineTransformationClass = FineTransformationCalc(self.calcPrefs)
        finePoseClusters = fineTransformationClass.start(
            self.cloudPoints_a,
            self.cloudPoints_b_save,
            self.normals_a,
            poseClusters_,
        )
        finePoseClusters_sorted = self.check_poses(finePoseClusters)
        return finePoseClusters_sorted

    def fineTransformationsChecked(self, poseClusters):
        finePoseClusters_sorted = self.fineTransformation(poseClusters)
        return self.check_poses(finePoseClusters_sorted)

    def __findPointPairs__(self):
        self.distancesPntsGrid, referenceIndices_a = self.kdtreeobj_a.kneighbors(
            self.cloudPoints_b
        )
        self.numberOfPoints = len(referenceIndices_a)
        referenceIndices_a = referenceIndices_a.reshape(self.numberOfPoints)

        self.nearCloudPoints_a = self.cloudPoints_a[referenceIndices_a]
        self.nearNormals_a = self.normals_a[referenceIndices_a]
        self.nearCurvatures_a = self.curvatures_a[referenceIndices_a]
        self.nearSurfacePoints_a = self.surfacePoints_a[referenceIndices_a]

        self.distancesPntsGrid = self.distancesPntsGrid.reshape(self.numberOfPoints)
        self.distancesPntsGrid[
            self.distancesPntsGrid > self.maxDistanceDeviation
        ] = self.maxDistanceDeviation

        self.distancesPntsSurface = np.linalg.norm(
            self.surfacePoints_b - self.nearSurfacePoints_a, axis=1
        )
        self.distancesPntsSurface[
            self.distancesPntsSurface > self.maxDistanceDeviation
        ] = self.maxDistanceDeviation

        self.distancesPnts = (
            self.distancesPntsSurface
        )  # paper = Grid, calibration= Surface ?

        self.minDistance = min(self.distancesPnts)
        if self.minDistance >= self.maxDistanceDeviation:
            self.DistanceStatus = False
        else:
            self.DistanceStatus = True

    def __calcGeometricCharacteristics__(self):
        self.GC_d_array = (self.maxDistanceDeviation - self.distancesPnts) / (
            self.maxDistanceDeviation - self.minDistance
        )
        # steps for calculating face normal angle difference
        # crT = np.cross(data_a_norms_nearest, data_b_norms, axisa = 1, axisb = 1)
        # nT = np.linalg.norm(crT, axis=1)
        # dT = np.einsum('ij,ij->i',data_a_norms_nearest, data_b_norms) = np.dot(_v0, v_1) row wise for all normals
        # aT = np.arctan2(nT,dT)

        self.__correctNormals__()
        self.GC_n_array = (
            1
            - np.abs(
                np.arctan2(
                    np.linalg.norm(
                        np.cross(self.nearNormals_a, self.normals_b, axisa=1, axisb=1),
                        axis=1,
                    ),
                    np.einsum("ij,ij->i", self.nearNormals_a, self.normals_b),
                )
            )
            * 2
            / np.pi
        )
        self.GC_n_array[self.GC_n_array < 0] = 0

        # radius of curvature cannot be zero -> relative measurement! see Patrikalakis, Maekawa 2010 - Shape Interrogation for Computer Aided
        self.__correctCurvatures__()
        self.GC_cmin_array = 1 - np.abs(
            np.abs(self.nearCurvatures_a[:, 0]) - np.abs(self.curvatures_b[:, 0])
        ) / np.abs(self.nearCurvatures_a[:, 0])

        self.GC_cmax_array = 1 - np.abs(
            np.abs(self.nearCurvatures_a[:, 1]) - np.abs(self.curvatures_b[:, 1])
        ) / np.abs(self.nearCurvatures_a[:, 1])

        self.GC_cmin_array[self.GC_cmin_array < 0] = 0
        self.GC_cmax_array[self.GC_cmax_array < 0] = 0

        self.GC_tuple = [
            self.GC_d_array,
            self.GC_n_array,
            self.GC_cmin_array,
            self.GC_cmax_array,
        ]

        self.GC_ln_tuple = [
            self.ln(self.GC_d_array),
            self.ln(self.GC_n_array),
            self.ln(self.GC_cmin_array),
            self.ln(self.GC_cmax_array),
        ]
        # zeroFloat = 1e-100
        # for array in [
        #     self.GC_d_array,
        #     self.GC_n_array,
        #     self.GC_cmin_array,
        #     self.GC_cmax_array,
        # ]:
        #     arrayCopy = np.copy(array)
        #     arrayCopy[arrayCopy == 0] = zeroFloat
        #     self.GC_tuple.append(arrayCopy)

        # self.GC_tuple = tuple(self.GC_tuple)

    def __correctNormals__(self):

        self.nearNormalsAOld = copy.deepcopy(self.nearNormals_a)
        self.normalsBOld = copy.deepcopy(self.normals_b)
        self.nearNormals_a = self.__correctNormalsWorker__(
            self.nearSurfacePoints_a,
            self.nearCloudPoints_a,
            self.cloudPoints_a,
            self.nearNormals_a,
        )

        self.normals_b = self.__correctNormalsWorker__(
            self.surfacePoints_b,
            self.cloudPoints_b,
            self.cloudPoints_b,
            self.normals_b,
        )

    def __correctNormalsWorker__(
        self,
        SurfacePoints,  # self.nearSurfacePoints_a,
        CloudPoints,  # self.nearCloudPoints_a,
        cloudPointsCentering,  # self.cloudPoints_a,
        normals,  # self.nearNormals_a
    ):

        # meassure angle between centerPoint-boxPoint and boxPoint-surfacePoint vector
        # If angle is larger than 90° -> turn normal vector by 180° with -1 multiplication

        vectorsBoxSurf = SurfacePoints - CloudPoints

        vectorsBoxSurf = vectorsBoxSurf / np.linalg.norm(
            vectorsBoxSurf, axis=1, keepdims=True
        )

        center = np.mean(
            np.vstack((self.cloudPoints_a, self.cloudPoints_b)), axis=0
        )  # np.mean(cloudPointsCentering, axis=0)
        center_Array = np.full((CloudPoints.shape[0], 3), center)

        vectorsBoxCenter = center_Array - CloudPoints

        vectorsBoxCenter = vectorsBoxCenter / np.linalg.norm(
            vectorsBoxCenter, axis=1, keepdims=True
        )
        anglesBoxSurf_BoxCenter = (
            np.arctan2(
                np.linalg.norm(
                    np.cross(
                        vectorsBoxSurf,
                        vectorsBoxCenter,
                        axisa=1,
                        axisb=1,
                    ),
                    axis=1,
                ),
                np.einsum("ij,ij->i", vectorsBoxSurf, vectorsBoxCenter),
            )
            * 180
            / np.pi
        )

        indicesInnerPoints = np.nonzero(anglesBoxSurf_BoxCenter > 90)[0]
        indicesOuterPoints = np.nonzero(anglesBoxSurf_BoxCenter <= 90)[0]
        anglesNorms_BoxSurf = (
            np.arctan2(
                np.linalg.norm(
                    np.cross(
                        normals,
                        vectorsBoxSurf,
                        axisa=1,
                        axisb=1,
                    ),
                    axis=1,
                ),
                np.einsum("ij,ij->i", normals, vectorsBoxSurf),
            )
            * 180
            / np.pi
        )

        indicesFalseInner = np.nonzero(anglesNorms_BoxSurf[indicesInnerPoints] > 90)[0]
        indicesFalseOuter = np.nonzero(anglesNorms_BoxSurf[indicesOuterPoints] < 90)[0]

        multiplier = np.ones((CloudPoints.shape[0], 1))
        multiplier[indicesInnerPoints[indicesFalseInner]] = -1
        multiplier[indicesOuterPoints[indicesFalseOuter]] = -1

        normals_corrected = multiplier * normals
        return normals_corrected

    def __correctCurvatures__(self):
        self.nearCurvaturesAOld = copy.deepcopy(self.nearCurvatures_a)
        self.curvaturesBOld = copy.deepcopy(self.curvatures_b)
        self.nearCurvatures_a = self.__correctCurvaturesWorker__(self.nearCurvatures_a)
        self.curvatures_b = self.__correctCurvaturesWorker__(self.curvatures_b)

    def __correctCurvaturesWorker__(self, Curvatures):
        Curvatures_New = np.empty((Curvatures.shape[0], 2))
        Curvatures_Abs = np.abs(Curvatures)

        Curvatures_New[:, 0] = np.min(Curvatures_Abs, axis=-1)
        Curvatures_New[:, 1] = np.max(Curvatures_Abs, axis=-1)

        return Curvatures_New

    def __calcGeometricSimilarity__(self) -> float:

        # GS_calc = (
        #     self.w_dist * np.sum(self.GC_d_array ** self.e_d_dist)
        #     + self.w_norm
        #     * np.sum(
        #         (self.GC_d_array ** self.e_d_norm) * (self.GC_n_array ** self.e_e_norm)
        #     )
        #     + self.w_curvMin
        #     * np.sum(
        #         (self.GC_d_array ** self.e_d_curvMin)
        #         * (self.GC_cmin_array ** self.e_e_curvMin)
        #     )
        #     + self.w_curvMax
        #     * np.sum(
        #         (self.GC_d_array ** self.e_d_curvMax)
        #         * (self.GC_cmax_array ** self.e_e_curvMax)
        #     )
        # ) / self.numberOfPoints
        GS_calc = (
            self.w_dist * np.sum(self.GC_d_array ** self.e_d_dist) / self.numberOfPoints
            + self.w_norm
            * np.average(
                self.GC_n_array ** self.e_e_norm,
                weights=self.GC_d_array ** self.e_d_norm,
            )
            + self.w_curvMin
            * np.average(
                self.GC_cmin_array ** self.e_e_curvMin,
                weights=self.GC_d_array ** self.e_d_curvMin,
            )
            + self.w_curvMax
            * np.average(
                self.GC_cmax_array ** self.e_e_curvMax,
                weights=self.GC_d_array ** self.e_d_curvMax,
            )
        )
        ## weighted average = sum(w_i * v_i)/sum(w_i)

        return GS_calc

    def __calcMSEPointCloudDistance__(self) -> float:
        distancesPntsGrid, referenceIndices_a = self.kdtreeobj_a.kneighbors(
            self.cloudPoints_b
        )
        return np.square(distancesPntsGrid).mean(axis=0)

    def __calcPointCloudDistance__(self) -> float:

        self.GC_d_array = (self.maxDistanceDeviation - self.distancesPnts) / (
            self.maxDistanceDeviation - self.minDistance
        )
        DR_calc = np.sum(self.GC_d_array) / self.numberOfPoints
        return DR_calc

    def ln(self, array: np.ndarray):
        return np.log(array, where=(array != 0.0))
        # return np.nan_to_num(np.log(array), posinf=1e100, neginf=-1e100)

    def __calcJacobian__(self, x_in):
        # print("-" * 10)
        # print(x_in)
        # print("-" * 10)
        jacobian = np.empty(len(x_in))
        wCat = set([1, 2, 3])
        dCat = set([5, 7, 9])
        eCat = set([6, 8, 10])

        ## preCalculations to save time
        GC_d_list = [self.GC_tuple[0] ** x_in[4]]
        GC_x_list = [0]
        GC_d_GC_x_lnGC_d_sums = [0]
        GC_d_GC_x_lnGC_x_sums = [0]
        GC_d_GC_x_list = [0]
        GC_d_sums = [0]

        for cat in [1, 2, 3]:
            GC_d_list.append(self.GC_tuple[0] ** x_in[int(cat * 2 + 3)])
            GC_x_list.append(self.GC_tuple[cat] ** x_in[int(cat * 2 + 4)])
            GC_d_GC_x_lnGC_d_sums.append(
                np.sum(GC_d_list[cat] * GC_x_list[cat] * self.GC_ln_tuple[0])
            )
            GC_d_GC_x_lnGC_x_sums.append(
                np.sum(GC_d_list[cat] * GC_x_list[cat] * self.GC_ln_tuple[cat])
            )
            GC_d_GC_x_list.append(np.sum(GC_d_list[cat] * GC_x_list[cat]))
            GC_d_sums.append(np.sum(GC_d_list[cat]))

        for i, x_i in enumerate(x_in):
            if i == 0:
                jacobian[0] = np.sum(GC_d_list[0]) / self.numberOfPoints
            elif i in wCat:
                jacobian[i] = GC_d_GC_x_list[i] / GC_d_sums[i]
            elif i == 4:
                jacobian[i] = (
                    x_in[0]
                    * np.sum(self.GC_ln_tuple[0] * GC_d_list[0])
                    / self.numberOfPoints
                )
            elif i in dCat:
                # d_wi: sum(w_i * v_i)/sum(w_i) = (w1v1+wivi)/(w1+w2)
                # (f/g)' = (f'g-g'f)/g**2 ->
                listPos = int((i - 3) / 2)
                # f'g:
                fg = GC_d_GC_x_lnGC_d_sums[listPos] * GC_d_sums[listPos]
                # g'f:
                GC_d_lnGC_d = np.sum(GC_d_list[listPos] * self.GC_ln_tuple[0])
                gf = GC_d_lnGC_d * GC_d_GC_x_list[listPos]
                # (f/g)'
                jacobian[i] = x_in[listPos] * (fg - gf) / (GC_d_sums[listPos] ** 2)

            elif i in eCat:
                listPos = int((i - 4) / 2)
                jacobian[i] = (
                    x_in[listPos] * GC_d_GC_x_lnGC_x_sums[listPos] / GC_d_sums[listPos]
                )

        return jacobian

    def __calcHessian__(self, x_in):
        hessian = np.zeros((len(x_in), len(x_in)))

        wCat = set([1, 2, 3])
        dCat = set([5, 7, 9])
        eCat = set([6, 8, 10])

        ## preCalculations to save time
        GC_d_list = [self.GC_tuple[0] ** x_in[4]]
        GC_x_list = [0]
        GC_d_GC_x_lnGC_d_sums = [0]
        GC_d_GC_x_lnGC_d2_sums = [0]
        GC_d_GC_x_sums = [0]
        GC_d_GC_x_lnGC_x_sums = [0]
        GC_d_sums = [0]
        GC_d_lnGC_d_sums = [0]
        for cat in [1, 2, 3]:
            dPos = int(cat * 2 + 3)
            ePos = int(cat * 2 + 4)
            GC_d_list.append(self.GC_tuple[0] ** x_in[dPos])
            GC_x_list.append(self.GC_tuple[cat] ** x_in[ePos])
            GC_d_GC_x_lnGC_d_sums.append(
                np.sum(GC_d_list[cat] * GC_x_list[cat] * self.GC_ln_tuple[0])
            )
            GC_d_GC_x_lnGC_d2_sums.append(
                np.sum(GC_d_list[cat] * GC_x_list[cat] * (self.GC_ln_tuple[0] ** 2))
            )
            GC_d_GC_x_sums.append(np.sum(GC_d_list[cat] * GC_x_list[cat]))
            GC_d_GC_x_lnGC_x_sums.append(
                np.sum(GC_d_list[cat] * GC_x_list[cat] * self.GC_ln_tuple[cat])
            )
            GC_d_sums.append(np.sum(GC_d_list[cat]))
            GC_d_lnGC_d_sums.append(np.sum(GC_d_list[cat] * self.GC_ln_tuple[0]))

        i = 0
        j = 4
        hessian[i, j] = hessian[j, i] = (
            np.sum(self.GC_ln_tuple[0] * GC_d_list[0]) / self.numberOfPoints
        )

        i = 4
        j = 4
        hessian[i, j] = (
            x_in[0]
            * np.sum((self.GC_ln_tuple[0] ** 2) * GC_d_list[0])
            / self.numberOfPoints
        )

        for i in range(5, len(x_in)):
            j = i
            listPos = int((i - 3) / 2)
            if i in dCat:

                GC_d_lnGC_d2 = np.sum(GC_d_list[listPos] * (self.GC_ln_tuple[0] ** 2))

                hessian[i, j] = (
                    x_in[listPos]
                    / GC_d_sums[listPos] ** 4
                    * (
                        (
                            GC_d_GC_x_lnGC_d2_sums[listPos] * GC_d_sums[listPos]
                            - GC_d_lnGC_d2 * GC_d_GC_x_sums[listPos]
                        )
                        * GC_d_sums[listPos] ** 2
                        - 2
                        * GC_d_sums[listPos]
                        * GC_d_lnGC_d_sums[listPos]
                        * (
                            GC_d_GC_x_lnGC_d_sums[listPos] * GC_d_sums[listPos]
                            - GC_d_lnGC_d_sums[listPos] * GC_d_GC_x_sums[listPos]
                        )
                    )
                )
            elif i in eCat:
                GC_d_GC_x_lnGC_x2 = np.sum(
                    GC_d_list[listPos]
                    * GC_x_list[listPos]
                    * (self.GC_ln_tuple[listPos] ** 2)
                )

                hessian[i, j] = x_in[listPos] * GC_d_GC_x_lnGC_x2 / GC_d_sums[listPos]

        for i in [1, 2, 3]:
            jd = int(i * 2 + 3)
            listPos = i

            hessian[i, jd] = hessian[jd, i] = (
                GC_d_GC_x_lnGC_d_sums[listPos] * GC_d_sums[listPos]
                - GC_d_lnGC_d_sums[listPos] * GC_d_GC_x_sums[listPos]
            ) / GC_d_sums[listPos] ** 2

            je = int(i * 2 + 4)
            hessian[i, je] = hessian[je, i] = (
                GC_d_GC_x_lnGC_x_sums[listPos] / GC_d_sums[listPos]
            )

        for i in [5, 7, 9]:
            j = i + 1
            listPos = int((i - 3) / 2)

            GC_d_GC_x_lnGC_d_lnGC_x = np.sum(
                GC_d_list[listPos]
                * GC_x_list[listPos]
                * self.GC_ln_tuple[0]
                * self.GC_ln_tuple[listPos]
            )

            hessian[i, j] = hessian[j, i] = (
                x_in[listPos] / GC_d_sums[listPos] ** 2
            ) * (
                GC_d_GC_x_lnGC_d_lnGC_x * GC_d_sums[listPos]
                - GC_d_lnGC_d_sums[listPos] * GC_d_GC_x_lnGC_x_sums[listPos]
            )

        return hessian

    def __setParameters__(self, x: np.ndarray):
        x = np.abs(x)
        self.w_dist = x[0]
        self.w_norm = x[1]
        self.w_curvMin = x[2]
        self.w_curvMax = x[3]
        self.e_d_dist = x[4]
        self.e_d_norm = x[5]
        self.e_e_norm = x[6]
        self.e_d_curvMin = x[7]
        self.e_e_curvMin = x[8]
        self.e_d_curvMax = x[9]
        self.e_e_curvMax = x[10]
