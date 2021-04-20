# -*- coding: utf-8 -*-
"""
Definition of paths for analysis
"""
import os
import sys
import shutil


class PathsClass(object):
    """ This class contains all necessary paths for the analysis"""

    (path_database, path_physicaldatabase, path_analyticaldatabase) = [""] * 3

    def __init__(self):
        super().__init__()

    def update(self):
        self.folders = [
            self.path_database,
            self.path_physicaldatabase,
            self.path_analyticaldatabase,
        ]
        self.__buildFolders()

    def __buildFolders(self):
        for folder in self.folders:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def getCSVpath(self, partFolder: str, csvName: str):
        return os.path.join(partFolder, csvName)
