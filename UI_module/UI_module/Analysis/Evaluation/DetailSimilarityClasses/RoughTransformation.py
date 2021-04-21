# -*- coding: utf-8 -*-
import collections
import copy
import itertools
import math
import multiprocessing as mp
import operator
import os
import pickle as _pi
import shutil
import time
import random
from typing import List, Tuple
import cProfile, pstats, io
from pstats import SortKey

import numpy as np
import scipy as sp

from Analysis.Evaluation.DetailSimilarityClasses.TransformationClasses import (
    TransformationClass,
    TransformationClassCluster,
    TransformationFunctions,
    PointCloudFunctions,
    BoxTransformationClass,
    BoundingBox,
)
from Shared.PartInfo import PartInfoClass
from Shared.Preferences import calcPrefClass


class RoughTransformationCalc:
    def __init__(self, calcPrefs: calcPrefClass):

        ## list of preferences for training
        self.preferenceList = [
            calcPrefs.samplingpoints_detail_roughcalc,
            calcPrefs.anglediscretisation_detail_roughcalc,
            calcPrefs.sampling_distancehash_detail_roughcalc,
            calcPrefs.digits_round_pos,
            calcPrefs.digits_round_dir,
        ]

        self.calcPrefs = calcPrefs
        self.sampling_distanceHash = calcPrefs.sampling_distancehash_detail_roughcalc
        self.angle_step_relative = calcPrefs.anglediscretisation_detail_roughcalc
        self.angle_step = (self.angle_step_relative) * math.pi / 180.0
        # self.samples_choice = calcPrefs.samplingpoints_detail_roughcalc

        self.use_weighted_avg = False
        self.name_part_a = "a"
        self.name_part_b = "b"
        self.hash_table_a = {}
        self.hash_table_b = {}

        self.combsMax = 50000

    def trainModel(
        self,
        part_a: PartInfoClass,
        partData_a: np.ndarray,
        part_a_BoundingBox: BoundingBox,
        noSave=False,
    ):
        """Train and save point cloud data"""
        self.part_a = part_a
        self.trained_a = False
        self.noSave = noSave
        # check if data was trained before
        if (
            os.path.exists(part_a.path_pointCloudDataPreferences) == True
            and os.path.exists(part_a.path_pointCloudDataTrained) == True
            and self.noSave == False
        ):
            self.checkLocalData(self.part_a, True)

        if self.trained_a == False:
            ## Sample points from point cloud with bounding box
            sampled = PointCloudFunctions.samplePCByQuantization(
                partData_a, part_a_BoundingBox, self.calcPrefs
            )

            self.hash_table_a = {}

            numRefPoints = int(
                sampled.shape[0]  # pylint: disable=E1136  # pylint/issues/3139
            )
            combs = np.array(list(itertools.combinations(range(numRefPoints), 3)))
            cpuCount = mp.cpu_count()
            cpusFor500combs = (
                combs.shape[0] / 500.0  # pylint: disable=E1136  # pylint/issues/3139
            )
            if cpusFor500combs < cpuCount:
                cpuCount = int(round(cpusFor500combs, 0))
                if cpuCount == 0:
                    cpuCount = 1
            splitCombs = np.array_split(combs, cpuCount, axis=0)

            hashPoolList_a = []
            trainingPool_a = mp.Pool(cpuCount)
            for comb in splitCombs:
                # self.hashTrainingWorker(comb, sampled)
                hashPoolList_a.append(
                    trainingPool_a.apply_async(
                        hashTrainingWorker,
                        args=(
                            comb,
                            sampled,
                            self.angle_step,
                            self.sampling_distanceHash,
                        ),
                    )
                )

            trainingPool_a.close()
            trainingPool_a.join()

            for hashProcess_a in hashPoolList_a:
                hashDict = hashProcess_a.get()
                for key, value in hashDict.items():
                    if key in self.hash_table_a:
                        self.hash_table_a[key].extend(value)
                    else:
                        self.hash_table_a[key] = value

            del hashPoolList_a

            if self.noSave == False:
                self.save_fkt(self.part_a)

    def roughMatch(
        self,
        part_b: PartInfoClass,
        partData_b: np.ndarray,
        part_b_BoundingBox: BoundingBox,
        poseClusters: List[TransformationClassCluster] = [],
    ) -> List[TransformationClassCluster]:

        self.part_b = part_b
        self.trained_b = False

        # check if data was trained before
        if (
            os.path.exists(part_b.path_pointCloudDataPreferences) == True
            and os.path.exists(part_b.path_pointCloudDataTrained) == True
            and self.noSave == False
        ):
            self.checkLocalData(self.part_b, False)

        if self.trained_b == False:
            if self.noSave == False:
                self.hash_table_a = {}  # free RAM for training

            # xRange, yRange, zRange = PointCloudFunctions.computeBboxStd(partData_b)
            ## Sample points from point cloud
            sampled = PointCloudFunctions.samplePCByQuantization(
                partData_b, part_b_BoundingBox, self.calcPrefs
            )

            self.hash_table_b = {}

            numRefPoints = int(
                sampled.shape[0]  # pylint: disable=E1136  # pylint/issues/3139
            )
            combs = np.array(list(itertools.combinations(range(numRefPoints), 3)))
            cpuCount = mp.cpu_count()
            cpusFor500combs = (
                combs.shape[0] / 500.0  # pylint: disable=E1136  # pylint/issues/3139
            )
            if cpusFor500combs < cpuCount:
                cpuCount = int(round(cpusFor500combs, 0))
                if cpuCount == 0:
                    cpuCount = 1
            splitCombs = np.array_split(combs, cpuCount, axis=0)

            hashPoolList_b = []
            trainingPool_b = mp.Pool(cpuCount)
            for comb in splitCombs:
                # self.hashTrainingWorker(comb, sampled)
                hashPoolList_b.append(
                    trainingPool_b.apply_async(
                        hashTrainingWorker,
                        args=(
                            comb,
                            sampled,
                            self.angle_step,
                            self.sampling_distanceHash,
                        ),
                    )
                )

            trainingPool_b.close()
            trainingPool_b.join()

            for hashProcess_b in hashPoolList_b:
                hashDict = hashProcess_b.get()
                for key, value in hashDict.items():
                    if key in self.hash_table_b:
                        self.hash_table_b[key].extend(value)
                    else:
                        self.hash_table_b[key] = value
            del hashPoolList_b

            if self.noSave == False:
                self.save_fkt(self.part_b, False)
                self.load_fkt(self.part_a, True)
        else:
            self.load_fkt(self.part_b, False)
            if len(self.hash_table_a) == 0:
                self.load_fkt(self.part_a, True)

        return self.comparePoses(poseClusters)

    def comparePoses(
        self, poseClusters: List[TransformationClassCluster]
    ) -> List[TransformationClassCluster]:

        hashKeys_table_b = list(self.hash_table_b.keys())
        hashKeys_AB = []
        compsAB = 0
        for hashB in hashKeys_table_b:
            if hashB in self.hash_table_a:
                hashKeys_AB.append(hashB)
                compsAB += len(self.hash_table_b[hashB]) * len(self.hash_table_a[hashB])

        # check if number of combinations is to high -> leads to long computations
        # if compsAB exceeds self.combsMax self.reduceHashTables is used for data reduction

        reduction = compsAB / self.combsMax
        compsAB = min(compsAB, self.combsMax)

        cpuCount = mp.cpu_count()
        cpusFor1000combs = compsAB / 1000.0
        if cpusFor1000combs < cpuCount:
            cpuCount = int(round(cpusFor1000combs, 0))
            if cpuCount == 0:
                cpuCount = 1

        points_a = collections.deque()
        points_b = collections.deque()
        compsABperCpu = int(compsAB / cpuCount)
        compsCheck = 0
        compsCheckSum = 0
        lastLoop = False
        lastRest = 0
        restReduction = 0
        dataPackages = []
        for HashAB in hashKeys_AB:
            if reduction <= 1:
                points_a.append(self.hash_table_a[HashAB])
                points_b.append(self.hash_table_b[HashAB])
            else:
                hashA, hashB, restReduction = self.reduceHashTables(
                    reduction,
                    self.hash_table_a[HashAB],
                    self.hash_table_b[HashAB],
                    restReduction,
                )
                points_a.append(hashA)
                points_b.append(hashB)

            compsCheck += len(self.hash_table_a[HashAB]) * len(
                self.hash_table_b[HashAB]
            )
            del self.hash_table_a[HashAB], self.hash_table_b[HashAB]  # free RAM

            if compsCheck >= compsABperCpu:
                dataPackages.append((points_a, points_b))
                points_a = collections.deque()
                points_b = collections.deque()
                compsCheckSum += compsCheck
                compsCheck = 0
                if abs(compsCheckSum - compsAB) < compsABperCpu:
                    lastLoop = True
                    lastRest = abs(compsCheckSum - compsAB)
            elif lastLoop == True and compsCheck == lastRest:
                dataPackages.append((points_a, points_b))
                break

        # free RAM
        self.hash_table_a = {}
        self.hash_table_b = {}

        # start_ip = time.time()
        hashPoolList = []
        hashComparePool = mp.Pool(cpuCount)
        workerCount = 0
        for dataPack in dataPackages:
            hashPoolList.append(
                hashComparePool.apply_async(
                    comparePosesWorker,
                    args=(
                        dataPack[0],
                        dataPack[1],
                        self.sampling_distanceHash,
                        self.calcPrefs.digits_round_pos,
                        self.calcPrefs.digits_round_dir,
                        workerCount,
                    ),
                )
            )
            # comparePosesWorker(
            #     dataPack[0],
            #     dataPack[1],
            #     self.sampling_distanceHash,
            #     self.calcPrefs.digits_round_pos,
            #     self.calcPrefs.digits_round_dir,
            #     workerCount,
            # )
            workerCount += 1

        hashComparePool.close()
        hashComparePool.join()

        # end_ip = time.time()
        # print(
        #     "Time for rough comparison of {} combinations = {}".format(
        #         compsAB, round(end_ip - start_ip, 4)
        #     )
        # )

        poses_dict = {}
        usedHashs = set(pose.hashKey for pose in poseClusters)
        for hashProcess in hashPoolList:
            hashDict = hashProcess.get()
            for key, pose_new in hashDict.items():
                if not key in usedHashs:
                    if key in poses_dict:
                        poses_dict[key].addPose(pose_new)
                    else:
                        poses_dict[key] = TransformationClassCluster(
                            pose_new, key, self.calcPrefs
                        )
        del hashPoolList

        # recalc hash of poses after joining poses
        poses_dict_cleared = {}
        for pose in poses_dict.values():
            poseHash = PointCloudFunctions.poseHash(pose.poseClass)
            if not poseHash in usedHashs:
                poses_dict_cleared[poseHash] = pose

        poses_list_sorted = list(
            poses_dict_cleared.values()
        )  # type: List[TransformationClassCluster]
        keyfun = operator.attrgetter("numVotes")
        poses_list_sorted = sorted(poses_list_sorted, key=keyfun, reverse=True)

        poses_list_out = []

        numOfPoses = len(poses_list_sorted)
        if numOfPoses == 0:
            print("No new poses from rough transformations, try ICP without posing")
            ##Update to 10 random rotaion matrices and standard translation
            pose_zero = TransformationClass(
                1, self.calcPrefs.digits_round_pos, self.calcPrefs.digits_round_dir
            )
            r_0 = np.eye(3)
            t_0 = np.zeros(3)
            pose_zero.setRT(r_0, t_0)
            poseHash = PointCloudFunctions.poseHash(pose_zero)
            poses_list_out = [
                TransformationClassCluster(
                    pose_zero, (0, 0, 0, 0, 0, 0, 0, 0), self.calcPrefs
                )
            ]

        else:
            poses_list_out = poses_list_sorted[0:50]
        return poses_list_out

    def reduceHashTables(
        self, reduction: float, hashSetA: List, hashSetB: List, rest: float = 0
    ):

        lenA = len(hashSetA)
        lenB = len(hashSetB)
        combs = lenA * lenB
        objective = max(
            combs / reduction - rest, min(5, combs)
        )  # objective shouldn not be less 5 or combs if combs < 5

        minArrayOrg = "A"
        lenMin = lenA
        lenMax = lenB
        if lenMin > lenMax:
            minArrayOrg = "B"
            lenMin = lenB
            lenMax = lenB

        lenMin_X = lenMin
        lenMax_X = lenMax
        combs_X = combs
        combs_diff_X = np.inf
        diff_diff_X = np.inf
        diff_diff_m1 = np.inf

        # iterative search for best array lengths to achieve the combination objective
        for i in range(lenMin):
            lenMin_i = lenMin - i
            lenMax_i = round(objective / lenMin_i, 0)

            diff_min = i
            diff_max = lenMax - lenMax_i
            diff_diff = abs(diff_max - diff_min)

            if diff_diff > diff_diff_m1 or diff_max < 0:
                break

            diff_diff_m1 = diff_diff
            combi = lenMax_i * lenMin_i
            combi_diff = abs(objective - combi)

            if (combi_diff < combs_diff_X and diff_diff <= diff_diff_X) or (
                combi_diff <= combs_diff_X and diff_diff < diff_diff_X
            ):
                combs_X = combi
                combs_diff_X = combi_diff
                diff_diff_X = diff_diff
                lenMin_X = lenMin_i
                lenMax_X = lenMax_i

        rest_X = combs_X - objective

        if minArrayOrg == "A":
            hashSetA_s = random.sample(hashSetA, int(lenMin_X))
            hashSetB_s = random.sample(hashSetB, int(lenMax_X))

            return (hashSetA_s, hashSetB_s, rest_X)
        else:
            hashSetA_s = random.sample(hashSetA, int(lenMax_X))
            hashSetB_s = random.sample(hashSetB, int(lenMin_X))

            return (hashSetA_s, hashSetB_s, rest_X)

    def save_fkt(self, part: PartInfoClass, part_a: bool = True):
        """Save preferences and trained data"""

        # preferences part
        pickle_preferences = open(part.path_pointCloudDataPreferences, "wb")
        _pi.dump(self.preferenceList, pickle_preferences, _pi.HIGHEST_PROTOCOL)
        pickle_preferences.close()

        # data dictionary
        pickle_data = open(part.path_pointCloudDataTrained, "wb")
        if part_a == True:
            # data part a
            _pi.dump(self.hash_table_a, pickle_data, _pi.HIGHEST_PROTOCOL)
        else:
            # data part b
            _pi.dump(self.hash_table_b, pickle_data, _pi.HIGHEST_PROTOCOL)
        pickle_data.close()

    def load_fkt(self, part: PartInfoClass, part_a: bool = True):
        """Load trained data"""
        # data dictionary
        pickle_data = open(part.path_pointCloudDataTrained, "rb")
        if part_a == True:
            self.hash_table_a = _pi.load(pickle_data)
        else:
            self.hash_table_b = _pi.load(pickle_data)
        pickle_data.close()

    def checkLocalData(self, part: PartInfoClass, part_a: bool = True):
        """Load and compaer preferences"""
        # preferences
        pickle_preferences = open(part.path_pointCloudDataPreferences, "rb")
        preferenceList = _pi.load(pickle_preferences)
        pickle_preferences.close()

        # check if same preferences were used
        trained = True
        for sP, savedPreference in enumerate(preferenceList):
            if savedPreference != self.preferenceList[sP]:
                trained = False
        if trained == True:
            if part_a == True:
                self.trained_a = True
            else:
                self.trained_b = True


