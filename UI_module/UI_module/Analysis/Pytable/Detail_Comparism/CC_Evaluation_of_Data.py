# -*- coding: utf-8 -*-
import time,os,random,sys,math,itertools
import pickle as _pi
#import C_PyTables_Funktionen.B_Pytables_Funktionen as PyTfkt_1
#import C_PyTables_Funktionen.C_Pytables_Funktionen_2 as PyTfkt_2 Not needet atm
import DD_Procrustes_Commandeur, EE_ICP, EE_OpenCV_Surface_Matching
from tables import *
import numpy as np


class Evaluation_of_Data():

    def _start(self):
        curvature_data_parts=self.read_of_data()
        combinations=list(itertools.combinations(curvature_data_parts.keys(),2))
        time_0=time.time()
        #combinations=[[0,1],[1,0],[0,2],[0,3],[0,4],[2,4],[0,5]]
        combinations=[[0,1]] ### influences how much is being analysed
        #combinations=[["test","test"]]
        for combination in combinations:
            print("#"*50)
            print("Kombi={}".format(combination))
            ID_1=combination[0]
            data_raw_1=curvature_data_parts[ID_1]
            koord_1=np.column_stack((data_raw_1.x_f,data_raw_1.y_f,data_raw_1.z_f))
            norm_1=np.column_stack((data_raw_1.normx_f,data_raw_1.normy_f,data_raw_1.normz_f))
            kr_1=np.column_stack((data_raw_1.Kruemmungsradius_1,data_raw_1.Kruemmungsradius_2))
            ID_2=combination[1]
            data_raw_2=curvature_data_parts[ID_2]
            koord_2=np.column_stack((data_raw_2.x_f,data_raw_2.y_f,data_raw_2.z_f))
            norm_2=np.column_stack((data_raw_2.normx_f,data_raw_2.normy_f,data_raw_2.normz_f))
            kr_2=np.column_stack((data_raw_2.Kruemmungsradius_1,data_raw_2.Kruemmungsradius_2))

            #koord_2=np.array([[0,0,0],
            #                  [55,0,0],
            #                  [55.0/2.0,60,0],
            #                  [27.5,30,20]])
            #koord_1=np.array([[48.72564295035,58.24165537896,57.13524204913],
            #                  [28.86751345948,28.86751345948,28.86751345948],
            #                  [24.20885247750,68.31595106721,81.57773683374],
            #                  [40.83374694503,81.65624288830,19.11255054512]])

            #norm_2=np.array([[-4.76849980118-0,
            #                  -5.20199978310-0,
            #                  14.35968690128-0],
            #                 [57.90884505092-55,
            #                  -3.17328551010-0,
            #                  8.75959021017-0],
            #                 [27.50000000000-55.0/2.0,
            #                  68.87520313960-60,
            #                  13.31280470941-0],
            #                 [27.50000000000-27.5,
            #                  30.00000000000-30,
            #                  36.00000000000-20]])
            #norm_1=np.array([[64.08236423873-48.72564295035,
            #                  55.40384798569-58.24165537896,
            #                  60.61632815402-57.13524204913],
            #                 [42.53503999552-28.86751345948,
            #                  20.61206613283-28.86751345948,
            #                  27.84462156709-28.86751345948],
            #                 [35.41228462766-24.20885247750,
            #                  67.88571173583-68.31595106721,
            #                  92.99255186396-81.57773683374],
            #                 [56.57621828095-40.83374694503,
            #                  82.55436086294-81.65624288830,
            #                  16.39814815391-19.11255054512]])

            #kr_2=np.array([[0,0],
            #               [1,1],
            #               [2,2],
            #               [3,3]])
            #kr_1=np.array([[3,3],
            #               [0,0],
            #               [2,2],
            #               [1,1]])

            time_01=time.time()
            #kategorien=["mit_Gauss_Mittlere","Kruemmungen"]
            #kategorien=["Koord_Gitter","Koord_Flaeche"]
            #DD_Procrustes_Commandeur._start(ID_1,ID_2,
            #                                ([daten_1,daten_2],[daten_3,daten_4]),
            #                                kategorien)
            EE_OpenCV_Surface_Matching._start([koord_1,norm_1,kr_1],[koord_2,norm_2,kr_2],combination)
            #EE_ICP._start([koord_1,norm_1],[koord_2,norm_2],combination)


            time_02=time.time()
            print("Dauer Analyse={}s".format(round(time_02-time_01),4))

        time_1=time.time()
        print("#"*50)
        print("Dauer Analyse_gesamt={}s".format(round(time_1-time_0),4))



    def read_of_data(self):
        import Global_Variables as GV
        import Table_Classes

        path_curvaturedata=GV.save_paths["Hauptdateipfade_Datenbank"]+GV.save_paths["HDF5"]+GV.save_paths["Kruemmungen_HDF5"]
        export_file=GV.save_paths["Datenbasis_Pickle"]
        export_path=GV.save_paths["Speicher"]

        if os.path.isfile(export_path+export_file)==False:
            ## Einlesen und Berechnen der Daten aus HDF5 Tabellen
            print("######## Read and Computation of Partdata from HDF5 Tables ########")
            _curvature_data=self.__curvaturedata(path_curvaturedata,
                                                GV.HDF5_def["Kruemmung"],
                                                GV.curvature_part)

            print("######## Read and Computation of Partdata done ########")
            print("######## Save and Export of Partdata ########")
            pickle_file=open(export_path+export_file,"wb")
            ##export_tuple=(ausgabe_koerperdaten,ausgabe_kruemmungen,ausgabe_NX_flaechen,ausgabe_zus_flaechen,ausgabe_groesste_flaechen)
            export_tuple=(_curvature_data)
            _pi.dump(export_tuple,pickle_file)
            pickle_file.close()
            print("######## Save and Export of Partdata done ########")
        else:
            print("######## Read of Partdata from File ########")
            pickle_file=open(export_path+export_file,"rb")
            export_tuple=_pi.load(pickle_file)
            pickle_file.close()
            print("######## Read of Partdata from File done ########")
    
        return export_tuple
    def __curvaturedata(self,_save_path_curvature,
                          _HDF5_def_curvature,
                          _class_parts):
        print("#### Read of Curvaturedata from HDF5 Tables ####")
        __separator=os.path.sep
        __path_HDF5_curvature=os.path.normpath(_save_path_curvature+__separator+_HDF5_def_curvature[0])
        pytables_file=open_file(__path_HDF5_curvature, mode = "r")
        #! Read all Part IDs
        distribution_table=pytables_file.get_node(_HDF5_def_curvature[1]+_HDF5_def_curvature[2][0])
        IDs=np.array(distribution_table.cols._f_col("ID"))
        distribution_table._f_close()
        #! Read Curvaturedata
        export_dict={}
        for ID in IDs:
            part_class=_class_parts(ID)
            _path_curvaturedata_part=_HDF5_def_curvature[1]+_HDF5_def_curvature[3][0]+_HDF5_def_curvature[1]+"Kruemmungsdaten_{}".format(ID)
            _table_curvatures=pytables_file.get_node(_path_curvaturedata_part)
            part_class._read_HDF5_Table(_table_curvatures)
            export_dict[ID]=part_class
        pytables_file.close()
        print("#### Read of Curvaturedata from HDF5 Tables done ####")
        return export_dict