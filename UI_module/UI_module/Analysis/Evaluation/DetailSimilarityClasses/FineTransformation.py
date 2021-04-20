# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math
import copy
import os
import shutil
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors
from Analysis.Evaluation.DetailSimilarityClasses.TransformationClasses import (
    TransformationFunctions,
    TransformationClassCluster,
    TransformationClass,
    PointCloudFunctions,
)
from Shared.Preferences import calcPrefClass
from typing import List, Tuple

# from statsmodels import robust


class FineTransformationCalc:
    def __init__(self, calcPrefs: calcPrefClass):

        self.calcPrefs = calcPrefs
        self.pathexport = None
        self.combination = None
        self.ID_min_pose = None
        self.diff_min_pose = None
        self.min_pose = None

    def start(
        self,
        _cloudPoints_a: np.ndarray,
        _cloudPoints_b: np.ndarray,
        _normals_a: np.ndarray,
        poses: List[TransformationClassCluster],
    ):
        # ptvsd.debug_this_thread()
        valList = []
        for i in range(len(poses)):
            cloudPoints_b_transformed = TransformationFunctions.transformPCPose(
                _cloudPoints_b, poses[i].poseClass
            )

            poseICP, val_min = Functions.icp_mod_point_plane_pyr(
                _cloudPoints_a, cloudPoints_b_transformed, _normals_a, self.calcPrefs
            )

            poses[i].setPoseICP(poseICP)
            valList.append(val_min)

        return poses