####################################################
################# worker functions #################
####################################################


def hashTrainingWorker(
    combinationList, sampledPoints, angle_step, sampling_distanceHash
):
    hashTable = {}
    for i, j, k in combinationList:

        p1 = sampledPoints[i][0:3]
        n1 = sampledPoints[i][3:6]

        p2 = sampledPoints[j][0:3]
        n2 = sampledPoints[j][3:6]

        p3 = sampledPoints[k][0:3]
        n3 = sampledPoints[k][3:6]

        f_list, points_sorted_list = computePPFFeatures((p1, n1), (p2, n2), (p3, n3))

        for l, f in enumerate(f_list):

            key = PointCloudFunctions.hashPPF(f, angle_step, sampling_distanceHash)

            if key in hashTable:
                hashTable[key].append(points_sorted_list[l])
            else:
                hashTable[key] = [points_sorted_list[l]]

    return hashTable


def computePPFFeatures(_pn1, _pn2, _pn3):
    point_list = [_pn1, _pn2, _pn3]
    d_list = []

    for pair in itertools.combinations(range(len(point_list)), 2):
        pair_1 = point_list[pair[0]]
        pair_2 = point_list[pair[1]]
        d_0 = pair_2[0] - pair_1[0]
        d_len = round(np.linalg.norm(d_0), 5)
        d_list.append((d_0 / d_len, d_len, pair))

    d_list = sorted(d_list, key=operator.itemgetter(1), reverse=True)
    lens_counter = collections.Counter(y for (x, y, z) in d_list).items()
    max_i_d_len = 0
    max_d_len = 0
    for d_len in lens_counter:
        if d_len[1] > 1:
            max_i_d_len = d_len[1]
            max_d_len = d_len[0]

    def build_f_points(_d_list):
        angles = []
        lenghts = []
        point_dict = dict.fromkeys(range(len(point_list)), 0)

        for i, d_tup in enumerate(_d_list):
            rank = len(d_list) - i
            p_1 = d_tup[2][0]
            point_dict[p_1] += rank
            n_1 = point_list[p_1][1]

            p_2 = d_tup[2][1]
            point_dict[p_2] += rank
            n_2 = point_list[p_2][1]

            a_12 = PointCloudFunctions.TAngle3Normalized(n_1, n_2)
            if np.isnan(a_12):
                a_12 = np.array([-1])
            angles += [a_12]
            d_len = d_tup[1]
            lenghts.append(d_len)

        f = {"angles": angles, "lenghts": lenghts}
        point_list_sort = sorted(
            point_dict.items(), key=operator.itemgetter(1), reverse=True
        )
        points_sorted = [
            point_list[point_list_sort[0][0]][0],
            point_list[point_list_sort[1][0]][0],
            point_list[point_list_sort[2][0]][0],
        ]

        return f, points_sorted

    if max_i_d_len == 0:
        f, points_sorted = build_f_points(d_list)
        return [f], [points_sorted]
    elif max_i_d_len == 2:
        check_pos_0 = d_list[0][1] == max_d_len
        if check_pos_0 == True:
            pos_ch = list(itertools.permutations(range(0, 2), 2))
            pos_0 = [2]
            pos_out = []
            for pos_ch_curr in pos_ch:
                pos_out.append(list(pos_ch_curr) + pos_0)
        else:
            pos_ch = list(itertools.permutations(range(1, 3), 2))
            pos_0 = [0]
            pos_out = []
            for pos_ch_curr in pos_ch:
                pos_out.append(pos_0 + list(pos_ch_curr))

        points_sorted_list = []
        f_list = []
        for pos in pos_out:
            d_list_curr = []
            for pos_i in pos:
                d_list_curr.append(d_list[pos_i])
            f, points_sorted = build_f_points(d_list_curr)
            f_list.append(f)
            points_sorted_list.append(points_sorted)
        return f_list, points_sorted_list
    else:
        pos_out = list(itertools.permutations(range(3), 3))
        points_sorted_list = []
        f_list = []
        for pos in pos_out:
            d_list_curr = []
            for pos_i in pos:
                d_list_curr.append(d_list[pos_i])
            f, points_sorted = build_f_points(d_list_curr)
            f_list.append(f)
            points_sorted_list.append(points_sorted)
        return f_list, points_sorted_list


