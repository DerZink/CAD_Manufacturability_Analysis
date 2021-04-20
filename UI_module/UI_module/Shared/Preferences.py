# -*- coding: utf-8 -*-
from configparser import ConfigParser, ExtendedInterpolation
import os
from typing import Dict, List, Tuple

from Shared.Paths import PathsClass
from Analysis.Utility import generateid


class calcPrefClass(object):
    """calculation preferences"""

    draft_mode = bool

    def __init__(self):
        super().__init__()


class PreferencesClass:
    """Class for global preference handling
    - calculation preferences
    - paths
    """

    config = ConfigParser(interpolation=ExtendedInterpolation())

    def __init__(self, path=None, init=False):
        self.pathModule = os.getcwd()
        if not path is None:
            self.pathConfigFile = os.path.join(path, "config.ini")
        else:
            self.pathConfigFile = os.path.join(os.getcwd(), "Shared", "config.ini")
        self.__load__()

        if init == True:
            self.change(
                ["paths_top"],
                ["path_module", "path_nx"],
                [self.pathModule, os.environ["UGII_BASE_DIR"]],
            )
            self.__load__()

    def __load__(self):
        self.config.read(self.pathConfigFile)

    def getPaths(self) -> PathsClass():
        pathClassOutput = PathsClass()  # type: PathsClass
        pathsSections = [
            "paths_top",
            "paths_tools",
            "paths_tables",
            "paths_data",
            "pytables_naming",
            "similarity_columns",
        ]
        for pathSection in pathsSections:
            for keySection in self.config[pathSection]:
                path_i = self.config.get(pathSection, keySection)
                setattr(
                    pathClassOutput,
                    keySection,
                    os.path.normpath(path_i).replace("\\", os.sep),
                )
        lenTestID = len(generateid()) + 6
        setattr(pathClassOutput, "IDLength", lenTestID)

        pathClassOutput.update()
        return pathClassOutput

    def calculationPreferences(self) -> calcPrefClass:
        calcClassOutput = calcPrefClass()  # type: calcPrefClass
        pathsSections = ["calc_bool", "calc_float", "calc_int"]
        for pathSection in pathsSections:
            for keySection in self.config[pathSection]:
                value_i = self.config.get(pathSection, keySection)
                if pathSection == "calc_bool":
                    value_i = self.config.getboolean(pathSection, keySection)
                if pathSection == "calc_float":
                    value_i = self.config.getfloat(pathSection, keySection)
                if pathSection == "calc_int":
                    value_i = self.config.getint(pathSection, keySection)
                setattr(calcClassOutput, keySection, value_i)
        return calcClassOutput

    def getFeatureColumns(self) -> List[Tuple[str, str]]:
        featureColumnList = []
        for keySection in self.config["feature_columns"]:
            featureColumnList.append(
                (keySection, self.config.get("feature_columns", keySection))
            )
        return featureColumnList

    def getFeatureDetails(self) -> Dict[str, Tuple[str, str]]:
        featureDetailDict = {}
        for keySection in self.config["data_names"]:
            name_in = self.config.get("data_names", keySection)
            type_in = self.config.get("data_type", keySection)
            featureDetailDict[keySection] = (name_in, type_in)

        return featureDetailDict

    def getDetailColumns(self):
        DetailColumnClass = detailColumnsClass()
        for keySection in self.config["detail_columns"]:
            value_i = self.config.get("detail_columns", keySection)
            setattr(DetailColumnClass, keySection, value_i)
        return DetailColumnClass

    def getFeatureSimilarityColumns(self) -> Dict[str, list]:  # set]:
        featureSimilarityColumns = {}
        for keySection in self.config["feature_similarity_columns"]:
            value_i = (
                self.config.get("feature_similarity_columns", keySection)
                .replace(" ", "")
                .split(",")
            )
            featureSimilarityColumns[keySection] = value_i
        return featureSimilarityColumns

    def getUIpreferences(self):
        UIpreferences = {}
        for keySection in self.config["ui_prefs"]:
            value_i = self.config.get("ui_prefs", keySection).split(",")
            UIpreferences[keySection] = value_i
        return UIpreferences

    def change(self, groups: List[str], variables: List[str], values: List[str]):
        if len(values) != len(groups):
            groups = [groups[0]] * len(values)
        for i in range(len(values)):
            self.config[groups[i]][variables[i]] = values[i]
        self.__save__()

    def __save__(self):
        with open(self.pathConfigFile, "w") as configfile:
            self.config.write(configfile)


class detailColumnsClass(object):
    """detail columns"""

    x_box = ""
    y_box = ""
    z_box = ""
    x_face = ""
    y_face = ""
    z_face = ""
    norm_x = ""
    norm_y = ""
    norm_z = ""
    curv_1 = ""
    curv_2 = ""

    def __init__(self):
        super().__init__()