class Functions:
    @staticmethod
    def sample_pc_uniform(SrcPc, numPoints):

        nPnts = len(SrcPc)
        # Selection
        if nPnts > numPoints:
            sampledIndices = range(0, nPnts, int(round(nPnts / numPoints)))
            return SrcPc[sampledIndices, :]
        else:
            return SrcPc

    @staticmethod
    def get_duplicates(d, indicesDst, indicesSrc):
        unq, unq_inv, unq_cnt = np.unique(
            indicesDst, return_inverse=True, return_counts=True
        )
        cnt_mask = unq_cnt > 1
        (cnt_idx,) = np.nonzero(cnt_mask)
        idx_mask = np.in1d(unq_inv, cnt_idx)
        (idx_idx,) = np.nonzero(idx_mask)
        srt_idx = np.argsort(unq_inv[idx_mask])
        dup_idx = np.split(idx_idx[srt_idx], np.cumsum(unq_cnt[cnt_mask])[:-1])

        list_to_delete = []
        if len(dup_idx[0]) > 0:
            for dup in dup_idx:
                min_akt = np.inf
                ind_akt = -1
                for i, dup_i in enumerate(dup):
                    if d[dup_i] < min_akt:
                        min_akt = d[dup_i]
                        ind_akt = i
                try:
                    list_to_delete += list(np.delete(dup, ind_akt))
                except:
                    print(dup)
                    print(ind_akt)
                    raise
            newIndicesDst = np.delete(indicesDst, list_to_delete)
            newIndicesSrc = np.delete(indicesSrc, list_to_delete)
        else:
            newIndicesDst = indicesDst
            newIndicesSrc = indicesSrc
        return (
            newIndicesDst[~np.isnan(newIndicesDst)],
            newIndicesSrc[~np.isnan(newIndicesSrc)],
        )

    @staticmethod
    def minimize_point_to_plane(Src, Dst, Normals):
        b = np.einsum(
            "ij,ij->i", (Dst - Src), Normals
        )  # np.dot(_v0, v_1) row wise for all distances and normals
        b = b.reshape(len(b), 1)
        A1 = np.cross(Src, Normals)
        A2 = Normals
        A = np.hstack((A1, A2))
        x = np.linalg.lstsq(A, b, rcond=-1)[0]
        return x

    @staticmethod
    def get_transform_mat(par):

        r = par[0:3]
        t = par[3:6]
        Rx = np.eye(3)
        Ry = np.eye(3)
        Rz = np.eye(3)

        cos0 = math.cos(r[0])
        sin0 = math.sin(r[0])
        cos1 = math.cos(r[1])
        sin1 = math.sin(r[1])
        cos2 = math.cos(r[2])
        sin2 = math.sin(r[2])

        Rx[1][1] = Rx[2][2] = cos0
        Rx[2][1] = sin0
        Rx[1][2] = -sin0

        # Rx = np.array(
        #     [
        #         [1, 0, 0],
        #         [0, np.cos(r[0]), -np.sin(r[0])],
        #         [0, np.sin(r[0]), np.cos(r[0])],
        #     ]
        # )

        Ry[0][0] = Ry[2][2] = cos1
        Ry[2][0] = -sin1
        Ry[0][2] = sin1

        # Ry = np.array(
        #     [
        #         [np.cos(r[1]), 0, np.sin(r[1])],
        #         [0, 1, 0],
        #         [-np.sin(r[1]), 0, np.cos(r[1])],
        #     ]
        # )

        Rz[0][0] = Rz[1][1] = cos2
        Rz[1][0] = sin2
        Rz[0][1] = -sin2

        # Rz = np.array(
        #     [
        #         [np.cos(r[2]), -np.sin(r[2]), 0],
        #         [np.sin(r[2]), np.cos(r[2]), 0],
        #         [0, 0, 1],
        #     ]
        # )

        R_total = Rz.dot(Ry).dot(Rx).astype(float)
        M = np.column_stack((R_total, t))
        return M

    @staticmethod
    def icp_mod_point_plane_pyr(
        _DstPC: np.ndarray,
        _SrcPC: np.ndarray,
        _DstN: np.ndarray,
        calcPrefs: calcPrefClass,
        output=None,
    ) -> Tuple[np.ndarray, float]:
        """calculation of tranformation pose from source point to destination points.
        Output shape of pose = (4,4) = Rotation (3,3) + Translation (3,1) + calculation row (1,4)[0,0,0,1]
        """

        ## comments OpenCV:
        # @brief This class implements a very efficient and robust variant of the iterative closest point (ICP) algorithm.
        # The task is to register a 3D model (or point cloud) against a set of noisy target data. The variants are put together
        # by myself after certain tests. The task is to be able to match partial, noisy point clouds in cluttered scenes, quickly.
        # You will find that my emphasis is on the performance, while retaining the accuracy.
        # This implementation is based on Tolga Birdal's MATLAB implementation in here:
        # http://www.mathworks.com/matlabcentral/fileexchange/47152-icp-registration-using-efficient-variants-and-multi-resolution-scheme
        # The main contributions come from:
        # 1. Picky ICP:
        # http://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2003/Zinsser03-ARI.pdf
        # 2. Efficient variants of the ICP Algorithm:
        # http://docs.happycoders.org/orgadoc/graphics/imaging/fasticp_paper.pdf
        # 3. Geometrically Stable Sampling for the ICP Algorithm: https://graphics.stanford.edu/papers/stabicp/stabicp.pdf
        # 4. Multi-resolution registration:
        # http://www.cvl.iis.u-tokyo.ac.jp/~oishi/Papers/Alignment/Jost_MultiResolutionICP_3DIM03.pdf
        # 5. Linearization of Point-to-Plane metric by Kok Lim Low:
        # https://www.comp.nus.edu.sg/~lowkl/publications/lowk_point-to-plane_icp_techrep.pdf

        # ptvsd.debug_this_thread()

        tolerance = calcPrefs.tolerance_detail_finecalc
        iterations = calcPrefs.iterations_detail_finecalc
        minNumberOfPoints = calcPrefs.numberofpoints_min_detail_finecalc
        outlierScale = calcPrefs.outlierscale_detail_finecalc
        layers = calcPrefs.layers_detail_finecalc

        # increase digits to round beacause of scaling

        DstPC = _DstPC
        DstN = _DstN
        SrcPC = _SrcPC

        useRobustRejection = True if outlierScale > 0 else False

        nPnts = len(SrcPC)

        # Hartley-Zissermann Scaling
        meanSrc = np.mean(SrcPC, axis=0)
        meanDst = np.mean(DstPC, axis=0)
        meanAvg = (meanSrc + meanDst) * 0.5
        SrcPC = SrcPC - meanAvg
        DstPC = DstPC - meanAvg

        # Average distance from origin
        avgDist = (
            np.sum(np.sqrt(np.sum(SrcPC ** 2, axis=1)))
            + np.sum(np.sqrt(np.sum(DstPC ** 2, axis=1)))
        ) * 0.5

        # Scaling to unit sphere
        scale = nPnts / avgDist
        SrcPC = SrcPC * scale
        DstPC = DstPC * scale

        # increase digits to round beacause of scaling
        digits_round_pos = calcPrefs.digits_round_pos + int(
            round(-1 * math.log10(scale), 0)
        )
        digits_round_dir = calcPrefs.digits_round_dir + int(
            round(-1 * math.log10(scale), 0)
        )

        # define first transformation class with the rotation matrix as identity matrix
        pose = np.column_stack((np.eye(3), np.zeros((3, 1))))
        pose = np.vstack((pose, np.array([0, 0, 0, 1])))
        poseClass = TransformationClass(1, digits_round_pos, digits_round_dir)
        poseClass.setPose(pose)

        # define nearest neighbor search
        kdtreeobj = NearestNeighbors(
            n_neighbors=1, algorithm="kd_tree", leaf_size=8
        ).fit(DstPC)

        # optimization pyramid - detail level from coarse to fine
        for level in range(layers, -1, -1):

            # level dependend preferences
            # number of points to be sampled from cloud
            numSamplesLevel = max(int(nPnts / (2 ** float(level))), minNumberOfPoints)

            # tolerance level of convergence
            tolLevel = tolerance * (float(level + 1) ** 2)

            # maximal number of iteration
            iterationsLevel = int(float(iterations) / (float(level + 1.0)))

            # transform source points with actual pose
            SrcPCLevel = TransformationFunctions.transformPCPose(SrcPC, poseClass)

            # sampling of points
            SrcPCLevel = Functions.sample_pc_uniform(SrcPCLevel, numSamplesLevel)
            nrPnts = len(SrcPCLevel)

            # deviation of previous iteration
            fval_old = np.inf
            # deviation change
            fval_perc = 0.0  # 1.0
            # transformed points
            Src_Moved_i = copy.deepcopy(SrcPCLevel)

            # minimum deviation
            fval_min = np.inf

            # iteration loop ICP
            i = 0
            while (
                fval_perc > (1.0 + tolLevel) or fval_perc < (1.0 - tolLevel)
            ) and i < iterationsLevel:

                # Picky ICP or BC-ICP

                # search nearest points
                distance, indicesDst = kdtreeobj.kneighbors(Src_Moved_i)

                # reshape arrays

                distance = distance.reshape(nrPnts)
                indicesDst = indicesDst.reshape(nrPnts)
                indicesSrc = np.array(range(0, nrPnts))

                # Step 1 of ICP : Robustly reject outliers
                if useRobustRejection == True and np.min(distance) > 0.0:
                    med = np.median(distance[distance > 0.0])
                    sigma = 1.48257968 * np.median(
                        np.abs(distance[distance > 0.0] - med)
                    )

                    threshold = outlierScale * sigma + med
                    sampledIndices = np.asarray(distance <= threshold).nonzero()
                    indicesDst = indicesDst[sampledIndices]
                    indicesSrc = indicesSrc[sampledIndices]

                # Step 2 of Picky ICP:
                # Among the resulting corresponding pairs, if more than one scene point p_i
                # is assigned to the same model point m_j, then select p_i that corresponds
                # to the minimum distance.
                mapDst, mapSrc = Functions.get_duplicates(
                    distance, indicesDst, indicesSrc
                )

                # pick unique points
                SrcMatchUnique = SrcPCLevel[mapSrc, :]
                DstMatchUnique = DstPC[mapDst, :]
                DstNMatchUnique = DstN[mapDst, :]

                x = Functions.minimize_point_to_plane(
                    SrcMatchUnique, DstMatchUnique, DstNMatchUnique
                )

                # Make the transformation matrix
                poseIteration = Functions.get_transform_mat(x)
                poseIteration = np.vstack((poseIteration, np.array([0, 0, 0, 1])))
                poseIterationClass = TransformationClass(
                    1, digits_round_pos, digits_round_dir
                )
                poseIterationClass.setPose(poseIteration)

                # Transform the Points
                Src_Moved_i = TransformationFunctions.transformPCPose(
                    SrcPCLevel, poseIterationClass
                )

                # mean point deviation after transformation
                fval = np.linalg.norm((Src_Moved_i[mapSrc, :] - DstMatchUnique)) / len(
                    DstMatchUnique
                )

                # deviation change
                if fval == 0:
                    fval_perc = 1
                else:
                    fval_perc = fval / fval_old

                # Store deviation value
                fval_old = fval

                if fval < fval_min:
                    fval_min = fval
                    poseMin = poseIterationClass

                # release some memory
                del SrcMatchUnique, DstMatchUnique, DstNMatchUnique
                i = i + 1

            poseClass.poseComposition(poseMin)

            if not output is None:
                poseSave = copy.deepcopy(poseClass)
                poseSave.setT(poseSave.t / scale + meanAvg - poseSave.R.dot(meanAvg))
                output.append(poseSave)

        poseClass.setT(poseClass.t / scale + meanAvg - poseClass.R.dot(meanAvg))
        return poseClass, fval_min
