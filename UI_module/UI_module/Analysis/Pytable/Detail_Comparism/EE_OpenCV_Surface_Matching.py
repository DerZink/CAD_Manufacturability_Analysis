# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import cv2, time, copy
import numpy as np
import EE_PPF3DDetector, EE_ICP, EE_PPF3D_Zink
import Global_Variables as GV
import pickle as _pi


def _start(_data_1, _data_2, combination):
    test_len = 1000  # 1000 #50 ### Influence how many points are put into the analysis
    max_curvature = 10.0 ** 6
    points_1_org = _data_1[0][0:test_len]
    norm_1_org = _data_1[1][0:test_len]
    kr_1_org = _data_1[2]
    kr_1_org[kr_1_org > max_curvature] = max_curvature
    kr_1_org[kr_1_org < -max_curvature] = -max_curvature
    kr_1_org = np.nan_to_num(kr_1_org)[0:test_len]
    data_1 = copy.deepcopy(np.column_stack((points_1_org, norm_1_org)))
    points_2_org = _data_2[0][0:test_len]
    norm_2_org = _data_2[1][0:test_len]
    kr_2_org = _data_2[2]
    kr_2_org[kr_2_org > max_curvature] = max_curvature
    kr_2_org[kr_2_org < -max_curvature] = -max_curvature
    kr_2_org = np.nan_to_num(kr_2_org)[0:test_len]
    data_2 = np.column_stack((points_2_org, norm_2_org))

    # fig = plt.figure()
    # ax_0  = fig.add_subplot(111,projection='3d')
    # ax_0.scatter(points_1_org[:,0], points_1_org[:,1], points_1_org[:,2],
    #                c="b", marker="o")
    # ax_0.scatter(points_2_org[:,0], points_2_org[:,1], points_2_org[:,2],
    #                c="r", marker="p")
    # plt.show()

    export_file = u"/00_PPF_results.txt"
    export_path = GV.save_paths["Speicher"]

    ID_min_Pose_abs = None
    diff_min_pose_abs = np.inf

    print("PPF3-Start")

    # detector=EE_PPF3DDetector.Detector(0.05, 0.05,360)
    detector = EE_PPF3D_Zink.Detector(0.15, 0.05, 30, combination)
    tim_1 = time.time()
    print("PPF3 Training")
    detector.trainModel(data_2)
    # detector.load_fkt()
    for i in range(1):
        # detector.save_fkt()
        ##detector.load_fkt()
        print("PPF3 abgleich")
        # print np.round(data_2,3)
        results = detector.match(data_1, 1.0 / 1.0, 0.15)
        # pickle_file=open(export_path+export_file,"wb")
        # export_tuple=(results)
        # _pi.dump(export_tuple,pickle_file)

        # pickle_file=open(export_path+export_file,"rb")
        # export_tuple=_pi.load(pickle_file)
        # results=export_tuple

        # pickle_file.close()

        #    print "Anzahl Cluster={}".format(len(results))
        time_pose = time.time()
        results_short = EE_PPF3D_Zink.EE_PPF3D_Zink()._check_poses(
            results, data_1, data_2, kr_1_org, kr_2_org
        )
        print("Duration Pose-Check {}s".format(round(time.time() - time_pose, 2)))
        # ICP_test=cv2.ppf_match_3d_ICP(100, 0.005, 2.5, 8)
        # ICP_test.registerModelToScene(data_2,data_1,results)
        print("PPF3-End")
        print("ICP-Start")
        ICP = EE_ICP.EE_ICP().ICP(0.005, 100, 2.5, 1, 6, 0, 1, 0)
        ICP.visualize_overview = 1
        ICP.pathsxport = r"X:\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging\Bauteil_Karte\01_Daten-Bauteil"  # "D:\Bauteil_Karte\01_Daten-Bauteil"
        # ICP.combination=["{}_Loop_{}".format(i,combination[0]),str(combination[1])]
        ICP.combination = combination
        ICP.start(data_1, data_2, results_short, kr_1_org, kr_2_org)

        # ICP.registerModelToScene(data_1,
        # data_2)
        # print "Beste Startbedingung={}".format(ICP.ID_min_pose)
        # print "Geringste Abweichung={}".format(round(ICP.diff_min_pose,4))
        print("-" * 50)
        if ICP.diff_min_pose < diff_min_pose_abs:
            diff_min_pose_abs = ICP.diff_min_pose
            ID_min_Pose_abs = [i, ICP.ID_min_pose]
            min_pose_ICP = ICP.min_pose
        ## Umbauen? nur beste Pose der ICP (kein Posecluster) nehmen und nochmal in die ICP
        ## auch quatsch... ICP checken
        # results_short=ICP.poses
        # data_1=EE_ICP.transformPCPose(data_1,min_pose_ICP)

    print("ICP-Ende")
    tim_2 = time.time()

    ## export Test:
    ## Hand:
    # pose_1=np.array([[9.99444772e-01,5.63944074e-04,-1.01678660e-02,-2.17041066e-01],
    #                 [-1.02014863e-03,9.98487311e-01,-4.48954793e-02,1.45837152e-01],
    #                 [1.01322667e-02,4.49035269e-02,9.98436060e-01,-5.05956685e+00],
    #                 [0,0,0,1]])
    # pose_2=np.array([[-9.99267935e-01,-3.49638251e-02,-1.55281857e-02,2.00680763e+02],
    #                [3.49318593e-02,-9.99386992e-01,2.32512480e-03,2.09646984e+02],
    #                [-1.55999620e-02,1.78099426e-03,9.99876727e-01,1.19026755e+00],
    #                [0,0,0,1]])
    # poses={31:pose_1,539:pose_2}
    # pose_check=[31,539]
    poses = ICP.poses
    pose_check = [ICP.ID_min_pose, ICP.i_kr_min, ICP.i_sum_min]
    pose_check_set = set(pose_check)
    # print pose_check
    path_pictures = GV.save_paths["Ergebnisse"]
    pickle_file = open(
        path_pictures
        + r"/{}vs{}_surface_matching.txt".format(combination[0], combination[1]),
        "wb",
    )
    export_poses = [x.pose for x in poses]
    export_tuple = (
        pose_check_set,
        export_poses,
        data_1,
        data_2,
        kr_1_org,
        kr_2_org,
    )
    _pi.dump(export_tuple, pickle_file)
    pickle_file.close()
    for i in pose_check_set:

        # data_PPF=EE_ICP.transformPCPose(data_1,min_pose_PPF.pose)
        # print "PPF, Abweichung={}".format(val_pose_PPF)
        # print min_pose_PPF.pose
        data_ICP = EE_ICP.EE_ICP().transformPCPose(data_1, poses[i].pose)
        # data_ICP=EE_ICP.transformPCPose(data_1,poses[i])

        d_means, data_filter, kr_filter = EE_ICP.EE_ICP().aberrance(
            data_ICP, data_2, kr_1_org, kr_2_org
        )
        print(d_means[0], d_means[1])
        # print len(data_ICP),len(data_2),len(data_filter[0])

        # print "ICP, Abweichung={}".format(diff_min_pose_abs)
        print("ICP {}".format(i))
        print(poses[i].pose)

        fig = plt.figure()
        ax_0 = fig.add_subplot(221)
        # ax_0.scatter(data_2[:,0], data_2[:,1], data_2[:,2], c="b", marker=".")
        ##ax_0.scatter(data_PPF[:,0], data_PPF[:,1], data_PPF[:,2], c="r", marker="o")
        # ax_0.scatter(data_ICP[:,0], data_ICP[:,1], data_ICP[:,2], c="r", marker="^")

        ax_1 = fig.add_subplot(222, projection="3d")

        t_multiplier = int(len(data_filter[0]) / 9)
        t = []
        t_i = 0
        while t_i < t_multiplier:
            t_i += 1
            for item in range(20):
                t.append(item)
        # t=range(20)*int(len(data_filter[0])/9) ### Changed for Python 3 ###
        t = t[0 : len(data_filter[0])]
        # t = np.arange(len(data_filter[0]))
        ax_1.scatter(data_2[:, 0], data_2[:, 1], data_2[:, 2], c="b", marker="o")
        ax_1.scatter(data_ICP[:, 0], data_ICP[:, 1], data_ICP[:, 2], c="r", marker="p")

        ax_2 = fig.add_subplot(212, projection="3d")
        t_2_hist = kr_filter[2][~np.isnan(kr_filter[2])]
        t_2 = kr_filter[2]
        t_2[np.isnan(t_2)] = -50.0
        if len(t_2_hist) != 0:
            ax_0.hist(t_2_hist, 50, log=True)
            ax_0.autoscale_view(True, True, True)
        # print t_2
        c_map = "jet"
        # print "Kr_neu={}".format(np.sum(t_2,axis=0)/len(t_2))
        ax_2.scatter(
            data_filter[1][:, 0],
            data_filter[1][:, 1],
            data_filter[1][:, 2],
            c=t_2,
            cmap=plt.get_cmap(c_map),
            marker="o",
        )
        aha = ax_2.scatter(
            data_filter[0][:, 0],
            data_filter[0][:, 1],
            data_filter[0][:, 2],
            c=t_2,
            cmap=plt.get_cmap(c_map),
            marker="p",
        )
        # im = ax_2.imshow(t_2, cmap=c_map)
        # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        # fig.colorbar(im, cax=cbar_ax)
        plt.colorbar(aha, ax=ax_2)

        ax_1.autoscale_view(True, True, True)
        ax_2.autoscale_view(True, True, True)
        plt.savefig(
            path_pictures
            + r"/{}vs{}_{}_surface_matching.png".format(
                combination[0], combination[1], i
            )
        )
        # plt.show()
        plt.close()

    # print "Dauer Erkennung= {}s".format(round(tim_2-tim_1,0))
    # print "Beste Startbedingung={}".format(ID_min_Pose_abs)
    # print "Geringste Abweichung={}".format(round(diff_min_pose_abs,4))
