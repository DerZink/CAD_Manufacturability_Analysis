# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import math, copy, os, shutil, operator, EE_ICP
import pickle as _pi
import Global_Variables as GV
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

EPS = 1.192092896e-07
PPF_LENGTH = 5


class EE_PPF3DDetector:
    def computeBboxStd(self, _data=np.array):
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

    def samplePCByQuantization(
        self, _data, xrange, yrange, zrange, sampleStep, weightByCenter=True
    ):

        numSamplesDim = int(1.0 / sampleStep)

        xr = xrange[1] - xrange[0]
        yr = yrange[1] - yrange[0]
        zr = zrange[1] - zrange[0]

        # numPoints = 0

        map = {}  # [[]]*((numSamplesDim+1)*(numSamplesDim+1)*(numSamplesDim+1))

        for i, punkt in enumerate(_data):

            xCell = int(float(numSamplesDim) * (punkt[0] - xrange[0]) / xr)
            yCell = int(float(numSamplesDim) * (punkt[1] - yrange[0]) / yr)
            zCell = int(float(numSamplesDim) * (punkt[2] - zrange[0]) / zr)
            index = (
                xCell * numSamplesDim * numSamplesDim + yCell * numSamplesDim + zCell
            )

            if not index in map:
                map[index] = [i]
            else:
                map[index].append(i)

            # map[index].append(i)

        # for map_i in map:
        numPoints = len(map)

        pcSampled = np.empty((numPoints, _data.shape[1]), dtype=float)
        c = 0
        for map_i in map:
            px = py = pz = 0.0
            nx = ny = nz = 0.0

            map_zeile = map[map_i]
            cn = len(map_zeile)

            if weightByCenter == True:
                weightSum = 0
                zCell = map_i % numSamplesDim
                yCell = ((map_i - zCell) / numSamplesDim) % numSamplesDim
                xCell = (map_i - zCell - yCell * numSamplesDim) / (
                    numSamplesDim * numSamplesDim
                )
                xc = (xCell + 0.5) * xr / numSamplesDim + xrange[0]
                yc = (yCell + 0.5) * yr / numSamplesDim + yrange[0]
                zc = (zCell + 0.5) * zr / numSamplesDim + zrange[0]

                for j in range(cn):
                    ptInd = map_zeile[j]
                    point = _data[ptInd]
                    dx = point[0] - xc
                    dy = point[1] - yc
                    dz = point[2] - zc
                    d = math.sqrt(dx * dx + dy * dy + dz * dz)
                    w = 0
                    if d > EPS:
                        w = 1.0 / d

                    px += w * point[0]
                    py += w * point[1]
                    pz += w * point[2]
                    nx += w * point[3]
                    ny += w * point[4]
                    nz += w * point[5]

                    weightSum += w

                weightSum = float(weightSum)
                px /= weightSum
                py /= weightSum
                pz /= weightSum
                nx /= weightSum
                ny /= weightSum
                nz /= weightSum
            else:
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
            pcData[0] = float(px)
            pcData[1] = float(py)
            pcData[2] = float(pz)

            norm = math.sqrt(nx * nx + ny * ny + nz * nz)

            if norm > EPS:

                pcData[3] = float(nx / norm)
                pcData[4] = float(ny / norm)
                pcData[5] = float(nz / norm)
            c += 1

        return pcSampled

    def TAngle3Normalized(self, _v0, v_1):
        return np.arccos(_v0.dot(v_1))

    def hashPPF(self, _f, _angle_step_radians, _distanceStep):
        key = np.zeros((4, 1), dtype=int)
        key[0] = int(float(_f[0]) / _angle_step_radians)
        key[1] = int(float(_f[1]) / _angle_step_radians)
        key[2] = int(float(_f[2]) / _angle_step_radians)
        key[3] = int(float(_f[3]) / _distanceStep)
        # hashkey=PMurHash32(42,key,"dummy")
        hashvalue = hash(tuple(map(float, key)))
        return key, hashvalue

    def computeAlpha(self, _p1, _n1, _p2):

        R, Tmg = computeTransformRT(_p1, _n1)
        mpt = Tmg + R.dot(_p2)
        alpha = np.arctan2(-mpt[2], mpt[1])
        if np.sin(alpha) * mpt[2] < 0.0:
            alpha = -alpha

        return alpha, mpt

    def computeTransformRT(self, _p1, _n1):
        ## Winkel mit x-Achse und orthogonaler Vektor
        ##--> Rotationsmatrix + Translationsvektor
        ## dot product with x axis
        angle = np.arccos(_n1[0])
        ## cross product with x axis
        axis = np.array([0, _n1[2], -_n1[1]])

        if _n1[1] == 0 and _n1[2] == 0:
            axis[1] = 1
            axis[2] = 0
        else:
            norm = np.linalg.norm(axis)
            if norm > EPS:
                axis *= 1.0 / norm

        R = aaToR(axis, angle)
        t = -R.dot(_p1)
        return R, t

    def aaToR(self, _axis, _angle):
        sinA = np.sin(_angle)
        cosA = np.cos(_angle)
        cos1A = 1.0 - cosA

        # R=np.eye(3)*cosA

        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(_axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(_angle / 2.0)
        b, c, d = -axis * math.sin(_angle / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        R = np.array(
            [
                [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
            ]
        )

        # for i in range(3):
        #    for j in range(3):
        #        if i!=j:
        #            if_erg=0
        #            if (i + 1) % 3 == j:
        #                if_erg=-1
        #            else:
        #                if_erg=1
        #            R[i][j]+=if_erg * sinA * _axis[3 - i - j]
        #        R[i][j] += cos1A * _axis[i] * _axis[j]

        R = R * (math.sqrt(3) / np.linalg.norm(R))
        return R

    def rtToPose(self, _R, _t):
        P = np.hstack((_R, _t))
        P_v = np.zeros((1, 4))
        P_v[0][3] = 1
        Pose = np.vstack((P, P_v))
        return Pose

    def poseToRT(self, _Pose):
        R = self.poseToR(_Pose)
        t = _Pose[:3, 3:4]
        return R, t

    def poseToR(self, _Pose):
        R = _Pose[:3, :3]
        return R

    def getUnitXRotation(self, _angle):
        sx = math.sin(_angle)
        cx = math.cos(_angle)

        Rx = np.eye(3)
        Rx[1, 1] = cx
        Rx[1, 2] = -sx
        Rx[2, 1] = sx
        Rx[2, 2] = cx

        return Rx

    def dcmToQuat(self, _R):
        q = np.empty((4, 1))
        tr = np.trace(_R)
        v = np.empty((3, 1))
        v[0] = _R[0, 0]
        v[1] = _R[1, 1]
        v[2] = _R[2, 2]

        if tr > 0.0:
            idx = 3  ## Org =3
            tr_x = tr
        else:
            idx = np.argmax(v)
            tr_x = 2 * _R[idx, idx] - tr

        norm4 = q[(idx + 1) % 4] = 1.0 + tr_x
        if idx % 2 == 0:
            step = -1
        else:
            step = 1
        curr = 3

        for i in range(3):
            curr = (curr + step) % 4
            next = (curr + 1) % 3
            prev = (curr + 2) % 3
            if tr > 0.0 or idx == curr:
                q_z = -1
            else:
                q_z = 1

            # q[(idx + i + 2) % 4] = _R[next, prev] + q_z * _R[prev, next]
            q[(idx + i + 2) % 4] = _R[prev, next] + q_z * _R[next, prev]
        q *= 0.5 / math.sqrt(norm4)
        return q

    def quatToDCM(self, _q):
        sq = _q * _q
        R = np.zeros((3, 3))
        R[0, 0] = sq[0] + sq[1] - sq[2] - sq[3]
        R[1, 1] = sq[0] - sq[1] + sq[2] - sq[3]
        R[2, 2] = sq[0] - sq[1] - sq[2] + sq[3]

        tmp1 = _q[1] * _q[2]
        tmp2 = _q[3] * _q[0]

        R[0, 1] = 2.0 * (tmp1 + tmp2)
        R[1, 0] = 2.0 * (tmp1 - tmp2)

        tmp1 = _q[1] * _q[3]
        tmp2 = _q[2] * _q[0]

        R[0, 2] = 2.0 * (tmp1 - tmp2)
        R[2, 0] = 2.0 * (tmp1 + tmp2)

        tmp1 = _q[2] * _q[3]
        tmp2 = _q[1] * _q[0]

        R[1, 2] = 2.0 * (tmp1 + tmp2)
        R[2, 1] = 2.0 * (tmp1 - tmp2)

        return R

    def _plot_export(
        self, Src_Moved, DstPCOrig, _name, pathexport=None, combination=None
    ):
        fig = plt.figure()
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
            pathexport = r"D:\Bauteil_Karte\01_data-Bauteil"
        if combination == None:
            combination = ["NaN", "NaN"]
        path_export_spez = pathexport + r"/{}vs{}_ICP_export".format(
            combination[0], combination[1]
        )
        if os.path.isdir(path_export_spez) == False:
            os.makedirs(path_export_spez)
        elif _name == "00_Status":
            shutil.rmtree(path_export_spez)
            os.makedirs(path_export_spez)

        plt.savefig(path_export_spez + r"/{}.png".format(_name))
        # plt.show()
        plt.close()

    def _check_poses(self, _poses, _data_1, _data_2, _kr_1, _kr_2):
        print("+" * 50)
        print("Controlling Poses")
        data_2_pkte = _data_2[:, 0:3]
        kdtreeobj = NearestNeighbors(
            n_neighbors=1, algorithm="kd_tree", leaf_size=8
        ).fit(data_2_pkte)
        min = min_kr = np.inf
        pose_i = pose_i_kr = None

        for i, pose in enumerate(_poses):
            Src_zw = EE_ICP.transformPCPose(_data_1, pose.pose)
            data_1_pkte = Src_zw[:, 0:3]
            d, j = kdtreeobj.kneighbors(data_1_pkte)
            # newJ,newI=EE_ICP.get_duplicates(d,j,np.arange(len(Src_zw)))
            newJ = j
            newI = range(len(data_1_pkte))
            data_1_nearest = data_1_pkte[newI].reshape(len(newI), 3)
            data_2_nearest = data_2_pkte[newJ].reshape(len(newJ), 3)

            data_1_kr = _kr_1[newI].reshape(len(newI), 2)
            data_2_kr = _kr_2[newJ].reshape(len(newJ), 2)

            delta_kr = np.sum(np.abs(data_1_kr - data_2_kr), axis=1) / 2
            med = np.median(delta_kr[delta_kr > 0.0])
            sigma = 1.48257968 * np.median(np.abs(delta_kr[delta_kr > 0.0] - med))
            threshold = 5 * sigma + med
            delta_kr[delta_kr >= threshold] = np.NaN
            delta_kr_ohne_nan = delta_kr[~np.isnan(delta_kr)]
            d_mean_kr = np.sum(delta_kr_ohne_nan) / len(delta_kr_ohne_nan)
            # data_1_ver=np.column_stack((data_1_nearest,data_1_kr))
            # data_2_ver=np.column_stack((data_2_nearest,data_2_kr))

            # Src_zw[:,3:6]=Src_zw[:,3:6]/np.linalg.norm(Src_zw[:,3:6])
            # data_2_nearest[:,3:6]=data_2_nearest[:,3:6]/np.linalg.norm(data_2_nearest[:,3:6])

            # fval = np.linalg.norm((data_1_ver - data_2_ver))/len(newI)

            fval = np.linalg.norm((data_1_nearest - data_2_nearest)) / len(newI)
            fval_kr = d_mean_kr  # np.linalg.norm((data_1_kr - data_2_kr))/len(newI)
            if fval < min:
                min = fval
                pose_i = i
            if fval_kr < min_kr:
                min_kr = fval_kr
                pose_i_kr = i

            print(
                "{}\tnumVotes={}\tBewertung={}, {}".format(
                    i, pose.numVotes, fval, fval_kr
                )
            )
        print("Pose {} = MIN:{}".format(pose_i, min))
        print("Pose_kr {} = MIN:{}".format(pose_i_kr, min_kr))
        print("+" * 50)
        return _poses[pose_i], min

    class Detector:
        def __init__(
            self, _RelativeSamplingStep=0.05, _RelativeDistanceStep=0.05, _NumAngles=30
        ):
            self.sampling_step_relative = float(_RelativeSamplingStep)
            self.distance_step_relative = float(_RelativeDistanceStep)
            self.scene_sample_step = int(1.0 / 0.04)
            self.angle_step_relative = float(_NumAngles)
            self.angle_step_radians = (
                (360.0 / self.angle_step_relative) * math.pi / 180.0
            )
            self.angle_step = self.angle_step_radians
            self.trained = False
            self.samples_choice = 700

            self.position_threshold = self.sampling_step_relative
            self.rotation_threshold = (360.0 / self.angle_step) / 180.0 * math.pi
            self.use_weighted_avg = False

            self.export_datei = u"/00_PPF_Class.txt"
            self.export_path = GV.speicher_pathe["Speicher"]

        def trainModel(self, _Zieldata=np.array):
            xRange, yRange, zRange = computeBboxStd(_Zieldata)
            dx = xRange[1] - xRange[0]
            dy = yRange[1] - yRange[0]
            dz = zRange[1] - zRange[0]
            diameter = math.sqrt(dx * dx + dy * dy + dz * dz)
            distanceStep = diameter * self.sampling_step_relative

            ## Zusammenrechnung Punkte mit geringem Abstand. Schwierigkeiten bei duennen Bauteilen.
            sampled = samplePCByQuantization(
                _Zieldata, xRange, yRange, zRange, self.sampling_step_relative, False
            )
            # sampled = _Zieldata[np.random.choice(len(_Zieldata),self.samples_choice, False)]
            # print sampled
            # sampled_pkt, sampled_norms=EE_ICP.sample_pc_stable(_Zieldata[:,0:3],_Zieldata[:,3:6],samples)

            # sampled=np.vstack({tuple(row) for row in np.column_stack((sampled_pkt,sampled_norms))})

            # _plot_export(sampled,_Zieldata,"test_0")

            size = numPPF = int(sampled.shape[0] ** 2)
            hashTable = {}
            self.ppf = np.empty((numPPF, PPF_LENGTH), dtype=float)
            self.test_dict = {}
            numRefPoints = int(sampled.shape[0])
            for i in range(numRefPoints):

                p1 = sampled[i][0:3]
                n1 = sampled[i][3:6]

                for j in range(numRefPoints):
                    if i != j:
                        p2 = sampled[j][0:3]
                        n2 = sampled[j][3:6]

                        # print "-"*10
                        # print "{} {}".format(i,j)

                        f = self.computePPFFeatures(p1, n1, p2, n2)
                        key, hashvalue = hashPPF(
                            f, self.angle_step_radians, distanceStep
                        )
                        alpha, mpt = computeAlpha(p1, n1, p2)
                        ppfInd = i * numRefPoints + j

                        # print "a={}={}".format(alpha,alpha*180.0/math.pi)
                        # print hashvalue
                        # print key

                        if hashvalue in hashTable:
                            hashTable[hashvalue][ppfInd] = (key, i, j)
                        else:
                            hashTable[hashvalue] = {ppfInd: (key, i, j)}

                        self.ppf[ppfInd, 0:4] = f.T
                        self.ppf[ppfInd, 4] = float(alpha)
                        self.test_dict[ppfInd] = mpt

            self.distance_step = distanceStep
            self.hash_table = hashTable
            self.num_ref_points = numRefPoints
            self.sampled_pc = sampled
            self.trained = True

        def computePPFFeatures(self, _p1, _n1, _p2, _n2):
            ## Winkel zwischen n1|d, n2|d, n1|n2 und Betrag des Abstandes |d|
            f = np.zeros((4, 1))
            d = _p2 - _p1
            f[3] = np.linalg.norm(d)
            if f[3] <= EPS:
                return
            d *= 1.0 / f[3]

            f[0] = TAngle3Normalized(_n1, d)
            f[1] = TAngle3Normalized(_n2, d)
            f[2] = TAngle3Normalized(_n1, _n2)
            # print "f:"
            # print f[0]*180/math.pi
            # print f[1]*180/math.pi
            # print f[2]*180/math.pi
            # print f[3]
            return f

        def match(self, _data, relativeSceneSampleStep, relativeSceneDistance):
            if self.trained == False:
                print("Zieldata wurde nicht trainiert. Match nicht moeglich")
                raise
            if relativeSceneSampleStep > 1.0:
                print("relativeSceneSampleStep > 1.0")
                raise
            if relativeSceneDistance < 0.0:
                print("relativeSceneDistance < 0.0")
                raise

            numAngles = int(math.floor(2 * math.pi / self.angle_step))
            distanceStep = self.distance_step
            n = self.num_ref_points
            sceneSamplingStep = int(1.0 / relativeSceneSampleStep)

            xRange, yRange, zRange = computeBboxStd(_data)
            ## Zusammenrechnung Punkte mit geringem Abstand. Schwierigkeiten bei duennen Bauteilen.
            sampled = samplePCByQuantization(
                _data, xRange, yRange, zRange, relativeSceneDistance, False
            )
            # print sampled
            # sampled = _data[np.random.choice(len(_data),self.samples_choice, False)]
            # print len(sampled)
            # sampled = _data
            # sampled_pkt, sampled_norms=EE_ICP.sample_pc_stable(_data[:,0:3],_data[:,3:6],samples)
            # sampled=np.vstack({tuple(row) for row in np.column_stack((sampled_pkt,sampled_norms))})
            # _plot_export(sampled,_data,"test_1")

            # poseList=[0]*((sampled.shape[0]/sceneSamplingStep)+4)
            # poseList_i=0
            poseList = []
            dict_a = {0: 3, 1: 2, 2: 0, 3: 1}
            dict_b = {0: 0, 1: 1, 2: 3, 3: 2}
            for i in range(0, sampled.shape[0], sceneSamplingStep):
                refIndMax = alphaIndMax = maxVotes = 0

                p1 = sampled[i][0:3]
                n1 = sampled[i][3:6]

                accumulator = [0] * (numAngles * n)
                # if i==2:
                #    print "break"

                ## Was bringt Projektion auf X-Achse?!?? Besser Rotationsmatrix/Winkel?
                Rsg, tsg = computeTransformRT(p1, n1)

                for j in range(sampled.shape[0]):
                    if i != j:

                        p2 = sampled[j][0:3]
                        n2 = sampled[j][3:6]
                        # print "-"*10
                        # print "{} {}".format(i,j)
                        # if i==2 and j==3:
                        #    print "break"
                        f = self.computePPFFeatures(p1, n1, p2, n2)
                        key, hashvalue = hashPPF(f, self.angle_step, distanceStep)

                        p2t = tsg + Rsg.dot(p2)

                        alpha_scene = np.arctan2(-p2t[2], p2t[1])

                        # print "a={}={}".format(alpha_scene,alpha_scene*180.0/math.pi)
                        # print hashvalue
                        # print key

                        if math.sin(alpha_scene) * p2t[2] < 0.0:
                            alpha_scene = -alpha_scene

                        if hashvalue in self.hash_table:
                            node = self.hash_table[hashvalue]

                            for eintrag_i in node:

                                ppfInd = eintrag_i
                                eintrag = node[eintrag_i]
                                corrI = eintrag[1]
                                corrJ = eintrag[2]
                                status_i = ""
                                druck_i = False
                                if dict_a[i] == dict_b[corrI]:
                                    status_i = "i=i"
                                    druck_i = True
                                elif dict_a[i] == dict_b[corrJ]:
                                    status_i = "i=j"
                                    druck_i = False

                                status_j = ""
                                druck_j = False
                                if dict_a[j] == dict_b[corrI]:
                                    status_j = "j=i"
                                    druck_j = False
                                elif dict_a[j] == dict_b[corrJ]:
                                    status_j = "j=j"
                                    druck_j = True

                                ppfCorrScene = self.ppf[ppfInd]
                                alpha_model = ppfCorrScene[PPF_LENGTH - 1]
                                alpha = alpha_model - alpha_scene
                                p_train = self.test_dict[ppfInd]

                                alpha_index = int(
                                    numAngles
                                    * (alpha + 2.0 * math.pi)
                                    / (4.0 * math.pi)
                                )
                                accIndex = corrI * numAngles + alpha_index
                                accumulator[accIndex] += 1

                                v_org = (
                                    self.sampled_pc[corrJ][0:3]
                                    - self.sampled_pc[corrI][0:3]
                                )
                                v_org_norm = v_org / np.linalg.norm(v_org)
                                trans_akt = self.sampled_pc[corrI][0:3] - p1
                                v_akt = (p2) - (p1)
                                v_akt_norm = v_akt / np.linalg.norm(v_akt)
                                v_cross = np.cross(v_akt_norm, v_org_norm)
                                v_sin = np.linalg.norm(v_cross)
                                v_cos = v_akt_norm.dot(v_org_norm)
                                v_sin_deg = math.asin(v_sin) * 180.0 / math.pi
                                v_cos_deg = math.acos(v_cos) * 180.0 / math.pi

                                v_x = np.array(
                                    [
                                        [0, -v_cross[2], v_cross[1]],
                                        [v_cross[2], 0, -v_cross[0]],
                                        [-v_cross[1], v_cross[0], 0],
                                    ]
                                )
                                R_akt = (
                                    np.eye(3)
                                    + v_x
                                    + np.power(v_x, 2) * 1.0 / (1.0 + v_cos)
                                )
                                test = R_akt.dot(v_akt_norm)
                                test_2 = R_akt.dot(v_org_norm)
                                R_eig = np.linalg.eig(R_akt)[1][0]

                                R_1_t, t_1_t = computeTransformRT(p1, v_akt_norm)

                                R_1_t_inv = R_1_t.T
                                t_1_t_Inv = -R_1_t_inv.dot(t_1_t).reshape(3, 1)

                                R_2_t, t_2_t = computeTransformRT(
                                    self.sampled_pc[corrI][0:3], v_org_norm
                                )

                                R_x = R_1_t.dot(R_2_t)
                                R_x_inv = R_1_t_inv.dot(R_2_t)

                                R_x_eig = np.linalg.eig(R_x)[1][0]
                                R_x_inv_eig = np.linalg.eig(R_x_inv)[1][0]

                                R_x_a = (
                                    math.acos((np.trace(R_x) - 1) / 2) * 180 / math.pi
                                )
                                R_x_inv_a = (
                                    math.acos((np.trace(R_x_inv) - 1) / 2)
                                    * 180
                                    / math.pi
                                )

                                test_3 = R_x.dot(p1)
                                test_4 = R_x_inv.dot(p1)

                                if druck_i == True and druck_j == True:
                                    print("+" * 2)
                                    # print "{} {} vs. {} {}".format(i,j,corrI,corrJ)
                                    print(
                                        "{} {} vs. {} {}".format(
                                            dict_a[i],
                                            dict_a[j],
                                            dict_b[corrI],
                                            dict_b[corrJ],
                                        )
                                    )
                                    # print "status_i: {}".format(status_i)
                                    # print "status_j: {}".format(status_j)
                                    print(p2t)
                                    print(alpha_scene)
                                    print(p_train)
                                    print(alpha_model)
                                    print(
                                        "a={}={}".format(alpha, alpha * 180.0 / math.pi)
                                    )
                                    print(alpha_index)  # ,accIndex)
                                    print(
                                        "Sin={},Cos={}".format(
                                            round(v_sin_deg, 2), round(v_cos_deg, 2)
                                        )
                                    )
                                    print(R_eig)
                                    print(R_akt)

                                    # print "Stand acc={}".format(accumulator[accIndex])

                ## Suche nach Eintrag Max accumulator. Optimierungspotenzial!!
                for k in range(n):
                    for j in range(numAngles):
                        accInd = k * numAngles + j
                        accVal = accumulator[accInd]
                        if accVal > maxVotes:
                            maxVotes = accVal
                            refIndMax = k
                            alphaIndMax = j
                ## Aktueller Punkt auf x-Achse
                RInv = Rsg.T
                tInv = -RInv.dot(tsg).reshape(3, 1)

                TsgInv = rtToPose(RInv, tInv)

                ## Max. korrelierender Punkt auf x-Achse
                pMax = self.sampled_pc[refIndMax][0:3]
                nMax = self.sampled_pc[refIndMax][3:6]
                Rmg, tmg = computeTransformRT(pMax, nMax)
                tmg = tmg.reshape(3, 1)
                Tmg = rtToPose(Rmg, tmg)

                ## Haeufigste Winkelabweichung beider Punkte
                alpha_index = alphaIndMax
                alpha = (alpha_index * (4.0 * math.pi)) / numAngles - 2.0 * math.pi
                t = np.zeros((3, 1))
                R = getUnitXRotation(alpha)
                Talpha = rtToPose(R, t)

                rawPose = TsgInv.dot(Talpha.dot(Tmg))

                pose = Pose3D(alpha, refIndMax, maxVotes)
                pose.updatePose(rawPose)

                poseList.append(pose)
                # poseList_i+=1

            # numPosesAdded = int(sampled.shape[0]/sceneSamplingStep)
            numPosesAdded = len(poseList)
            print("Anzahl Poses org={}".format(numPosesAdded))
            results = self.clusterPoses(poseList, numPosesAdded)
            return results

        def clusterPoses(self, poseList, numPoses):

            poseClusters = []
            keyfun = operator.attrgetter("numVotes")
            poseList.sort(key=keyfun, reverse=True)

            for i in range(numPoses):
                pose = poseList[i]
                assigned = False
                j = 0
                while assigned == False and j < len(poseClusters):
                    poseCenter = poseClusters[j].poseList[0]
                    ## CHeck Matchpose Radian und relativer Abstand!! (Angepasst)
                    if self.matchPose(pose, poseCenter):
                        poseClusters[j].addPose(pose)
                        assigned = True
                    j += 1
                if assigned == False:
                    pose_Cluster_akt = PoseCluster(pose)
                    poseClusters.append(pose_Cluster_akt)

            keyfun = operator.attrgetter("numVotes")
            poseClusters.sort(key=keyfun, reverse=True)

            finalPoses = [0] * len(poseClusters)
            if self.use_weighted_avg == True:
                for i in range(len(poseClusters)):
                    qAvg = np.zeros((4, 1))
                    tAvg = np.zeros((3, 1))
                    curCluster = poseClusters[i]
                    curPoses = curCluster.poseList
                    curSize = len(curPoses)
                    numTotalVotes = 0

                    for j in range(curSize):
                        numTotalVotes += curPoses[j].numVotes

                    wSum = 0

                    for j in range(curSize):

                        w = curPoses[j].numVotes / numTotalVotes
                        qAvg += w * curPoses[j].q
                        tAvg += w * curPoses[j].t
                        wSum += w

                    tAvg *= 1.0 / wSum
                    qAvg *= 1.0 / wSum

                    curPoses[0].updatePoseQuat(qAvg, tAvg)
                    curPoses[0].numVotes = curCluster.numVotes

                    finalPoses[i] = curPoses[0]
            else:
                for i in range(len(poseClusters)):
                    qAvg = np.zeros((4, 1))
                    tAvg = np.zeros((3, 1))
                    curCluster = poseClusters[i]
                    curPoses = curCluster.poseList
                    curSize = len(curPoses)

                    for j in range(curSize):
                        qAvg += curPoses[j].q
                        tAvg += curPoses[j].t

                    tAvg *= 1.0 / curSize
                    qAvg *= 1.0 / curSize

                    curPoses[0].updatePoseQuat(qAvg, tAvg)
                    curPoses[0].numVotes = curCluster.numVotes

                    finalPoses[i] = curPoses[0]

            return finalPoses

        def matchPose(self, sourcePose, targetPose):
            dv = targetPose.t - sourcePose.t
            dNorm = np.linalg.norm(dv)
            phi = math.fabs(sourcePose.angle - targetPose.angle)
            export = False
            ## Angepasst...
            if (
                phi < (self.angle_step_relative * math.pi / 180.0)
                and dNorm < self.distance_step
            ):
                # if phi<self.rotation_threshold and dNorm<self.position_threshold:
                export = True
            return export

        def save_fkt(self):

            pickle_datei = open(self.export_path + self.export_datei, "wb")
            export_tuple = (
                self.distance_step,
                self.hash_table,
                self.ppf,
                self.num_ref_points,
                self.sampled_pc,
            )
            _pi.dump(export_tuple, pickle_datei)
            pickle_datei.close()

        def load_fkt(self):
            pickle_datei = open(self.export_path + self.export_datei, "rb")
            export_tuple = _pi.load(pickle_datei)
            (
                self.distance_step,
                self.hash_table,
                self.ppf,
                self.num_ref_points,
                self.sampled_pc,
            ) = export_tuple
            self.trained = True
            pickle_datei.close()

    class Pose3D:
        def __init__(self, Alpha, ModelIndex=0, NumVotes=0):
            self.alpha = Alpha
            self.modelIndex = ModelIndex
            self.numVotes = NumVotes
            self.residual = 0
            self.angle = 0
            self.q = 0

            self.pose = np.zeros((4, 4))

        def updatePose(self, _NewPose):
            self.pose = _NewPose
            self.R, self.t = poseToRT(self.pose)
            self.trace = np.trace(self.R)

            if math.fabs(self.trace - 3) <= EPS:
                self.angle = 0
            else:
                if math.fabs(self.trace + 1) <= EPS:
                    self.angle = math.pi
                else:
                    self.angle = math.acos((self.trace - 1.0) / 2.0)
            self.q = dcmToQuat(self.R)

        def updatePoseQuat(self, Q, NewT):
            self.NewR = quatToDCM(Q)
            self.q = Q

            self.pose = rtToPose(self.NewR, NewT)

            self.trace = np.trace(self.NewR)

            if math.fabs(self.trace - 3.0) <= EPS:
                self.angle = 0
            else:
                if math.fabs(self.trace + 1.0) <= EPS:
                    self.angle = math.pi
                else:
                    self.angle = math.acos((self.trace - 1.0) / 2.0)

        def appendPose(self, IncrementalPose):

            PoseFull = IncrementalPose.dot(self.pose)
            self.R, self.t = poseToRT(PoseFull)
            self.trace = np.linalg.norm(self.R)

            if math.fabs(self.trace - 3) <= EPS:
                self.angle = 0
            else:
                if math.fabs(self.trace + 1) <= EPS:
                    angle = math.pi
                else:
                    self.angle = math.acos((self.trace - 1.0) / 2.0)
            self.q = dcmToQuat(self.R)
            self.pose = PoseFull

    class PoseCluster:
        def __init__(self, _pose=None):
            self.numVotes = 0
            self.id = 0

            self.poseList = []
            if _pose != None:
                self.poseList.append(_pose)
                self.numVotes = _pose.numVotes

        def addPose(self, _pose):
            self.poseList.append(_pose)
            self.numVotes += _pose.numVotes