def comparePosesWorker(
    pointLists_a,
    pointLists_b,
    sampling_distanceHash,
    digits_round_pos,
    digits_round_dir,
    workerCount,
):
    pose_dict = {}
    for ih in range(len(pointLists_a)):
        points_a = pointLists_a[ih]
        points_b = pointLists_b[ih]
        for node_a in points_a:
            for node_b in points_b:

                koords_origin_sorted = np.vstack((node_b[0], node_b[1], node_b[2]))
                koords_dest_sorted = np.vstack((node_a[0], node_a[1], node_a[2]))

                try:
                    (R_curr, t_curr) = PointCloudFunctions.rigitMotion(
                        koords_origin_sorted, koords_dest_sorted, sampling_distanceHash
                    )
                except:
                    continue

                check_det = math.fabs(np.linalg.det(R_curr))
                det_bool = False
                if round(abs(check_det), 1) != 1.0:
                    # print("EQUAL CHECK")
                    # difficulties if points are identical
                    checkEqualityOfPoints = np.allclose(
                        koords_origin_sorted,
                        koords_dest_sorted,
                        0.0,
                        10 ** (-digits_round_pos),
                    )
                    if checkEqualityOfPoints:
                        # print("true")
                        R_curr = np.identity(3)
                        t_curr = np.zeros(3)
                        check_det = 1
                        det_bool = True
                    else:
                        # print("false")
                        pass
                else:
                    det_bool = True

                if det_bool == True:

                    koords_dest_test = R_curr.dot(koords_origin_sorted.T).T + t_curr
                    koords_dest_delta = np.absolute(
                        koords_dest_sorted - koords_dest_test
                    )
                    rigidMotionTest = np.linalg.norm(koords_dest_delta)
                    # transformation distance should be less 5mm
                    if rigidMotionTest <= 5:

                        pose_class = TransformationClass(
                            1, digits_round_pos, digits_round_dir
                        )
                        pose_class.setRT(R_curr, t_curr)
                        poseHash = PointCloudFunctions.poseHash(pose_class)

                        if poseHash in pose_dict:
                            pose_dict[poseHash].numVotes += 1
                        else:
                            pose_dict[poseHash] = pose_class
    return pose_dict
