from typing import List

import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets

from Analysis.Evaluation.DetailSimilarityClasses.PartPairClass import GS_PartPairclass
from Illustration.Preferences import CalibrationResults, PartPairs


def initPreferenceTree(self):

    ## Build Preferences TreeView from config.ini
    for treeCat in self.UIpreferences["pref_categories"]:
        parent = QtGui.QStandardItem(treeCat)
        subCatKey = "{}_categories".format(treeCat.lower())
        if subCatKey in self.UIpreferences:
            for subCat in self.UIpreferences[subCatKey]:
                parent.appendRow(QtGui.QStandardItem(subCat))
        self.model_preferences.appendRow(parent)

    ## set preference view widget
    preferenceView_whiteBackground(self)
    self.widgetDict = {}

    partPairsWidget(self)
    calibrationResultFS(self)
    calibrationResultGS(self)


def partPairsWidget(self):
    partPairs = PartPairs.PartPairView(
        self.paths, self.featureSimilarityColumns, self.detailColumns, self.calcPrefs
    )
    partPairs.FScalibration_done.connect(
        lambda: calibrationResultFS(
            self,
            partPairs.FScalibration.A,
            partPairs.FScalibration.y,
            partPairs.FScalibration.weights,
        )
    )

    partPairs.GScalibration_done.connect(
        lambda: calibrationResultGS(
            self,
            partPairs.GScalibration.GS_BodyPairclass_list,
            partPairs.GScalibration.GS_Objective,
            partPairs.GScalibration.xSolution,
        )
    )

    self.widgetDict[
        self.UIpreferences["pref_categories"][1],
        self.UIpreferences["calibration_categories"][0],
    ] = partPairs.partPairWidget


def calibrationResultFS(
    self,
    matrixA: np.ndarray = None,
    vectorY: np.ndarray = None,
    solutionX: np.ndarray = None,
):
    calibrationResult = CalibrationResults.CalibrationResultFS(
        self.paths, self.featureSimilarityColumns, matrixA, vectorY, solutionX
    )
    self.widgetDict[
        self.UIpreferences["pref_categories"][1],
        self.UIpreferences["calibration_categories"][1],
    ] = calibrationResult.calibrationResultWidget


def calibrationResultGS(
    self,
    partPairs: List[GS_PartPairclass] = None,
    vectorY: np.ndarray = None,
    solutionX: np.ndarray = None,
):
    calibrationResult = CalibrationResults.CalibrationResultsGS(
        self.paths, self.detailColumns, self.calcPrefs, partPairs, vectorY, solutionX
    )
    self.widgetDict[
        self.UIpreferences["pref_categories"][1],
        self.UIpreferences["calibration_categories"][2],
    ] = calibrationResult.calibrationResultWidget


def preferenceView_whiteBackground(self):
    preferenceWidget = QtWidgets.QWidget()  # tyype: QtWidgets.QWidget
    preferenceWidget.setAutoFillBackground(True)
    palette = preferenceWidget.palette()
    palette.setColor(preferenceWidget.backgroundRole(), QtCore.Qt.white)
    preferenceWidget.setPalette(palette)
    self.setPreferenceWidget(preferenceWidget)
