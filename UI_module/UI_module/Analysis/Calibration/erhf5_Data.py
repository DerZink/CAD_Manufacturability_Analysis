#!/usr/bin/python
import os.path
import pickle

import numpy as np
from sklearn.neighbors import NearestNeighbors
from tables import *


class erhf5_Data:
    """description of class"""

    def __init__(self, path: str, name: str, *args, **kwargs):
        self.filename = name.split(os.path.sep)[-1].split(".")[0]
        self.partname = name.split(os.path.sep)[-1].split("_")[0]
        # if self.partname =="Pyramide":
        #     self.partname = "Kofferecke"
        self.h5file = name
        print("-" * 5 + self.filename + "-" * 5)
        self.pickleFileNameRaw = path + os.path.sep + self.filename + "_raw.pickle"
        self.pickleFileNameCalced = (
            path + os.path.sep + self.filename + "_calced.pickle"
        )
        self._openSavedDataCalced()
        if not self.pickleFileCalced:
            self._openSavedDataRaw()
            if not self.pickleFileRaw:
                self._readH5()
            self._calcData()
        print("-" * 20)

    def _readH5(self):
        print("Opening {}".format(self.h5file))
        self.h5 = open_file(self.h5file)
        self._find_lastSimStep()
        self._collectElements()
        self.h5.close()
        self._saveRawData()

    def _calcData(self):
        print("Calculation {}".format(self.h5file))
        self._find_neighbors()
        self._saveDataCalced()

    def _find_lastSimStep(self):
        # path to all simulated sates
        simStates = self.h5.get_node("/", "post/singlestate")
        self.timeMax = 0
        self.lastState = ""
        for state in simStates:
            timeStepArray = state.__getattr__(
                "entityresults/SHELL/Shear_Angle/ZONE1_set1/erfblock/indexval"
            )
            timeStep = timeStepArray[0]
            if timeStep > self.timeMax:
                self.timeMax = timeStep
                self.lastState = state

        print("Last Timestep = ", self.timeMax)

    def _collectElements(self):
        # collect stamp and textile elements
        print("Start collecting data of elements and Nodes")

        # find ID of textile and stamp
        array_ShellPartNames = self.h5.get_node(
            "/", "post/constant/attributes/PART/erfblock/title"
        )
        array_ShellPartName_ID = self.h5.get_node(
            "/", "post/constant/attributes/PART/erfblock/entid"
        )
        pos_name = 0
        ID_stamp_ = 0
        ID_textile_ = 0
        ID_blankholder_ = 0
        for name_byte in array_ShellPartNames:
            name = str(name_byte, "utf-8").replace(" ", "")
            if "Halbzeug" in name:
                ID_textile_ = array_ShellPartName_ID[pos_name]
            if self.partname in name:
                ID_stamp_ = array_ShellPartName_ID[pos_name]
            if "Niederhalter" in name:
                ID_blankholder_ = array_ShellPartName_ID[pos_name]
            pos_name += 1
        self.ID_stamp = ID_stamp_
        self.ID_textile = ID_textile_
        self.ID_blankholder = ID_blankholder_

        self.elementsStamp_dict = {}
        stampEndCoords_list = []
        self.elementsTextileAll_dict = {}
        self.textileNodeID_list = []
        self.textileStartCoords_dict = {}
        textileEndCoords_list = []
        self.elementsBlankholder_dict = {}
        blankholderCoords_list = []

        # array of part IDs for elements
        array_ShellPartIDs = self.h5.get_node(
            "/", "post/constant/connectivities/SHELL/erfblock/pid"
        )
        # array of nodes IDs for elements
        array_ShellNodeIDs = self.h5.get_node(
            "/", "post/constant/connectivities/SHELL/erfblock/ic"
        )
        self.shellNodes_dict = {}
        # array of node positions
        array_NodePositions = self.h5.get_node(
            "/", "post/constant/entityresults/NODE/COORDINATE/ZONE1_set0/erfblock/res"
        )
        # array of final node displacement
        array_NodeDisplacement = self.lastState.__getattr__(
            "entityresults/NODE/Translational_Displacement/ZONE1_set1/erfblock/res"
        )
        # array of element shear angle
        array_ShearAngle = self.lastState.__getattr__(
            "entityresults/SHELL/Shear_Angle/ZONE1_set1/erfblock/res"
        )
        # array of element position in shear angle array
        array_ShearAnglePos = self.lastState.__getattr__(
            "entityresults/SHELL/Shear_Angle/ZONE1_set1/erfblock/entid"
        )

        pos = 0
        nodeSavedCheck = set()
        for shell in array_ShellPartIDs:
            if (
                shell == self.ID_stamp
                or shell == self.ID_textile
                or shell == self.ID_blankholder
            ):
                nodes = array_ShellNodeIDs[pos]
                shellID = pos + 1

                centerStart = np.array([0.0, 0.0, 0.0])
                centerEnd = np.array([0.0, 0.0, 0.0])
                countNodes = 0
                # go through nodes of shell element
                for node in nodes:
                    arrayPos = node - 1
                    nodeCoords = array_NodePositions[arrayPos]
                    centerStart += nodeCoords
                    nodeDisplacement = array_NodeDisplacement[arrayPos]
                    nodeLastCoords = nodeCoords + nodeDisplacement
                    centerEnd += nodeLastCoords

                    # save node for nearest neighbor calc
                    if not node in nodeSavedCheck:
                        if shell == self.ID_stamp:
                            stampEndCoords_list.append(nodeLastCoords)
                        elif shell == self.ID_textile:
                            self.textileStartCoords_dict[node] = nodeCoords
                            textileEndCoords_list.append(nodeLastCoords)
                            self.textileNodeID_list.append(node)
                        elif shell == self.ID_blankholder:
                            blankholderCoords_list.append(nodeLastCoords)

                    # save node shell connection for shear angle import
                    if shell == self.ID_textile:
                        if not node in self.shellNodes_dict:
                            self.shellNodes_dict[node] = [shellID]
                        else:
                            self.shellNodes_dict[node].append(shellID)
                    nodeSavedCheck.add(node)
                    countNodes += 1

                centerStart /= countNodes
                centerEnd /= countNodes

                if shell == self.ID_textile:
                    shearPos = np.where(array_ShearAnglePos[:] == shellID)[0][0]
                    shearAngle = array_ShearAngle[shearPos][0]
                    self.elementsTextileAll_dict[shellID] = (
                        nodes,
                        centerStart,
                        centerEnd,
                        shearAngle,
                    )
                elif shell == self.ID_stamp:
                    stampEndCoords_list.append(centerEnd)
                    for node in nodes:
                        arrayPos = node - 1
                        nodeCoords = array_NodePositions[arrayPos]
                        nodeCenterMid = (nodeCoords + centerEnd) * 0.5
                        stampEndCoords_list.append(nodeCenterMid)
                elif shell == self.ID_blankholder:
                    blankholderCoords_list.append(centerEnd)
                    # for node in nodes:
                    #     arrayPos = node-1
                    #     nodeCoords = array_NodePositions[arrayPos]
                    #     nodeCenterMid = (nodeCoords + centerEnd)*0.5
                    #     blankholderCoords_list.append(nodeCenterMid)

            pos += 1

        # arrays of element coords for nearest neighbor algorithm
        self.stampEndCoords_array = np.array(stampEndCoords_list)
        self.textileEndCoords_array = np.array(textileEndCoords_list)
        self.blankholderCoords_array = np.array(blankholderCoords_list)

        print("Collecting finished")

    def _find_neighbors(self):
        # find nearest neighbor of stamp on textile
        print("Start searching neighbors")
        # train of stamp coords
        nbrs_stamp = NearestNeighbors(n_neighbors=1, algorithm="auto", n_jobs=-1).fit(
            self.stampEndCoords_array
        )
        # train of blankholder coords
        nbrs_blankholder = NearestNeighbors(
            n_neighbors=1, algorithm="auto", n_jobs=-1
        ).fit(self.blankholderCoords_array)
        # calc distances to stamp
        distances_stamp, indices_stamp = nbrs_stamp.kneighbors(
            self.textileEndCoords_array
        )
        # calc distances to blankholder
        distances_blankholder, indices_blankholder = nbrs_blankholder.kneighbors(
            self.textileEndCoords_array
        )

        self.formedNodesTextile_list = []
        pos_indice = 0
        dist2blankholder_min = 8.0
        # dist2stamp_max = width of blankholder (4mm buffer resulting because of stamp blankholder distance)
        dist2stamp_max = 40
        # first check distance of every textile node to blankholder
        for distance_blankholder in distances_blankholder:
            # get textile node ID to blankholder
            node_ID = self.textileNodeID_list[pos_indice]
            # get distance
            distance2blankholder = distance_blankholder[0]
            # if higher than threshold
            if distance2blankholder >= dist2blankholder_min:
                # check distance to stamp
                distance2stamp = distances_stamp[pos_indice][0]
                # if lower than threshold
                if distance2stamp <= dist2stamp_max:
                    # calc mean shear angle
                    elementsOfNode = self.shellNodes_dict[node_ID]
                    meanShearAngle = 0
                    for nodeElement in elementsOfNode:
                        shearAngle = self.elementsTextileAll_dict[nodeElement][3]
                        meanShearAngle += shearAngle
                    meanShearAngle = meanShearAngle / len(elementsOfNode)
                    # get node data
                    nodeStartCoords = self.textileStartCoords_dict[node_ID]
                    nodeEndCoords = self.textileEndCoords_array[pos_indice]
                    self.formedNodesTextile_list.append(
                        (nodeStartCoords, nodeEndCoords, meanShearAngle, distance2stamp)
                    )

                    # if not element_ID in self.formedNodesTextile_list:
                    #     element_data = self.elementsTextileAll_dict[element_ID]
                    #     self.formedNodesTextile_list[element_ID] = (
                    #         element_data[0], element_data[1], element_data[2], element_data[3], distance)
                    # else:
                    #     distance_old = self.formedNodesTextile_list[element_ID][4]
                    #     if distance < distance_old:
                    #         element_data = self.elementsTextileAll_dict[element_ID]
                    #         self.formedNodesTextile_list[element_ID] = (
                    #             element_data[0], element_data[1], element_data[2], element_data[3], distance)
            pos_indice += 1

        print("Neighbor search finished")

    def _saveRawData(self):
        print("Save raw data with pickle")
        with open(self.pickleFileNameRaw, "wb", pickle.HIGHEST_PROTOCOL) as handle:
            pickle.dump(
                (
                    self.textileNodeID_list,
                    self.shellNodes_dict,
                    self.elementsTextileAll_dict,
                    self.stampEndCoords_array,
                    self.textileStartCoords_dict,
                    self.textileEndCoords_array,
                    self.blankholderCoords_array,
                ),
                handle,
            )
        handle.close()

    def _saveDataCalced(self):
        print("Save calc data with pickle")
        with open(self.pickleFileNameCalced, "wb", pickle.HIGHEST_PROTOCOL) as handle:
            pickle.dump(self.formedNodesTextile_list, handle)
        handle.close()

    def _openSavedDataRaw(self):
        self.pickleFileRaw = False
        if os.path.isfile(self.pickleFileNameRaw):
            self.pickleFileRaw = True
            print("Load raw data with pickle")
            with open(self.pickleFileNameRaw, "rb") as handle:
                savedRawData = pickle.load(handle)
                (
                    self.textileNodeID_list,
                    self.shellNodes_dict,
                    self.elementsTextileAll_dict,
                    self.stampEndCoords_array,
                    self.textileStartCoords_dict,
                    self.textileEndCoords_array,
                    self.blankholderCoords_array,
                ) = savedRawData
            handle.close()

    def _openSavedDataCalced(self):
        self.pickleFileCalced = False
        if os.path.isfile(self.pickleFileNameCalced):
            self.pickleFileCalced = True
            print("Load calc data with pickle")
            with open(self.pickleFileNameCalced, "rb") as handle:
                self.formedNodesTextile_list = pickle.load(handle)
            handle.close()
