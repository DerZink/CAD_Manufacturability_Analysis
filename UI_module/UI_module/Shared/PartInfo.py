import os
from Shared.Paths import PathsClass
from configparser import ConfigParser, ExtendedInterpolation


class PartInfoClass(object):
    """Stores the single part info"""

    def __init__(
        self,
        assemblyId: str = "",
        partName: str = "",
        partPath: str = "",
        createdate: str = "",
        currdate: str = "",
        partIDstr: str = "",
        pathClass: PathsClass = None,
    ):
        partNr = None
        if partIDstr != "" and assemblyId == "":
            assemblyId = "".join(partIDstr.split("_")[:-1])
            partNr = partIDstr.split("_")[-1]

        self.assemblyId = assemblyId
        self.partName = ".".join(str(partName).split(".")[0:-1])
        self.partFormat = str(partName).split(".")[-1]
        self.partPath = os.path.normpath(partPath)  # origin path of part
        self.createDate = createdate
        self.currdate = currdate
        self.statusFeatureAnalysis = "False"
        self.statusDetailAnalysis = "False"

        if not pathClass is None:
            self.defineOutputPaths(pathClass)
            if not partNr is None:
                self.updateDecomposition(partNr)
                self.definePointCloudData(pathClass)

    def updateAccessdate(self, newdate):
        self.currdate = newdate

    def defineOutputPaths(self, pathClass: PathsClass):
        self.paths = pathClass
        self.name_physicalDirectory = self.assemblyId
        self.path_physicalDirectory = os.path.join(
            self.paths.path_physicaldatabase, self.name_physicalDirectory
        )

    def updateDecomposition(self, partID: str):
        self.partId = partID
        self.partName_physicalDatabase = self.partId
        self.name_physicalDirectory = self.partId
        self.path_physicalDirectory = os.path.join(
            self.path_physicalDirectory, self.name_physicalDirectory
        )
        self.savePartProperties()

    def savePartProperties(self):
        if os.path.isdir(self.path_physicalDirectory):
            properties = ConfigParser(interpolation=ExtendedInterpolation())
            pathPropertyFile = os.path.join(
                self.path_physicalDirectory, self.paths.namedata_partproperties
            )
            properties["part_data"] = {
                "Name": self.partName,
                "Origin": self.partPath,
                "Date": self.currdate,
            }

            with open(pathPropertyFile, "w") as PropertyFile:
                properties.write(PropertyFile)

    def definePointCloudData(self, pathClass: PathsClass):

        self.namedata_pointcloud_preferences = pathClass.namedata_pointcloud_preferences

        self.name_pointCloudDataTrained = (
            self.partName_physicalDatabase + pathClass.namedata_pointcloud_trained
        )
        self.path_pointCloudDataTrained = os.path.join(
            self.path_physicalDirectory, self.name_pointCloudDataTrained
        )

        self.name_pointCloudDataPreferences = (
            self.partName_physicalDatabase + self.namedata_pointcloud_preferences
        )
        self.path_pointCloudDataPreferences = os.path.join(
            self.path_physicalDirectory, self.name_pointCloudDataPreferences
        )

    def getTotalID(self) -> str:
        return self.assemblyId + "_" + self.partId

    def featureAnalysis(self, status: str):
        self.statusFeatureAnalysis = status

    def detailAnalysis(self, status: str):
        self.statusDetailAnalysis = status

    def databaseRow(self, row: int) -> int:
        self.row_db = row
